import os
from core.pager import Pager

def test_pager_write_and_read():
    db_file = "test_mydb.db"
    
    # Clean up any leftover file from a previous test run
    if os.path.exists(db_file):
        os.remove(db_file)

    # 1. Open pager, write to page 0, and close
    pager1 = Pager(db_file)
    page0 = pager1.get_page(0)
    
    # write the word "hello" into the start of the page
    hello_bytes = b"hello"
    page0[:len(hello_bytes)] = hello_bytes
    
    # Close it, which flushes the pages to disk
    pager1.close()

    # 2. Re-open pager and ensure we can read our data back
    pager2 = Pager(db_file)
    restored_page0 = pager2.get_page(0)
    
    # Read the first 5 bytes back
    assert restored_page0[:5] == b"hello"
    
    pager2.close()
    
    print("Pager test passed!")

    # Cleanup afterwards
    os.remove(db_file)

if __name__ == "__main__":
    test_pager_write_and_read()
