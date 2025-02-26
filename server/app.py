from flask import Flask, request, send_file

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello!"

@app.route("/form", methods=["POST", "GET"])
def postIndex():
    user = request.form.get("user")
    print(user)
    return send_file("./static/form.html")

app.run(port=3000)