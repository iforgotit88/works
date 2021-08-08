import flask
app = flask.Flask(__name__)
import main 
import mymcs


@app.route("/plant/<plantName>")
def getPlant(plantName):
    info = main.webScrap(plantName = plantName)
    return info
    #return plantName

@app.route("/")
def home():
    return "hello"


@app.route("/rain")
def getRain():
    return mymcs.getRain()


if __name__ == "__main__":
    app.debug = False 
    app.run(host = "0.0.0.0")
