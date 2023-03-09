from threading import Timer

def sayHello():
    print('Hello, World!')

Timer(5.0, sayHello).start()