import uuid
from flask import Flask, jsonify, redirect, request, send_file, send_from_directory
import games

# Disable static folder because anything under /static should return 404
app = Flask(__name__)

# Load games
MineSweeper = games.games['MineSweeper']
running_games = dict()

@app.route('/<game>/game', methods=["GET"]) 
def indexGame():
    # Check if game id is in query params
    if 'id' not in request.args:
        return "Error: no game id"
    
    id = request.args.get("id") # Get game id from query params
    
    game = running_games.get(id) # Get game from running games - can be None
    if game is None: # If game is not found, return error
        return f"Error: game with id `{id}` not found"
    
    return send_file(f"games/{game}/{game}.html")

@app.route('/<game>/game', methods=["PUT"])
def playGame():
    # Check if game id is in query params
    if 'id' not in request.args:
        return jsonify(status="error", message=f"Error: no game id")
    
    id = request.args.get("id") # Get game id from query params

    game = running_games.get(id) # Get game from running games - can be None
    if game is None: # If game is not found, return error
        return jsonify(status="error", message=f"Error: game with id `{id}` not found")
    
    action = request.json.get("action")
    data = request.json.get("data")

    if action == "board":
        return jsonify(data=game.get_board())
    
    elif action == "pick":
        row = data.get("row")
        col = data.get("col")

        res = game.pickSpace(row, col)
        if res == False:
            return jsonify(status="error", message="Invalid move")

        return jsonify(data=game.pickSpace(row, col))
    
    else:
        return jsonify(status="error", message="Invalid action")

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

@app.route("/stream")
def subscribe():
    def emitter():
        while True:
            yield 'data: <data>\n\n'

app.run(port=8080)