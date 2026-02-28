"""
Pager (Your Disk Manager):
Reads and writes 4KB pages to/from the .db file.
"""

import os

PAGE_SIZE = 4096

class Pager:
    def __init__(self, filename):
        """
        Open the database file. If it doesn't exist, it will be created.
        We keep a dictionary `pages` as our memory cache.
        """
        self.filename = filename
        
        # open the file in binary read/write mode ("r+b"). 
        # If it doesn't exist, we create it and then open it.
        if not os.path.exists(filename):
            open(filename, "w").close()
            
        self.file = open(filename, "r+b")
        self.pages: dict[int, bytearray] = {} # the cache: page_num -> bytes

        # calculate how many pages currently exist in the file
        self.file.seek(0, os.SEEK_END)
        self.num_pages = self.file.tell() // PAGE_SIZE

    def get_page(self, page_num):
        """
        Get a page. First check the memory cache. 
        If it's missing, read it from disk.
        """
        # If it's already in memory, just return it
        if page_num in self.pages:
            return self.pages[page_num]

        # Otherwise, calculate where it sits on disk
        offset = page_num * PAGE_SIZE
        
        # We might be asking for a brand new page at the very end of the file
        if page_num >= self.num_pages:
            # Create a brand new empty page filled with 0s
            page = bytearray(PAGE_SIZE)
            self.num_pages += 1
        else:
            # Seek to the correct offset and read 4KB
            self.file.seek(offset)
            page = bytearray(self.file.read(PAGE_SIZE))
            
        # Cache it for next time
        self.pages[page_num] = page
        return page

    def flush_page(self, page_num):
        """
        Write a specific page from memory back to the disk.
        """
        if page_num in self.pages:
            page = self.pages[page_num]
            assert len(page) == PAGE_SIZE, f"Page {page_num} size is {len(page)}, expected {PAGE_SIZE}"
            
            offset = page_num * PAGE_SIZE
            self.file.seek(offset)
            self.file.write(page)
            # Ask the OS to actually write to disk immediately (optional but good)
            self.file.flush()

    def close(self):
        """
        Close the pager, making sure to flush all cached pages back to disk first.
        """
        for page_num in self.pages.keys():
            self.flush_page(page_num)
        self.file.close()

