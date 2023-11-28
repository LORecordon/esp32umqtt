import ubinascii
import machine
from umqtt.simple import MQTTClient
import network
import time
import _thread
import ujson

from locker import Locker
from station import Station
print("Starting Program")

# Create lockers
l1 = Locker("3", 10, 20, 30, 13, 21, 25, 22, True)
l2 = Locker("2", 10, 20, 30, 26, 19, 33, 4)
l3 = Locker("1", 10, 20, 30, 27, 18, 32, 23)

# Create station
S1 = Station("G5", [l1, l2, l3])




# Function to connect to Wi-Fi
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.active(True)
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print("Wi-Fi Connected:", wlan.ifconfig())

        

wifi_ssid = "WIFI GRATIS"
wifi_password = "password"
mqtt_broker = "5f065f6ce8da42d1abd6eab15ecdd41f.s2.eu.hivemq.cloud"
mqtt_user = b"esp32"
mqtt_password = b"Abcd1234"

ssl_params = {"server_hostname": mqtt_broker}

# Connect to Wi-Fi
connect_wifi(wifi_ssid, wifi_password)

# Generate a unique client ID
client_id = ubinascii.hexlify(machine.unique_id()).decode()

# Instantiate the MQTTClient object
client = MQTTClient("station", server='5f065f6ce8da42d1abd6eab15ecdd41f.s2.eu.hivemq.cloud', user="esp32", password="Abcd1234",  ssl=True, ssl_params=ssl_params)


#Message "queue"
toRespond = None

# Callback for incoming messages
def on_message(topic, msg):
    global S1, toRespond

    temp = msg.decode('utf-8')
    try:
        temp = ujson.loads(temp)
    except:
        print("Not A Json Message, Recieved:", temp)
        return
    topic = topic.decode('utf-8')
    print("Received message:", temp)
    print(topic == "unloading")
    if topic == "reservation":
        if temp["station_name"] == S1.id:
            print("Reservation message received")
            S1.changeState(str(temp["nickname"]), 1)
    elif topic == "load":
        if temp["station_name"] == S1.id:
            print("Loading message received")
            response = S1.load(str(temp["nickname"]))
            toRespond = response
            
    elif topic == "unload":
        if temp["station_name"] == S1.id:
            print("Unloading message received")
            respone = S1.unload(str(temp["nickname"]))
            toRespond = ujson.dumps(respone)

# Set the on_message callback
client.set_callback(on_message)

# Connect to the MQTT broker
client.connect()
print('connected')
# Subscribe to the desired topic
client.subscribe(b"reservation/#", qos=1)
client.subscribe(b"load/#", qos=1)
client.subscribe(b"unload/#", qos=1)
client.subscribe(b"testing/#", qos=1)



#not used
def constant_messaging(client, station):
    while True:
        time.sleep(5)
        message = station.create_mesagge()
        client.publish("info", str(message), qos=1)




try:
    x = 38
    while True:
        time.sleep(0.5)

        x+=1
        if x >= 40:
            print("Creating and Sending Info Message")
            message = ujson.dumps(S1.create_mesagge())
            client.publish("info", str(message), qos=1)
            x = 0
        #Check for incoming messages
        
        #if toRespond != None:
        #    print("Responding with:", toRespond)
        #    client.publish("response", str(toRespond), qos=1)
        #    toRespond = None
        
        client.check_msg()

except KeyboardInterrupt:
    print("Interrupted")
    client.disconnect()
    _thread.exit()


client.disconnect()
_thread.exit()
    
