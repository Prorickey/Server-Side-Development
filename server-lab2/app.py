import uuid
from flask import Flask, redirect, request, send_file, send_from_directory
import games

# Disable static folder because anything under /static should return 404
app = Flask(__name__)

# Load games
MineSweeper = games.games['MineSweeper']
running_games = dict()

@app.route('/<game>/game', methods=["GET", "PUT"]) 
def indexGame(game):
    if 'id' not in request.args:
        return "Error: no game id"
    
    id = request.args.get("id")
    
    game = running_games.get(id)
    if game is None:
        return f"Error: game with id `{id}` not found"
    
    return send_file(f"games/{game}/{game}.html")

@app.route('/<game>/game', methods=["POST"]) 
def createGame(game):
    data = dict()
    params = ["rows", "cols", "name"]
    for param in params:
        if param not in request.args and param not in request.args:
            return f"Error: missing {param}"
        
        data[param] = request.args.get(param) if param in request.args else request.form.get(param)

    rows = data['rows']
    cols = data['cols']
    name = data['name']

    game = MineSweeper(rows, cols)
    id = uuid.uuid4()
    running_games[id] = game

    return redirect(f"/{game}/game?id={id}")

@app.route("/", methods=["GET"])
@app.route("/<path:filename>", methods=["GET"])
def serve_static(filename="login"):
    return send_from_directory("./static/", f"{filename}.html")

@app.route("/login", methods=["POST"])
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