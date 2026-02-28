"""
B-Tree (Your Index Engine):
B-Tree structure where each node lives in one page.
Implements insert, search, and a simple in-order traversal.
"""
import struct
from core.pager import PAGE_SIZE
from core.serializer import serialize_row, deserialize_row

NODE_TYPE_LEAF = 1
NODE_TYPE_INTERNAL = 2

# Node Header Offsets
NODE_TYPE_OFFSET = 0
IS_ROOT_OFFSET = 1
PARENT_POINTER_OFFSET = 2
NUM_CELLS_OFFSET = 6

LEAF_NODE_HEADER_SIZE = 8
INTERNAL_NODE_HEADER_SIZE = 12
RIGHT_CHILD_OFFSET = 8

class BTree:
    def __init__(self, pager):
        self.pager = pager
        self.root_page_num = 0
        
        if pager.num_pages == 0:
            self._initialize_root()
            
    def _initialize_root(self):
        page = self.pager.get_page(self.root_page_num)
        self._set_node_type(page, NODE_TYPE_LEAF)
        self._set_is_root(page, 1)
        self._set_parent_pointer(page, 0)
        self._set_num_cells(page, 0)
        

    def _get_node_type(self, page):
        return page[NODE_TYPE_OFFSET]
        
    def _set_node_type(self, page, node_type):
        page[NODE_TYPE_OFFSET] = node_type
        
    def _get_is_root(self, page):
        return page[IS_ROOT_OFFSET]
        
    def _set_is_root(self, page, is_root):
        page[IS_ROOT_OFFSET] = is_root

    def _get_parent_pointer(self, page):
        return struct.unpack('>I', page[PARENT_POINTER_OFFSET:PARENT_POINTER_OFFSET+4])[0]
        
    def _set_parent_pointer(self, page, parent_page_num):
        page[PARENT_POINTER_OFFSET:PARENT_POINTER_OFFSET+4] = struct.pack('>I', parent_page_num)

    def _get_num_cells(self, page):
        return struct.unpack('>H', page[NUM_CELLS_OFFSET:NUM_CELLS_OFFSET+2])[0]
        
    def _set_num_cells(self, page, num_cells):
        page[NUM_CELLS_OFFSET:NUM_CELLS_OFFSET+2] = struct.pack('>H', num_cells)

    def _get_right_child(self, page):
        return struct.unpack('>I', page[RIGHT_CHILD_OFFSET:RIGHT_CHILD_OFFSET+4])[0]
        
    def _set_right_child(self, page, child_page_num):
        page[RIGHT_CHILD_OFFSET:RIGHT_CHILD_OFFSET+4] = struct.pack('>I', child_page_num)

    # --- Cell Offset Logic ---
    def _leaf_node_cell_offset(self, cell_num, page):
        offset = LEAF_NODE_HEADER_SIZE
        for _ in range(cell_num):
            offset += 4
            payload_len = struct.unpack('>H', page[offset:offset+2])[0]
            offset += 2 + payload_len
        return offset

    def _internal_node_cell_offset(self, cell_num):
        return INTERNAL_NODE_HEADER_SIZE + (cell_num * 8)

    # --- Insert Logic ---
    def insert(self, key, row_dict):
        payload = serialize_row(row_dict)
        page_num = self._find_leaf_node(key)
        page = self.pager.get_page(page_num)
        
        num_cells = self._get_num_cells(page)
        insert_index = num_cells
        
        for i in range(num_cells):
            cell_offset = self._leaf_node_cell_offset(i, page)
            cell_key = struct.unpack('>I', page[cell_offset:cell_offset+4])[0]
            if key == cell_key:
                raise Exception("Duplicate keys are not supported.")
            elif key < cell_key:
                insert_index = i
                break
                
        cell_size = 4 + len(payload)
        end_offset = self._leaf_node_cell_offset(num_cells, page)
        
        if end_offset + cell_size > PAGE_SIZE:
            # Splitting required
            self._split_leaf_node(page_num, insert_index, key, payload)
        else:
            self._insert_into_leaf(page_num, insert_index, key, payload)

    def _insert_into_leaf(self, page_num, insert_index, key, payload):
        page = self.pager.get_page(page_num)
        num_cells = self._get_num_cells(page)
        
        cell_size = 4 + len(payload)
        start_offset = self._leaf_node_cell_offset(insert_index, page)
        end_offset = self._leaf_node_cell_offset(num_cells, page)
        
        # Shift cells right
        if insert_index < num_cells:
            page[start_offset + cell_size : end_offset + cell_size] = page[start_offset : end_offset]  # type: ignore
            
        page[start_offset:start_offset+4] = struct.pack('>I', key)
        page[start_offset+4:start_offset+4+len(payload)] = payload  # type: ignore
        
        self._set_num_cells(page, num_cells + 1)
        # Clear out space beyond to maintain exact 4096 bytes size
        page[end_offset + cell_size:] = bytearray(PAGE_SIZE - (end_offset + cell_size))  # type: ignore
        self.pager.flush_page(page_num)

    def _split_leaf_node(self, old_page_num, insert_index, key, payload):
        old_page = self.pager.get_page(old_page_num)
        num_cells = self._get_num_cells(old_page)
        
        cells = []
        for i in range(num_cells):
            offset = self._leaf_node_cell_offset(i, old_page)
            cell_key = struct.unpack('>I', old_page[offset:offset+4])[0]
            payload_len = struct.unpack('>H', old_page[offset+4:offset+6])[0]
            cell_payload = old_page[offset+4:offset+4+2+payload_len]
            cells.append((cell_key, cell_payload))
            
        cells.insert(insert_index, (key, payload))
        
        # Split point
        mid = len(cells) // 2
        left_cells = cells[:mid]  # type: ignore
        right_cells = cells[mid:]
        
        # Allocate new right page
        right_page_num = self.pager.num_pages
        right_page = self.pager.get_page(right_page_num) # This creates it
        self._set_node_type(right_page, NODE_TYPE_LEAF)
        self._set_is_root(right_page, 0)
        self._set_parent_pointer(right_page, 0)
        self._set_num_cells(right_page, 0)
        
        # Reset old page (left)
        self._set_num_cells(old_page, 0)
        # Re-initialize the byte array beyond header to avoid old data
        old_page[LEAF_NODE_HEADER_SIZE:] = bytearray(PAGE_SIZE - LEAF_NODE_HEADER_SIZE)  # type: ignore
        for i, (k, p) in enumerate(left_cells):
            self._insert_into_leaf(old_page_num, i, k, p)
            
        # Fill new page (right)
        for i, (k, p) in enumerate(right_cells):
            self._insert_into_leaf(right_page_num, i, k, p)
            
        right_min_key = right_cells[0][0]
        
        is_root = self._get_is_root(old_page)
        if is_root:
            self._create_new_root(old_page_num, right_page_num, right_min_key)
        else:
            parent_page_num = self._get_parent_pointer(old_page)
            self._set_parent_pointer(right_page, parent_page_num)
            self._insert_into_internal(parent_page_num, old_page_num, right_page_num, right_min_key)

    def _create_new_root(self, left_page_num, right_page_num, split_key):
        # We move the left child (which was the root at page 0) to a new page
        # And rewrite page 0 as the internal root node traversing them.
        left_child_page_num = self.pager.num_pages
        left_child_page = self.pager.get_page(left_child_page_num)
        old_root_page = self.pager.get_page(self.root_page_num) # page 0
        
        # Copy content
        left_child_page[:] = old_root_page[:]  # type: ignore
        self._set_is_root(left_child_page, 0)
        self._set_parent_pointer(left_child_page, self.root_page_num)
        
        right_child_page = self.pager.get_page(right_page_num)
        self._set_parent_pointer(right_child_page, self.root_page_num)
        
        # Turn old root into internal node
        self._set_node_type(old_root_page, NODE_TYPE_INTERNAL)
        self._set_is_root(old_root_page, 1)
        self._set_num_cells(old_root_page, 0)
        self._set_right_child(old_root_page, right_page_num)
        
        # Wipe rest of root page
        old_root_page[INTERNAL_NODE_HEADER_SIZE:] = bytearray(PAGE_SIZE - INTERNAL_NODE_HEADER_SIZE)  # type: ignore
        self._insert_into_internal(self.root_page_num, left_child_page_num, right_page_num, split_key)

        self.pager.flush_page(left_child_page_num)
        self.pager.flush_page(right_page_num)

    def _insert_into_internal(self, internal_page_num, left_child_page_num, right_child_page_num, key):
        page = self.pager.get_page(internal_page_num)
        num_cells = self._get_num_cells(page)
        
        insert_index = num_cells
        for i in range(num_cells):
            offset = self._internal_node_cell_offset(i)
            cell_key = struct.unpack('>I', page[offset+4:offset+8])[0]
            if key < cell_key:
                insert_index = i
                break
                
        start_offset = self._internal_node_cell_offset(insert_index)
        end_offset = self._internal_node_cell_offset(num_cells)
        
        if insert_index < num_cells:
            page[start_offset + 8 : end_offset + 8] = page[start_offset : end_offset]  # type: ignore
            
        page[start_offset:start_offset+4] = struct.pack('>I', left_child_page_num)
        page[start_offset+4:start_offset+8] = struct.pack('>I', key)
        
        if insert_index == num_cells:
            self._set_right_child(page, right_child_page_num)
            
        self._set_num_cells(page, num_cells + 1)
        self.pager.flush_page(internal_page_num)

    # --- Search Logic ---
    def search(self, key):
        page_num = self._find_leaf_node(key)
        page = self.pager.get_page(page_num)
        
        num_cells = self._get_num_cells(page)
        for i in range(num_cells):
            cell_offset = self._leaf_node_cell_offset(i, page)
            cell_key = struct.unpack('>I', page[cell_offset:cell_offset+4])[0]
            
            if cell_key == key:
                payload_bytes = page[cell_offset+4:]
                row_dict, _ = deserialize_row(payload_bytes)
                return row_dict
                
        return None

    def _find_leaf_node(self, key, page_num=0):
        page = self.pager.get_page(page_num)
        node_type = self._get_node_type(page)
        
        if node_type == NODE_TYPE_LEAF:
            return page_num
            
        num_cells = self._get_num_cells(page)
        for i in range(num_cells):
            cell_offset = self._internal_node_cell_offset(i)
            child_page_num = struct.unpack('>I', page[cell_offset:cell_offset+4])[0]
            cell_key = struct.unpack('>I', page[cell_offset+4:cell_offset+8])[0]
            
            if key < cell_key:
                return self._find_leaf_node(key, child_page_num)
                
        right_child = self._get_right_child(page)
        return self._find_leaf_node(key, right_child)
        
    def traverse(self, page_num=0):
        """
        Yield all rows in primary key order.
        """
        page = self.pager.get_page(page_num)
        node_type = self._get_node_type(page)
        
        if node_type == NODE_TYPE_LEAF:
            num_cells = self._get_num_cells(page)
            for i in range(num_cells):
                cell_offset = self._leaf_node_cell_offset(i, page)
                payload_bytes = page[cell_offset+4:]
                row_dict, _ = deserialize_row(payload_bytes)
                yield row_dict
        else:
            num_cells = self._get_num_cells(page)
            for i in range(num_cells):
                cell_offset = self._internal_node_cell_offset(i)
                child_page_num = struct.unpack('>I', page[cell_offset:cell_offset+4])[0]
                yield from self.traverse(child_page_num)
                
            right_child = self._get_right_child(page)
            yield from self.traverse(right_child)
