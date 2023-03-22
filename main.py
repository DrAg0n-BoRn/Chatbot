import os 
import openai 
import pyaudio
import wave
import pyttsx3


# --- Get Audio ---
# Max recording duration:
DURACION = 8

# Audio Parameters
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1  
fs = 44100  # Record at 44100 samples per second

audio_object = pyaudio.PyAudio()

# Record
stream = audio_object.open(format=sample_format, channels=channels, rate=fs, frames_per_buffer=chunk, input=True)

# Store data in chunks for a few seconds
frames = []
print("RECORDING")
for i in range(0, int(fs / chunk * DURACION)):
    data = stream.read(chunk)
    frames.append(data)

# Stop and close the stream 
print("STOP")
stream.stop_stream()
stream.close()

# Terminate the PortAudio interface
audio_object.terminate()

# Save the recorded data as a WAV file
name = "test"  # input("Filename: ")
filename = os.path.join(os.getcwd(), name + ".wav")

wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(audio_object.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()


# --- Speech to Text ---
openai.api_key = os.getenv('OPENAPIKEY')

with open(filename, "rb") as audio_file:
    transcription_raw = openai.Audio.transcribe(model="whisper-1", file=audio_file)
    
# Parse transcription
transcription: str = transcription_raw.get("text")
print(transcription)


# --- Send text to chatgpt and get completion ---
response_raw = openai.Completion.create(model="text-davinci-003", 
                                        prompt=transcription, 
                                        temperature=0.8, 
                                        max_tokens=90, 
                                        frequency_penalty=0.5,
                                        presence_penalty=0.5
                                        )

'''
RESPONSE EXAMPLE

        <class 'openai.openai_object.OpenAIObject'>

        {
        "choices": [
            {
            "finish_reason": "stop",
            "index": 0,
            "logprobs": null,
            "text": "\n\nI'm feeling great, thanks for asking! And yes, it's looking like it will be a good day."
            }
        ],
        "created": 1679455340,
        "id": "cmpl-6wjLIRoSxuK4wvmEKkGpzqyj01lYH",
        "model": "text-davinci-003",
        "object": "text_completion",
        "usage": {
            "completion_tokens": 25,
            "prompt_tokens": 14,
            "total_tokens": 39
        }
        }
'''

# Parse response
response: str = response_raw.get("choices")[0].get("text").strip()
if not response:
    raise ValueError("Response from ChatGPT is None or empty string")
print(response)

# -- Output response: text to speech ---
engine = pyttsx3.init()

# configure voice rate
engine.setProperty("rate", 180)

# Speak
engine.say(response)
engine.runAndWait()
engine.stop()
