from twilio.rest import TwilioRestClient 
 
# put your own credentials here 
ACCOUNT_SID = "" 
AUTH_TOKEN = "" 
 
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 
call = client.calls.create(
	to="+98765", 
	from_="+12345", 
	url="http://az1.goza.net:8081",          
) 
 
print call.sid 
