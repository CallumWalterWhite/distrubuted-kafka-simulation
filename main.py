from flask import Flask, render_template
import paho.mqtt.client as mqtt
from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
    posts = [{
        'title': 'hello kit',
        'created': 'BLAHH'
    },{
        'title': 'super mario speed run',
        'created': 'UNDER 2mins!'
    }]
    return render_template('index.html', posts=posts)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def createClient():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("mqtt.eclipseprojects.io", 80, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()

t = Thread(target=createClient)
t.start()
app.run()