from flask import Flask, request, send_file, redirect, render_template, Response
import redis
import games
import database

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
        return render_template('login.j2')
    
    fields = ['username', 'password', 'mode']
    for field in fields:
        if field not in request.form:
            return "ERROR"
        if len(str(request.form.get(field)).strip()) == 0:
            return "ERROR"
    
    if request.form.get('mode') not in ['login', 'register']:
        return "ERROR"

    print(request.form.get('username'))
    print(request.form.get('password'))
    print('MODE:', str(request.form.get('mode')).upper())
    return redirect('/games/minesweeper')

@app.route("/profile", methods=["GET"])
def profile():
    # # Get the session token from the request cookies - server-side token
    # token = request.cookies.get('session')

    # if token is None:
    #     # No token found, redirect to login page
    #     return redirect('/login')
    
    # # Yay! the user is logged in and we redirect them to their profile
    # user = get_token_data(token)

    # if user is None:
    #     # No user found in redis, redirect to login page
    #     return redirect('/login')

    profiles = database.get_all_profiles()

    print(profiles)

    return render_template("users.j2", profiles=profiles)

app.run(port=8080, debug=True)