from flask import Blueprint, send_file, request, Response, redirect, jsonify
from .serverwrapper import ServerMineSweeper
import json
import os
import uuid
import redis

"""
The Flask Blueprint for the Minesweeper Game Module. 

This blueprint contains all routes and server-side code for this Game
"""

MineSweeperBlueprint = Blueprint('minesweeper', 'minesweeper')
bp_path = os.path.dirname(os.path.abspath(__file__))

runningGames = dict()
R_Server = redis.StrictRedis()
try:
    R_Server.ping()
except:
    print("REDIS: Not Running -- No Streams Available")
    R_Server = None

@MineSweeperBlueprint.route("/")
def index():
    """
        The introduction pages to the Game Module. This route
        handles the Creation of the game
    """
    path_to_file = os.path.join(bp_path, 'intro.html')
    return send_file(path_to_file)

@MineSweeperBlueprint.route('/game', methods=['GET', 'PUT'])
def gameOperations():
    """
        This route allows users to view and play game instances which 
        already exist. UUIDs to games are stored in the runningGames dictionary

        Returns:
            GET - the game html if the game exists, ERROR string if the game doesn't exist
            PUT - a JSON-encoded string based on the actions permitted
            
            The JSON is of the form:
                status: string {ok, error}
                message: string {action taken, error message}
                data: dictionary { payload dependent on action }

            For actions see the MineSweeper Server Wrapper
    """

    if 'id' not in request.args:
        return "ERROR: Game Does Not Exist"
    
    gameid = request.args.get('id')
    if gameid == None or gameid not in runningGames:
        return 'ERROR: Game Does Not Exist'

    if request.method == 'GET':
        return send_file(os.path.join(bp_path, 'minesweeper.html'))

    # Handle PUT Request
    body = request.get_json()
    if 'action' not in body or 'data' not in body:
        return "ERROR: Incomplete data"
    action = body.get('action')
    data = body.get('data')

    game = runningGames[gameid]
    
    # Setup the data packet -- assume success
    packet = {
        'status' : "OK", 
        'message' : action,
        'data' : { }
    }
    try:
        rtnPacket = game.action({
            'action': action, 
            'data': data
        })

        packet['data'] = rtnPacket

        # If _announce_ is in the packet, then accounce over PubSub
        # Delete the key, so it's not sent back to the client
        if '_announce_' in rtnPacket:
            publish = rtnPacket['_announce_']
            del rtnPacket['_announce_']
            if R_Server != None:
                R_Server.publish(gameid, json.dumps(publish))

    except Exception as e:
        # Invalid action attempted or missing required data for the action
        packet['status'] = 'Error'
        packet['message'] = f'ERROR: {str(e)}'

    return jsonify(packet)

@MineSweeperBlueprint.route('/game', methods=['POST'])
def gameCreation():
    """
        Route used to CREATE new games. Every constructor takes 
        creation options. If a required creation option is missing,
        the constructor raises an exception

        Returns:
            1. On successs, redirects to the GET game route with the valid UUID
            2. On failure, JSON-encoded string of the format
                status: string {error}, message: string {error string}
    """
    creationOptions = dict()
    for field in request.form:
        creationOptions[field] = request.form.get(field)
    
    factory = ServerMineSweeper
    try:

        # Attempt to create the game, store it, and redirect
        gameID = str(uuid.uuid4())
        gameLogic = factory(creationOptions)
        runningGames[gameID] = gameLogic
        return redirect(f'/minesweeper/game?id={gameID}')
    except Exception as e:

        # Creation failed
        return jsonify({
            'status': "error",
            'message': str(e)
        })

@MineSweeperBlueprint.route('/stream')
def gameStream():
    """
        Route used to allow subscription to this Game Module's PubSub
        mechanism.

        Returns:
            A response stream which allows for server-side events
    """
    
    if R_Server == None:
        return "ERROR: Updates Not Available"

    gameid = request.args.get('id')
    if gameid == None or gameid not in runningGames:
        return "ERROR: Game Does Not Exist" 

    def emitter():
        if R_Server == None:
            return 'data: Streaming Down\n\n'
        
        pubsub = R_Server.pubsub()
        pubsub.subscribe(gameid)
        for message in pubsub.listen():
            data = message['data']
            if type(data) == bytes:
                yield f'data: {data.decode()}\n\n'

    res = Response(emitter(), mimetype='text/event-stream')
    return res