from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "shopping_data.json"

# ❌ words जो product नहीं हैं
STOP_WORDS = [
    "add", "buy", "remove", "delete", "to",
    "my", "the", "list", "please", "can",
    "you", "me", "from"
]

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {"items": [], "history": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def categorize(item):
    categories = {
        "milk": "Dairy",
        "cheese": "Dairy",
        "apple": "Produce",
        "banana": "Produce",
        "pineapple": "Produce",
        "chicken": "Meat",
        "fish": "Meat",
        "rice": "Grains",
        "oil": "Grocery"
    }
    return categories.get(item, "Others")

def extract_product(words):
    for w in words:
        if w not in STOP_WORDS:
            return w
    return None

@app.route("/")
def index():
    data = load_data()
    return render_template("index.html", items=data["items"])

@app.route("/process", methods=["POST"])
def process():
    text = request.json["command"].lower()
    words = text.split()
    data = load_data()

    # ➕ ADD / BUY
    if "add" in words or "buy" in words:
        item = extract_product(words)

        if not item:
            return jsonify({"message": "No product detected"})

        data["items"].append({
            "name": item,
            "category": categorize(item),
            "time": str(datetime.now())
        })
        data["history"].append(item)
        save_data(data)
        return jsonify({"message": f"{item} added successfully"})

    # ❌ REMOVE
    if "remove" in words or "delete" in words:
        item = extract_product(words)

        if not item:
            return jsonify({"message": "No product detected"})

        data["items"] = [i for i in data["items"] if i["name"] != item]
        save_data(data)
        return jsonify({"message": f"{item} removed successfully"})

    # 💡 SUGGEST
    if "suggest" in words:
        if data["history"]:
            return jsonify({"message": f"You often buy {data['history'][-1]}"})
        return jsonify({"message": "No suggestions available"})

    return jsonify({"message": "Command not recognized"})


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
