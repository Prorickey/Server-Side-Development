from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello!"

@app.route("/form", methods=["POST", "GET"])
def postIndex():
    print(request.args.get("user"))
    return "FORM PAGE"

app.run(port=3000)