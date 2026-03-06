"""
The SQL Parser:
Reads a raw SQL string and returns a structured Python dict describing the intent.
Supports: CREATE TABLE, INSERT INTO, SELECT.
"""
import re

def parse_statement(sql: str) -> dict:
    """
    Parses a SQL string into a dictionary.
    """
    sql = sql.strip()
    # Normalize whitespace but be careful around quotes if we supported them fully.
    # For now, a simple normalize is fine for our subset.
    sql = re.sub(r'\s+', ' ', sql)

    if sql.upper().startswith("CREATE TABLE"):
        # Format: CREATE TABLE users (id, name, age)
        match = re.match(r"CREATE TABLE\s+(\w+)\s*\((.*?)\)", sql, re.IGNORECASE)
        if match:
            table_name = match.group(1)
            columns = [col.strip() for col in match.group(2).split(',')]
            return {"type": "CREATE", "table": table_name, "columns": columns}
            
    elif sql.upper().startswith("INSERT INTO"):
        # Format: INSERT INTO users VALUES (1, 'alice', 25)
        match = re.match(r"INSERT INTO\s+(\w+)\s+VALUES\s*\((.*?)\)", sql, re.IGNORECASE)
        if match:
            table_name = match.group(1)
            values_str = str(match.group(2))
            # Basic parsing of values (integers vs strings)
            # Not robust against commas inside strings, but works for the MVP
            values = []
            for val in values_str.split(','):
                val = val.strip()
                if val.startswith("'") and val.endswith("'"):
                    values.append(val[1:-1]) # type: ignore
                elif val.startswith('"') and val.endswith('"'):
                    values.append(val[1:-1]) # type: ignore
                elif val.isdigit():
                    values.append(int(val))
                else:
                    values.append(val) # type: ignore
            return {"type": "INSERT", "table": table_name, "values": values}

    elif sql.upper().startswith("SELECT"):
        # Format: SELECT * FROM users [WHERE id = 1]
        match = re.match(r"SELECT\s+\*\s+FROM\s+(\w+)(?:\s+WHERE\s+(.*?))?$", sql, re.IGNORECASE)
        if match:
            table_name = match.group(1)
            where_str = match.group(2)
            
            where_dict = None
            if where_str:
                # Expecting simple: column = value
                where_match = re.match(r"(\w+)\s*=\s*(.*)", where_str)
                if where_match:
                    col = str(where_match.group(1))
                    val_str = str(where_match.group(2)).strip()
                    
                    if val_str.isdigit():
                        val = int(val_str) # type: ignore
                    elif (val_str.startswith("'") and val_str.endswith("'")) or (val_str.startswith('"') and val_str.endswith('"')):
                        val = val_str[1:-1] # type: ignore
                    else:
                        val = val_str # type: ignore
                        
                    where_dict = {"col": col, "op": "=", "val": val}
            
            return {"type": "SELECT", "table": table_name, "where": where_dict}

    raise ValueError(f"Unrecognized or unsupported SQL statement: {sql}")
