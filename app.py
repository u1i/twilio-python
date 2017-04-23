from flask import Flask, request, redirect
import twilio.twiml
import requests
import urllib
import urllib.request
import uuid
import json

app = Flask(__name__)

callers = {
    "+6538247287": "John",
    "+6551143411": "Jane",
}



def speech2text(blob_url):

	with urllib.request.urlopen(blob_url) as url:
	    blob = url.read()
	
	# Get access token to use the speech services
	url_token_api = 'https://api.cognitive.microsoft.com/sts/v1.0/issueToken' # service address 
	api_key = ''
	
	headers = {'Content-Length': '0', 'Ocp-Apim-Subscription-Key':api_key}
	
	api_response = requests.post(url_token_api, headers=headers)
	
	access_token = str(api_response.content.decode('utf-8'))
	
	
	# Call Speech to text service
	url_stt_api = 'https://speech.platform.bing.com/recognize' # service address 
	
	headers = {'Authorization': 'Bearer {0}'.format(access_token), \
	           'Content-Length': str(len(blob)), \
	           'Content-type': 'audio/wav', \
	           'codec': 'audio/pcm', \
	           'samplerate': '16000'}
	
	params = urllib.parse.urlencode({
	    'scenarios': 'ulm',
	    'appid': 'D4D52672-91D7-4C74-8AD8-42B1D98141A5', # dont change, it is fixed by design
	    'locale': 'en-US', # speech in english
	    'device.os': 'PC',
	    'version': '3.0',
	    'format': 'json', # return value in json
	    'instanceid': str(uuid.uuid1()), # any guid
	    'requestid': str(uuid.uuid1()),
	})
	
	api_response = requests.post(url_stt_api, headers=headers, params=params, data=blob)
	
	res_json = json.loads(api_response.content.decode('utf-8'))

	try:	
		result = str(res_json['results'][0]['lexical'])
		print ("Caller said: " + result)
	except:
		result = 'ERROR'
		print ("no language detected")
	
	# print(json.dumps(res_json, indent=2, sort_keys=True))
	
	#print (result)
	return result

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():

	from_number = request.values.get('From', None)

	resp = twilio.twiml.Response()
	resp.pause()

	if from_number in callers:
		resp.say("Testing Testing. Hello " + callers[from_number])
		print (callers[from_number] + " calling")
	else:
		resp.say("Testing Testing. Hello Stranger!")
		print ("Stranger calling")

	resp.say("Please speak to me, a few sentences only, and I will try to repeat after you.,,, I will need a moment to think. So please talk now, for about ten seconds.")
	resp.record(maxLength="10", action="/handle-recording")

	# resp.play("http://demo.twilio.com/hellomonkey/monkey.mp3")

#	with resp.gather(numDigits=1, action="/handle-key", method="POST") as g:
#		g.say("To hear a lame joke, press 1. For complaints, please call someone else! If you want to give it a go, press 2")
	return str(resp)

@app.route("/handle-key", methods=['GET', 'POST'])
def handle_key():

	digit_pressed = request.values.get('Digits', None)
	if digit_pressed == "2":
		resp = twilio.twiml.Response()
		resp.say("Ok so here's a joke. What do you call a cow with no legs? .Ground Beef.")
		resp.play("https://geekery.blob.core.windows.net/media/haha.wav")
		resp.say("Good bye")
		return str(resp)

	elif digit_pressed == "1":
		resp = twilio.twiml.Response()
		resp.say("Ok sure, please talk now:?")
		resp.record(maxLength="10", action="/handle-recording")
		return str(resp)

	else:
		return redirect("/")

@app.route("/handle-recording", methods=['GET', 'POST'])
def handle_recording():

	recording_url = request.values.get("RecordingUrl", None)
	spoken_text=speech2text(recording_url).replace("XYZ2187623",",")

	resp = twilio.twiml.Response()

	if spoken_text == 'ERROR':
		resp.say("I'm sorry, but I didn't understand anything. Is it noisy where you are? Please speak clearly.")
	else:
		resp.say(",Right, so this is what you said.")
		resp.play(recording_url)
		resp.say(",,now let me try to repeat that:")
		resp.say(spoken_text)


	with resp.gather(numDigits=1, action="/handle-key", method="POST") as g:
		g.say(",..To try one more time, press 1. If you want to hear a lame joke please press 2.")

	return str(resp)

if __name__ == "__main__":
	app.run(debug=True, host='10.0.0.4', port=8081)

