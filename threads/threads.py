from threading import Thread, Lock

num = 0
lock = Lock()

def func():
    global num

    lock.acquire()
    num += 1
    print("NUM: ", num)
    lock.release()

for _ in range(100):
        Thread(target=func).start()
