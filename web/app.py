import os
import sys
import traceback
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# Add root directory to sys.path to resolve 'core' and 'sql' modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sql.parser import parse_statement
from core.executor import Executor

app = Flask(__name__)
# Enable CORS for all routes so our Vite frontend can talk to it
CORS(app)

# Initialize a persistent executor with a file
DB_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "test.db")
os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
executor = Executor(DB_FILE)

@app.route("/")
def index():
    """Serve the main UI page where users type SQL queries."""
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def query():
    """
    Receives a SQL string from the frontend.
    Passes it through the parser and executor.
    Returns the result as JSON along with step-by-step progress.
    """
    data = request.get_json()
    sql = data.get("sql", "").strip()
    
    steps = []
    
    # Step 1: Parsing
    try:
        steps.append({"action": "Parsing SQL", "status": "running"})
        parsed_stmt = parse_statement(sql)
        steps[-1]["status"] = "success"
        steps[-1]["details"] = parsed_stmt
    except Exception as e:
        steps[-1]["status"] = "error"
        steps[-1]["details"] = str(e)
        return jsonify({"status": "error", "message": f"Parse Error: {e}", "steps": steps})
        
    # Step 2: Executing
    try:
        steps.append({"action": "Executing Query against B-Tree", "status": "running"})
        result = executor.execute(parsed_stmt)
        
        # The executor could return an Error string if an operation fails (like "Error: ...")
        if isinstance(result, str) and result.startswith("Error:"):
            steps[-1]["status"] = "error"
            steps[-1]["details"] = result
            return jsonify({"status": "error", "message": result, "steps": steps})
            
        steps[-1]["status"] = "success"
        
        # Differentiate between SELECT operations and others
        if isinstance(result, list):
            # It's a list, meaning it's a SELECT result
            return jsonify({
                "status": "success",
                "message": f"Successfully retrieved {len(result)} rows.",
                "data": result,
                "steps": steps
            })
        else:
            # It's a string, meaning it's a CREATE/INSERT message
            return jsonify({
                "status": "success",
                "message": result,
                "steps": steps
            })
            
    except Exception as e:
        steps[-1]["status"] = "error"
        steps[-1]["details"] = traceback.format_exc()
        return jsonify({"status": "error", "message": f"Execution Error: {e}", "steps": steps})

if __name__ == "__main__":
    # In production (Render, etc.), the PORT environment variable is provided.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)