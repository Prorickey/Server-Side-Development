from flask import Flask, request, send_file

# Disable static folder because anything under /static should return 404
app = Flask(__name__)

@app.route("/login", methods=["GET", "POST"])
def loginPost():
    user = request.form.get("user")
    password = request.form.get("password")
    mode = request.form.get("mode")
    return send_file("./static/login.html")

@app.route("/games/minesweeper", methods=["GET"])
def minesweeper():
    return send_file("./games/minesweeper/intro.html")
 
@app.route("/games/minesweeper/game", methods=["GET"])
def minesweeperFile():
    return send_file("./games/minesweeper/minesweeper.html")

app.run(port=8080)