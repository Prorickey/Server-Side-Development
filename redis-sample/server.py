from flask import Flask, send_file, Response, request
import redis

db = redis.StrictRedis()
try:
    db.ping()
except:
    print("ERROR: Redis unavailable")
    db = None

app = Flask(__name__)

@app.route("/stream")
def stream():
    def emitter():
        count = 0
        pubsub = db.pubsub()
        pubsub.subscribe("chat")

        for message in pubsub.listen():
            message = message["data"]
            if type(message) == bytes:
                yield f"data: {count} {message.decode()}\n\n"
                count += 1

    return Response(emitter(), mimetype="text/event-stream")
    
@app.route("/chat")
def chat():
    return send_file('chat.html')

@app.route("/chat", methods=["POST"])
def message():
    message = request.form.get("message")
    db.publish("chat", message)
    return send_file("chat.html")

app.run(port=3000)