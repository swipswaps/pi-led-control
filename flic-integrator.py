#!/usr/bin/env python3
# This caller relies on https://github.com/50ButtonsEach/fliclib-linux-hci

FLIC_LIB_PATH = "/home/pi/fliclib-linux-hci/clientlib/python/"
PI_LED_HOST = "http://localhost:9000"
FLIC_HOST = "localhost"
import sys
sys.path.append(FLIC_LIB_PATH)
import fliclib
import requests
import json
import time

flicClient = fliclib.FlicClient(FLIC_HOST)
lastHoldPress = 0

def toogleFeed(channel, click_type, was_queued, time_diff=None):
        global lastHoldPress
        try:
                print(str(channel.bd_addr) + " " + str(click_type) + " " + str(was_queued) + " " + str(time_diff))
                if click_type == fliclib.ClickType.ButtonSingleClick:
                        print(str(time.time() - lastHoldPress))
                        if time.time() - lastHoldPress > 2:
                                statusRequestResult = requests.get(PI_LED_HOST + "/getStatus")
                                jsonBody = json.loads(statusRequestResult.text)
                                color = jsonBody["color"]
                                if color == None:
                                        print("feed")
                                        r = requests.post(PI_LED_HOST + "/startProgram", json.dumps({'name': 'feed', 'params': []}))
                                else:
                                        if (color["blue"] == 0 and color["red"] == 0 and color["green"] == 0) or jsonBody["brightness"] < 0.10:
                                                print("feed")
                                                r = requests.post(PI_LED_HOST + "/startProgram", json.dumps({'name': 'feed', 'params': []}))
                                        else:
                                                print("softoff")
                                                r = requests.post(PI_LED_HOST + "/startProgram", json.dumps({'name': 'softOff', 'params': []}))
                if click_type == fliclib.ClickType.ButtonDoubleClick:
                        r = requests.post(PI_LED_HOST + "/startProgram", json.dumps({'name': 'white', 'params': []}))
                if click_type == fliclib.ClickType.ButtonHold:
                        lastHoldPress = time.time()
                        print("new hold: " + str(lastHoldPress))
                        r = requests.post(PI_LED_HOST + "/startProgram", json.dumps({'name': 'randomPath', 'params': []}))
                        
        except:
                print("toggleFeed failed" + traceback.format_exc())
                        
                        
def got_button(bd_addr):
	channel = fliclib.ButtonConnectionChannel(bd_addr)
	channel.on_button_up_or_down = toogleFeed
	channel.on_button_click_or_hold = toogleFeed
	channel.on_button_single_or_double_click = toogleFeed
	channel.on_button_single_or_double_click_or_hold = toogleFeed
	flicClient.add_connection_channel(channel)

def got_info(items):
	print(items)
	for bd_addr in items["bd_addr_of_verified_buttons"]:
		got_button(bd_addr)

flicClient.get_info(got_info)

flicClient.on_new_verified_button = got_button

flicClient.handle_events()