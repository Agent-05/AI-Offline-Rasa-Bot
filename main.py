import importlib
import json
import os
import subprocess
import time
import tkinter as tk

import pyaudio
import requests
from vosk import KaldiRecognizer, Model

# Start Rasa server
subprocess.Popen(["rasa", "shell", "--cors", "*"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# If you have custom actions, start the actions server too
subprocess.Popen(["rasa", "run", "actions"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Give the servers some time to start
time.sleep(5)

# Path to the Vosk model directory
model_path = "vosk-model-en-us-0.22"

# Load the Vosk model
if not os.path.exists(model_path):
    print("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit(1)
print("started loading model")
model = Model(model_path)
print("Done loading model")
# Global flag for controlling continuous listening
is_listening = True

# Function to record audio and transcribe using Vosk
def record_and_transcribe():
    global is_listening
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=4000)
    stream.start_stream()

    recognizer = KaldiRecognizer(model, 16000)
    
    print("Listening...")
    transcription = ""

    while is_listening:
        data = stream.read(4000)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            current_transcription = json.loads(result)["text"]
            transcription += current_transcription

            # Check if "Friday" is spoken
            if "friday" in transcription.lower():
                # Send the full transcription to Rasa
                transcription = transcription[transcription.index("friday") + 6:]
                if len(transcription.strip()) > 0:
                    rasa_response = send_to_rasa(transcription)
                    response_label.config(text="Rasa Response: " + rasa_response)
                    print(rasa_response)
            transcription = ""

    stream.stop_stream()
    stream.close()
    p.terminate()

def send_to_rasa(command):
    url = "http://localhost:5005/webhooks/rest/webhook"  
    headers = {"Content-Type": "application/json"}
    payload = {"sender": "user", "message": command}
    
    print("Sending to Rasa:", payload)  # Debugging
    response = requests.post(url, json=payload, headers=headers)
    
    print("Response Status Code:", response.status_code)  # Debugging
    print("Response Text:", response.text)  # Debugging
    if response.status_code == 200:
        rasa_data = response.json()
        if rasa_data and len(rasa_data) > 0:
            return rasa_data[0].get("text", "No response from Rasa")
    return "Failed to get a response from Rasa"

def submit():
    try:
        input_text = root.inputField.get()  # Change the variable name to avoid shadowing
        rasa_response = send_to_rasa(input_text)
        response_label.config(text="Rasa Response: " + rasa_response)  # Update the response label
    except Exception as e:
        print(f"Error in submit function: {e}")
        response_label.config(text="Error: " + str(e))

def voiceControl():
    global is_listening
    # Start listening in the background
    is_listening = True
    record_button = tk.Button(root, text="Stop Listening", command=stop_listening)
    record_button.pack(pady=20)
    # Run the recording and transcription in a separate thread to avoid blocking the GUI
    from threading import Thread
    listen_thread = Thread(target=record_and_transcribe)
    listen_thread.daemon = True
    listen_thread.start()

def stop_listening():
    global is_listening
    is_listening = False

def textControl():
    voiceControlButton.pack_forget()
    textControlButton.pack_forget()
    root.inputField = tk.Entry(root)
    root.inputField.pack(pady=20)
    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.pack(pady=10)

# Set up the GUI
root = tk.Tk()
root.title("Voice Command App")

root.geometry("400x200")

voiceControlButton = tk.Button(root, text="Voice Control", command=voiceControl)
textControlButton = tk.Button(root, text="Text Control", command=textControl)
voiceControlButton.pack(pady=20)
textControlButton.pack(pady=20)

# Label to display the Rasa response
response_label = tk.Label(root, text="Rasa Response: ")
response_label.pack(pady=20)

# Run the GUI loop
root.mainloop()
