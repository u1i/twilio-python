# Twilio Python Samples & Demos

[Twilio](http://www.twilio.com) lets users interact with your application using phone calls and SMS text messages. The API documentation is excellent and provides code samples in various languages.

This set of Python code pieces is what I was using to explore the Twilio service.

## [sms.py](sms.py)

sends a text message (SMS), please replace the `from_:` number which a Twilio number that you own. Also make sure that the country of the `to:` number is in your list of approved countries to send messages to.

## [make_call.py](make_call.py)
calls a number and executes the Twiml app or Twiml bin that you specify in the `url`.

## [app.py](app.py)
is a Twiml app that can receive calls, identifies callers based on the number they are calling from, and attempts to repeat what the caller is saying, using speech-to-text analysis. It also shows the 'press 1 for x, press 2 for y' capabilities.
