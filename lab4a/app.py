import redis 

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

if r.ping():
    print("Redis is available")
else: 
    print("Redis is unavailable")
    exit(1)

r.set("panda", "bamboo")
r.set("eel", "seaweed")
r.set("maki", 12)
r.set(7, "banana")
r.set(10, 4)
r.rpush("animals", "panda", "lemming", "sheep")
r.hset("user1", mapping={
    'name': 'Sea',
    'age': 3542,
    'birthday': '1/32/-1500'
})

print(r.get("panda"))
print(r.get("eel"))
print(r.get("maki"))
print(r.get(7))
print(r.get(10))
print(r.lrange("animals", 0, -1))
print(r.hgetall("user1"))
        