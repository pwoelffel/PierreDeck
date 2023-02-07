from serial import Serial
from pynput.keyboard import Key, Controller, KeyCode
import simpleobsws
import asyncio
import json
from time import sleep
from random import randint

def hex_to_dec(hex):
    return int(hex, 16)

def stopMedias():
    medias: simpleobsws.RequestResponse = loop.run_until_complete(obs.call(simpleobsws.Request("GetInputList", {"inputKind": "ffmpeg_source"})))
    for video in medias.responseData["inputs"]:
        mediaData: simpleobsws.RequestResponse = loop.run_until_complete(obs.call(simpleobsws.Request("GetMediaInputStatus", {"inputName": video["inputName"]})))
        if (mediaData.responseData["mediaDuration"] == "OBS_MEDIA_STATE_PLAYING"):
            loop.run_until_complete(obs.call(simpleobsws.Request("TriggerMediaInput", {"inputName": video["sourceName"], "mediaAction": "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_RESTART"})))

def incrementCounter():
    try:
        with open('compteur.txt', 'r') as file:
            text = file.read()
            counterIncr = int(text) + 1
    except:
        print('Erreur à la lecture du fichier')
    try:
        with open('compteur.txt', 'w') as file:
            file.write(str(counterIncr))
    except:
        print('Erreur à l\'écriture du compteur')

def toggleSource(scene, source):
    sourceState = loop.run_until_complete(obs.call(simpleobsws.Request("GetSceneItemProperties", {"scene-name": scene, "item": {"name": source}})))
    loop.run_until_complete(obs.call(simpleobsws.Request("SetSceneItemRender", {"scene-name": scene, "source": source, "render": not sourceState['visible']})))

def parseInput(message):
    try:
        messageJson = json.loads(message)
        return messageJson
    except:
        return message

async def connectObs(obs: simpleobsws.WebSocketClient):
    await obs.connect()
    await obs.wait_until_identified()

text: str
try:
    with open('PierreDeck.json') as file:
        text = file.read()
        jsonFunctions = json.loads(text)
except:
    print('Erreur à la lecture du fichier')
    exit()

obs = simpleobsws.WebSocketClient(password="")

loop = asyncio.get_event_loop()
try :
    loop.run_until_complete(connectObs(obs))
    if (obs.identified):
        print("Connected succefully")
    else :
        print("Connection failed")
except:
    obsConnection = False
    print('Pas de connexion OBS')

keyboard = Controller()
ser = Serial('COM3', 9600)

print(loop.run_until_complete(obs.call(simpleobsws.Request("GetInputList", {"inputKind": "ffmpeg_source"}))))

while (1):
    message = ser.readline().decode().strip()
    input = parseInput(message)
    if (input == "Mute"):
        print("Mute")
        #print(loop.run_until_complete(obs.call("GetSceneItemProperties", {"scene-name": "Discussion", "item": {"name": "nome"}})))
        keyboard.tap(Key.f13)
    else:
        pageInt = hex_to_dec(input['page'])
        actionInt = hex_to_dec(input['action'])
        for i in range(len(jsonFunctions[pageInt][actionInt])):
            if (jsonFunctions[pageInt][actionInt][i]['action'] == "obs"):
                print(jsonFunctions[pageInt][actionInt][i]['arg'])
                loop.run_until_complete(obs.call(simpleobsws.Request(jsonFunctions[pageInt][actionInt][i]['call'], jsonFunctions[pageInt][actionInt][i]['arg'])))
            elif (jsonFunctions[pageInt][actionInt][i]['action'] == "function"):
                print(jsonFunctions[pageInt][actionInt][i]['function'])
                exec(jsonFunctions[pageInt][actionInt][i]['function'])
loop.close()