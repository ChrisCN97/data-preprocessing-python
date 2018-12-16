import eel

eel.init("web")

@eel.expose
def hello():
    return "hello"

eel.start("index.html")