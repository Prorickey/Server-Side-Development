from flask import Flask, request, send_file, send_from_directory

# Disable static folder because anything under /static should return 404
app = Flask(__name__, static_folder=None)

@app.route("/", methods=["GET"])
@app.route("/<path:filename>", methods=["GET"])
def serve_static(filename="login"):
    return send_from_directory("./static/", f"{filename}.html")

@app.route("/login", methods=["POST"])
def loginPost():
    print(request.form)
    return "POSTED"

@app.route("/games/minesweeper", methods=["GET"])
def minesweeper():
    return send_file("./games/minesweeper/intro.html")

@app.route("/games/minesweeper/game", methods=["GET"])
def minesweeperFile():
    return send_file("./games/minesweeper/minesweeper.html")

app.run(port=8080)