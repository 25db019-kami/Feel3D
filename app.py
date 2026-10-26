print("app.py 読み込まれた")
from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/generate", methods=["POST"])
def generate():

    print("generate呼ばれた")

    data = request.json

    print(data)

    weight = data["weight"]
    height = data["height"]
    chest = data["chest"]
    waist = data["waist"]
    hip = data["hip"]

    subprocess.run([
        "py",
        "-3.11",
        "export_smpl.py",
        str(weight),
        str(height),
        str(chest),
        str(waist),
        str(hip)
    ])

    return jsonify({
        "success": True
    })

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )