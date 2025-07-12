from flask import Flask, request, jsonify, render_template
import requests
import base64

app = Flask(__name__)

REPLICATE_API_TOKEN = "r8_example_demokey"  # замените на свой токен
MODEL_VERSION = "cjwbw/sdxl-morpheus-style"  # замените при необходимости

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    file = request.files["image"]
    img_data = base64.b64encode(file.read()).decode("utf-8")
    b64_img = f"data:image/jpeg;base64,{img_data}"

    response = requests.post(
        "https://api.replicate.com/v1/predictions",
        headers={"Authorization": f"Token {REPLICATE_API_TOKEN}"},
        json={
            "version": MODEL_VERSION,
            "input": {
                "image": b64_img,
                "prompt": "portrait of a man in black coat, dark sunglasses, green matrix digital rain background, offering red and blue pill",
                "num_inference_steps": 40
            }
        },
    )

    output = response.json()
    url = output.get("urls", {}).get("get", None)
    return jsonify({"status": "ok", "image_url": url})