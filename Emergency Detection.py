import os
import wave
import pyaudio
import librosa
import numpy as np
import tensorflow as tf
from tensorflow.lite.python.interpreter import Interpreter
from twilio.rest import Client
import requests
import serial
import time
from geopy.geocoders import Nominatim
import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import threading
from opencage.geocoder import OpenCageGeocode

# Twilio account credentials
TWILIO_ACCOUNT_SID = "xxxxx"
TWILIO_AUTH_TOKEN = "yyyyy"
TWILIO_PHONE_NUMBER = "+123456789"
TO_PHONE_NUMBER = "00000000000"

# Emergency Trigger: Audio Recording Configuration
AUDIO_FILE_PATH = "emergency_audio.wav"
RECORD_SECONDS = 15  # Recording duration in seconds
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono channel
RATE = 44100  # Sampling rate
CHUNK = 1024  # Chunk size

# Load TensorFlow Lite Model for Audio Classification
interpreter = Interpreter(model_path=r"H:\\Women's safety using ai & iot\\Ai\\audio_classification_model.tflite")
interpreter.allocate_tensors()

# Twilio Client Setup
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# OpenCage API setup
OPENCAGE_API_KEY = '0e993d2166fc4a35b4209e8267341b79'
geocoder = OpenCageGeocode(OPENCAGE_API_KEY)

# Google Maps API setup
GOOGLE_MAPS_API_KEY = "AIzaSyASL1s2L-c4oo1Ltx4WEmZuyTDXNOChsJk"

# Vosk Model Setup
VOSK_MODEL_PATH = r"H:\\Women's safety using ai & iot\\Ai\\vosk-model-en-us-0.42-gigaspeech"
vosk_model = Model(VOSK_MODEL_PATH)  # Load Vosk model
recognizer = KaldiRecognizer(vosk_model, 16000)  # Initialize Kaldi Recognizer

# Geolocation Setup
geolocator = Nominatim(user_agent="emergency_helper")

# Record Audio with dynamic length based on detected keyword
def record_audio_dynamic(record_seconds=RECORD_SECONDS):
    print(f"Recording emergency audio for {record_seconds} seconds...")
    audio = pyaudio.PyAudio()

    # Open audio stream
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    frames = []
    for _ in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    # Close stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save recorded audio to a file
    with wave.open(AUDIO_FILE_PATH, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Audio recorded: {AUDIO_FILE_PATH}")
    return AUDIO_FILE_PATH

# Get Location Details from GPS
def get_gps_location():
    gps_port = "/dev/ttyS0"  # Change to your GPS serial port
    ser = serial.Serial(gps_port, baudrate=9600, timeout=1)

    while True:
        data = ser.readline()
        if data.startswith(b"$GPGGA"):
            try:
                parts = data.decode().split(',')
                latitude = float(parts[2]) / 100
                longitude = float(parts[4]) / 100
                return latitude, longitude
            except Exception as e:
                print("Error parsing GPS data:", e)
        time.sleep(1)

# Get IP-based Location
def get_ip_location():
    try:
        response = requests.get("http://ipinfo.io")
        data = response.json()
        loc = data["loc"].split(",")
        latitude, longitude = float(loc[0]), float(loc[1])
        return latitude, longitude
    except Exception as e:
        print("Error fetching location:", e)
        return None, None

# Try to get real-time location
def get_location():
    print("Fetching device location...")

    # Try GPS first
    try:
        latitude, longitude = get_gps_location()
        if latitude and longitude:
            return latitude, longitude
    except Exception:
        print("GPS not available, using IP-based location.")

    # Fallback to IP-based geolocation
    latitude, longitude = get_ip_location()

    if latitude and longitude:
        return latitude, longitude
    else:
        raise Exception("Unable to retrieve location.")

# Send Emergency SMS via Twilio
def send_emergency_sms(location, audio_file_path):
    print("Sending emergency SMS...")
    map_link = f"https://www.google.com/maps?q={location[0]},{location[1]}"
    message_body = f"Emergency detected! Location: {map_link}. Audio file is saved locally at {audio_file_path}."

    message = client.messages.create(
        body=message_body,
        from_=TWILIO_PHONE_NUMBER,
        to=TO_PHONE_NUMBER
    )
    print("Emergency SMS sent successfully!")
    return message.sid

# Preprocess the audio dynamically based on length and extract features
def preprocess_audio_dynamic(audio_file):
    audio, sr = librosa.load(audio_file, sr=None)
    duration = librosa.get_duration(y=audio, sr=sr)
    n_mfcc = min(max(13, 20 if duration < 20 else 50), 50)

    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc).T
    mfcc_flattened = mfcc.flatten()

    target_length = 50
    current_length = len(mfcc_flattened)
    if current_length < target_length:
        mfcc_flattened = np.pad(mfcc_flattened, (0, target_length - current_length))
    else:
        mfcc_flattened = mfcc_flattened[:target_length]

    print(f"MFCC shape: {mfcc.shape}, flattened length: {len(mfcc_flattened)}")
    return np.expand_dims(mfcc_flattened, axis=0).astype(np.float32)

# Predict if an emergency exists based on the audio features
def predict_audio_features_dynamic(features):
    print("Predicting emergency based on audio features...")
    interpreter.set_tensor(interpreter.get_input_details()[0]['index'], features)
    interpreter.invoke()
    output_data = interpreter.get_tensor(interpreter.get_output_details()[0]['index'])

    if output_data > 0.5:
        print("Emergency detected!")
        return True
    elif output_data > 0.3:
        print("Possible emergency detected, monitoring further.")
        return False
    else:
        print("No emergency detected.")
        return False

# Helper function to detect emergency keywords with negation handling
def is_emergency_detected(detected_text):
    detected_text = detected_text.lower()
    words = detected_text.split()
    
    negation_words = {"not", "no", "don't", "doesn't", "isn't", "aren't", "wasn't", "won't", "can't"}
    emergency_keywords = {"help", "emergency"}

    for i, word in enumerate(words):
        if word in emergency_keywords:
            # Check for negation within the last two words
            negation_window = words[max(0, i - 2):i]
            if any(neg_word in negation_window for neg_word in negation_words):
                print(f"Negated keyword detected in: {' '.join(negation_window)} {word}")
                return False
            return True
    return False

# Main function to handle keyword detection, emergency classification, and SMS alerts
def main():
    print("Listening for emergency keyword...")
    while True:
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            try:
                # Capture audio input
                audio_data = recognizer.listen(source)
                detected_text = recognizer.recognize_google(audio_data)
                print(f"You said: {detected_text}")

                # Check if an emergency keyword is detected
                if is_emergency_detected(detected_text):
                    print("Emergency keyword detected!")

                    # Record emergency audio
                    audio_file = record_audio_dynamic(RECORD_SECONDS)

                    # Process audio and predict emergency
                    features = preprocess_audio_dynamic(audio_file)
                    emergency_detected = predict_audio_features_dynamic(features)

                    # Handle emergency
                    if emergency_detected:
                        location = get_location()
                        if location:
                            send_emergency_sms(location, audio_file)
                        else:
                            print("Unable to determine location.")
                    else:
                        print("No emergency detected based on audio features.")
                else:
                    print("No emergency keyword detected or it was negated. Listening again...")

            except sr.UnknownValueError:
                print("Could not understand the audio. Please try again.")
            except sr.RequestError as e:
                print(f"Error with speech recognition: {e}")
            except Exception as e:
                print(f"Unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
