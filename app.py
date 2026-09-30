from flask import Flask, render_template, jsonify
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
        return jsonify({"ok": False, "error": str(exc)}), 500
