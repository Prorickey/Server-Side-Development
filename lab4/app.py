import base64
import os
from flask import Flask, jsonify, make_response, request, send_file, redirect, render_template, Response
import redis
import games
import database
import uuid

app = Flask(__name__)

# Register all available games
for game in games.games:
    blueprint = games.games[game].blueprint()
    app.register_blueprint(blueprint, url_prefix=f'/{game}')

# Initialize the SQLite database
database.init()

# Connect to Redis
R_Server = redis.StrictRedis()
try:
    R_Server.ping()
except:
    print("REDIS: Not Running -- No Streams Available")
    R_Server = None

def get_token_data(token):
    """
    Get the session data from Redis using the token.
    If Redis is not available, return None.
    """

    # Check if Redis server is available
    if R_Server is None:
        return None
    try:
        # Get the session data from Redis
        session_data = R_Server.get(token)
        if session_data is not None:
            return session_data.decode('utf-8')
    except redis.exceptions.ConnectionError:
        print("REDIS: Not Running -- No Streams Available")
        
    return None

@app.route("/")
def index():
    # Get the session token from the request cookies - server-side token
    token = request.cookies.get('session')

    if token is None:
        # No token found, redirect to login page
        return redirect('/login')
    
    # Yay! the user is logged in and we redirect them to their profile
    user = get_token_data(token)

    if user is None:
        # No user found in redis, redirect to login page
        return redirect('/login')
    
    return redirect(f'/profile/{user}')

@app.route("/form", methods=['GET', 'POST'])
def postIndex():
    print( request.args.get('user') )
    print( request.form.get('user') )   
    return send_file('static/form.html')

@app.route("/login", methods=["GET", "POST"])
def loginPage():
    if request.method == "GET":
        # Get the session token from the request cookies - server-side token
        token = request.cookies.get('session')

        if token != None:
            user = get_token_data(token)
            if user != None:
                return redirect(f'/profile/{user}')
        
        return render_template('login.j2')
    
    fields = ['username', 'password', 'mode']
    for field in fields:
        if field not in request.form:
            return "ERROR"
        if len(str(request.form.get(field)).strip()) == 0:
            return "ERROR"
    
    if request.form.get('mode') not in ['login', 'register']:
        return render_template('login.j2', error="Malformed request")

    print(request.form.get('username'))
    print(request.form.get('password'))
    print('MODE:', str(request.form.get('mode')).upper())

    if request.form.get('mode').lower() == 'login':
        # Attempt to login the user
        if database.login(request.form.get('username'), request.form.get('password')):
            # Create the session token
            token = uuid.uuid4()

            # Store the session data in Redis
            R_Server.set(str(token), request.form.get('username').lower())

            # Set the session cookie in the response
            response = redirect('/games/minesweeper')
            response.set_cookie('session', str(token))
            return response
        else:
            # It's important that the message is generic to prevent user phishing attacks
            return render_template('login.j2', error="User doesn't exist or password is incorrect")
    elif request.form.get('mode').lower() == 'register':
        # Attempt to register the user
        if database.register(request.form.get('username'), request.form.get('password')):
            # Create the session token
            token = uuid.uuid4()

            # Store the session data in Redis
            R_Server.set(str(token), request.form.get('username').lower())

            # Set the session cookie in the response
            response = redirect('/games/minesweeper')
            response.set_cookie('session', str(token))
            return response
        else:
            return render_template('login.j2', error="Could not register user. Username may already exist.")

    return redirect('/games/minesweeper')

@app.route("/logout", methods=["POST"])
def logout():
    # Get the session token from the request cookies - server-side token
    token = request.cookies.get('session')

    if token is None:
        # No token found, redirect to login page
        return redirect('/login')
    
    # Delete the session data from Redis
    R_Server.delete(token)

    # Delete the session cookie from the response
    response = redirect('/login')
    response.set_cookie('session', '', expires=0)
    
    return response

@app.route("/profile", methods=["GET"])
def profile():
    # Get the session token from the request cookies - server-side token
    token = request.cookies.get('session')

    if token is None:
        # No token found, redirect to login page
        return redirect('/login')
    
    # Yay! the user is logged in and we redirect them to their profile
    user = get_token_data(token)

    if user is None:
        # No user found in redis, redirect to login page
        return redirect('/login')

    profiles = database.get_all_profiles()

    print(profiles)

    return render_template("users.j2", profiles=profiles)

@app.route("/profile/<username>", methods=["GET"])
def profile_username(username):
    # Get the session token from the request cookies - server-side token
    token = request.cookies.get('session')

    if token is None:
        # No token found, redirect to login page
        return redirect('/login')
    
    # Yay! the user is logged in and we redirect them to their profile
    user = get_token_data(token)

    if user is None:
        # No user found in redis, redirect to login page
        return redirect('/login')
    
    profile = database.get_profile(username.lower())
    
    if user == username:
        # The user is trying to access their own profile
        return render_template("profile.j2", ownprofile=True, fname=profile[0], lname=profile[1], avatar=f"/static/avatars/{user}_avatar.png")
    else:
        return render_template("profile.j2", ownprofile=False, fname=profile[0], lname=profile[1], avatar=profile[2])

@app.route("/profile/<username>", methods=["PUT", "DELETE"])
def update_account(username):
    token = request.cookies.get('session')

    if token is None:
        # No token found, redirect to login page
        return jsonify({'status': 401, 'error': 'Unauthenticated', 'data':{}}), 401
    
    # Yay! the user is logged in and we redirect them to their profile
    user = get_token_data(token)

    if user is None:
        # No user found in redis, redirect to login page
        return jsonify({'status': 401, 'error': 'Unauthenticated', 'data':{}}), 401
    
    if user != username:
        # Wrong user!
        return jsonify({'status': 401, 'error': 'Unauthenticated', 'data':{}}), 401

    if request.method == "DELETE":
        # Delete from the database and redis
        database.delete_user(user)
        R_Server.delete(token)
        # respond with the updated session
        resp = make_response()
        resp.set_cookie('session', '', expires=0)
        return resp
    
    # Get the json in the request
    data = request.get_json()
    try:
        if data['action'] == "password":
            if database.update_password(user, data['data']['password']):
                return jsonify({'status': 200, 'data': 'password changed'}), 200
            
            return jsonify({'status': 400, 'error': 'password could not be changed'}), 400
        if data['action'] == "name":
            if database.update_name(user, data['data']['fname'], data['data']['lname']):
                return jsonify({'status': 200, 'data': 'name changed'}), 200
            
            return jsonify({'status': 400, 'error': 'name could not be changed'}), 400
        if data['action'] == "picture":
            # Split up the base64 string into header and data
            header, encoded = data['data']['picture'].split(',', 1)  
            file_ext = header.split('/')[1].split(';')[0] 
            image_binary = base64.b64decode(encoded) # Parse the base64 string

            # ensure the directory exists
            directory = "static/avatars/"
            os.makedirs(directory, exist_ok=True)

            # Save the image to the directory
            file_name = f"{user}_avatar.{file_ext}"
            file_path = os.path.join(directory, file_name)
            with open(file_path, 'wb') as f:
                f.write(image_binary)

            return jsonify({'status': 200, 'data': 'avatar successfully updated'}), 200
    except Exception as e:
        return jsonify({'status': 400, 'error': 'Malformed request', 'data':{}}), 400

app.run(port=8080, debug=True)