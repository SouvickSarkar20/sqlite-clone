"""
Test for the Executor.
"""
import os
import sys
import pytest

# Add the project directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sql.parser import parse_statement
from core.executor import Executor

def test_executor_insert_and_select():
    db_file = "test_executor.db"
    if os.path.exists(db_file):
        os.remove(db_file)
        
    executor = Executor(db_file)
    
    # 1. Create table (no-op in DB but returns success)
    create_stmt = parse_statement("CREATE TABLE users (id, name)")
    res = executor.execute(create_stmt)
    assert "created" in res
    
    # 2. Insert records
    stmt1 = parse_statement("INSERT INTO users VALUES (1, 'alice')")
    stmt2 = parse_statement("INSERT INTO users VALUES (2, 'bob')")
    
    executor.execute(stmt1)
    executor.execute(stmt2)
    
    # 3. Select all
    select_all = parse_statement("SELECT * FROM users")
    all_rows = executor.execute(select_all)
    
    assert len(all_rows) == 2
    assert all_rows[0] == {"values": [1, 'alice']}
    assert all_rows[1] == {"values": [2, 'bob']}
    
    # 4. Select with WHERE
    select_where = parse_statement("SELECT * FROM users WHERE id = 1")
    where_rows = executor.execute(select_where)
    
    assert len(where_rows) == 1
    assert where_rows[0] == {"values": [1, 'alice']}
    
    executor.close()
    
    if os.path.exists(db_file):
        os.remove(db_file)
