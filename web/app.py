

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    """Serve the main UI page where users type SQL queries."""
    return render_template("index.html")


@app.route("/query", methods=["POST"])
def query():
    """
    Receives a SQL string from the frontend.
    Passes it through the parser and executor.
    Returns the result as JSON.

    Wired up fully in Phase 6.
    """
    # Placeholder — real logic added in Phase 6
    data = request.get_json()
    sql = data.get("sql", "").strip()

    # For now, just echo back what was sent
    return jsonify({
        "status": "ok",
        "message": f"Received: {sql} — Query engine coming in Phase 6!"
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)