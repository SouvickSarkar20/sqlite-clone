"""
Test for the BTree.
"""
import os
from core.pager import Pager
from core.btree import BTree

def test_btree_insert_and_search():
    db_file = "test_btree.db"
    if os.path.exists(db_file):
        os.remove(db_file)
        
    pager = Pager(db_file)
    btree = BTree(pager)
    
    # Insert rows
    row1 = {"id": 10, "name": "alice", "age": 25}
    row2 = {"id": 20, "name": "bob", "age": 30}
    row3 = {"id": 5, "name": "charlie", "age": 35}
    
    # Inserting out of order
    btree.insert(row1["id"], row1)
    btree.insert(row2["id"], row2)
    btree.insert(row3["id"], row3)
    
    # Verify search
    assert btree.search(10) == row1
    assert btree.search(20) == row2
    assert btree.search(5) == row3
    
    # Search missing key
    assert btree.search(999) is None
    
    # Verify traversal (should be sorted by key)
    rows = list(btree.traverse())
    assert len(rows) == 3
    assert rows[0] == row3 # ID 5
    assert rows[1] == row1 # ID 10
    assert rows[2] == row2 # ID 20
    
    pager.close()
    
    # Verify persistence
    pager2 = Pager(db_file)
    btree2 = BTree(pager2)
    assert btree2.search(10) == row1
    
    pager2.close()
    print("BTree basic test passed!")
    
    if os.path.exists(db_file):
        os.remove(db_file)

def test_btree_split():
    db_file = "test_btree_split.db"
    if os.path.exists(db_file):
        os.remove(db_file)
        
    pager = Pager(db_file)
    btree = BTree(pager)
    
    # Each row payload is about ~30 bytes, so ~100 rows would be ~3400 bytes.
    # We will insert 200 rows to force at least one split.
    for i in range(1, 201):
        btree.insert(i, {"id": i, "name": f"person_{i}", "padding": "x" * 20})
        
    # Verify all of them
    for i in range(1, 201):
        row = btree.search(i)
        assert row is not None
        assert row["id"] == i
        
    rows = list(btree.traverse())
    assert len(rows) == 200
    for i, row in enumerate(rows):
        assert row["id"] == i + 1
        
    pager.close()
    if os.path.exists(db_file):
        os.remove(db_file)

if __name__ == "__main__":
    test_btree_insert_and_search()
    test_btree_split()
