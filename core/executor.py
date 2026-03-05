"""
The Executor (Glue Layer):
Takes the parsed dict from the parser and calls the right B-Tree operation.
Connects parser, btree, and pager.
"""
from core.pager import Pager
from core.btree import BTree

class Executor:
    def __init__(self, db_file: str):
        self.pager = Pager(db_file)
        self.btree = BTree(self.pager)

    def execute(self, parsed_stmt: dict):
        stmt_type = parsed_stmt.get("type")

        if stmt_type == "CREATE":
            # For this simple clone, we don't strictly enforce schema
            # We just acknowledge it was created.
            return f"Table {parsed_stmt['table']} created."

        elif stmt_type == "INSERT":
            table_name = parsed_stmt["table"]
            values = parsed_stmt["values"]
            
            # We assume the first value is the primary key (id) for our BTree
            pk = values[0]
            
            # We'll just store the raw values array as the row dict for simplicity in the MVP
            # A real DB would map values to column names using the schema
            row_dict = {"values": values}
            
            try:
                self.btree.insert(pk, row_dict)
                return f"Inserted 1 row into {table_name}."
            except Exception as e:
                return f"Error: {e}"

        elif stmt_type == "SELECT":
            where_clause = parsed_stmt.get("where")
            
            results = []
            if where_clause:
                # We only support searching by primary key (id) for now
                if where_clause["col"] == "id" and where_clause["op"] == "=":
                    pk = where_clause["val"]
                    row = self.btree.search(pk)
                    if row:
                        results.append(row)
                else:
                    return f"Error: Only WHERE id = X is supported."
            else:
                # Traverse all records
                for row in self.btree.traverse():
                    results.append(row)
                    
            return results

        return "Error: Unknown statement type."
        
    def close(self):
        self.pager.close()
