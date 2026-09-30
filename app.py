from flask import Flask, render_template, jsonify
import os
from livesport_tenis_agent import run_scan

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/scan")
def scan():
    try:
        results, diagnostics = run_scan()
        return jsonify({"ok": True, "results": results, "diagnostics": diagnostics})
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
