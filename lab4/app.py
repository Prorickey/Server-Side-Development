from flask import Flask, request, send_file, redirect, render_template
import redis
import games

app = Flask(__name__)

# Register all available games
for game in games.games:
    blueprint = games.games[game].blueprint()
    app.register_blueprint(blueprint, url_prefix=f'/{game}')

# Connect to Redis
R_Server = redis.StrictRedis()
try:
    R_Server.ping()
except:
    print("REDIS: Not Running -- No Streams Available")
    R_Server = None

@app.route("/")
def index():
    return "Hello"

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
    return render_template("profile.j2")

app.run(port=8080, debug=True)