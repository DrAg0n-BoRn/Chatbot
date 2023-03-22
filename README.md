# Speech to Speech Chatbot using OpenAI API

## Step 1: Record Speech

A 'wav' audio file is created by using the library "pyaudio", which records the user's voice input.

## Step 2: Speech to Text

The audio file is transcribed and stored as a string. This is done by using the "whisper" model of OpenAI.

## Step 3: Text completion model

The transcribed text string is then sent to OpenAI, this time using its "davinci" model. Obtaining a response in JSON format.

## Step 4: Text to Speech

The response text is transformed to speech using the "pyttsx3" library.
