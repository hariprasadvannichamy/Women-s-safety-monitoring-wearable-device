import os
import wave
import pyaudio
import librosa
import numpy as np
import tensorflow as tf
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
TWILIO_ACCOUNT_SID = "xxx"
TWILIO_AUTH_TOKEN = "abc"
TWILIO_PHONE_NUMBER = "123456789"
TO_PHONE_NUMBER = "+91 1234567890"

# Emergency Trigger: Audio Recording Configuration
AUDIO_FILE_PATH = "emergency_audio.wav"
RECORD_SECONDS = 15  # Updated recording duration to 15 seconds
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono channel
RATE = 44100  # Sampling rate
CHUNK = 1024  # Chunk size

# Load TensorFlow Lite model
from tensorflow.lite.python.interpreter import Interpreter

interpreter = Interpreter(model_path=r"H:\Women's safety using ai & iot\Ai\audio_classification_model.tflite")
interpreter.allocate_tensors()

# Twilio Client Setup
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Vosk Model Setup (path updated to the correct one)
VOSK_MODEL_PATH = r"H:\Women's safety using ai & iot\Ai\vosk-model-en-us-0.42-gigaspeech"
vosk_model = Model(VOSK_MODEL_PATH)  # Load Vosk model
recognizer = KaldiRecognizer(vosk_model, 16000)  # Initialize Kaldi Recognizer

# Geolocation Setup
geolocator = Nominatim(user_agent="emergency_helper")

# OpenCage API setup
OPENCAGE_API_KEY = '0e993d2166fc4a35b4209e8267341b79'  # Replace with your OpenCage API key
geocoder = OpenCageGeocode(OPENCAGE_API_KEY)

# Record Audio with dynamic length based on detected keyword
def record_audio_dynamic(record_seconds=RECORD_SECONDS):
    print(f"Recording emergency audio for {record_seconds} seconds...")
    audio = pyaudio.PyAudio()

    # Open audio stream manually, no context manager
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    frames = []
    for _ in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    # Close stream manually
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
    gps_port = "COM5"  # Change to your GPS serial port (e.g., /dev/ttyUSB0 on Raspberry Pi)
    ser = serial.Serial(gps_port, baudrate=115200, timeout=1)

    # Wait for GPS data
    while True:
        data = ser.readline()
        if data.startswith(b"$GPGGA"):
            try:
                # Parse the NMEA sentence to extract latitude and longitude
                parts = data.decode().split(',')
                latitude = float(parts[2])/100
                longitude = float(parts[4])/100
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

# Get location from OpenCage using latitude and longitude
def get_location_from_opencage(latitude, longitude):
    query = f"{latitude}, {longitude}"
    results = geocoder.reverse_geocode(latitude, longitude)

    if results:
        # Extract detailed location info
        location = results[0]['components']
        print(f"Location details: {location}")
        formatted_location = f"{location.get('road', '')}, {location.get('city', '')}, {location.get('country', '')}"
        return formatted_location
    else:
        print("No location found")
        return None

# Try to get real-time location
def get_location():
    print("Fetching device location...")

    # Try GPS first
    try:
        latitude, longitude = get_gps_location()  # If using a GPS module, call this
        if latitude and longitude:
            return latitude, longitude
    except Exception:
        print("GPS not available, using IP-based location.")

    # Fallback to IP-based geolocation if GPS is not available
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
    # Load the audio file
    audio, sr = librosa.load(audio_file, sr=None)
    
    # Adjust the number of MFCCs based on the length of the audio
    duration = librosa.get_duration(y=audio, sr=sr)
    if duration < 5:
        n_mfcc = 13  # Use fewer coefficients for short audio
    elif duration < 20:
        n_mfcc = 20  # Use more coefficients for medium-length audio
    else:
        n_mfcc = 50  # Use the maximum for long audio
    
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
    mfcc = mfcc.T  # Shape it to (time_frames, n_mfcc)

    # Flatten the MFCC features into a 1D array
    mfcc_flattened = mfcc.flatten()

    # Ensure the input size is consistent with the model input
    if len(mfcc_flattened) > 50:  # If it's too long, slice it
        mfcc_flattened = mfcc_flattened[:50]
    elif len(mfcc_flattened) < 50:  # If it's too short, pad it
        mfcc_flattened = np.pad(mfcc_flattened, (0, 50 - len(mfcc_flattened)))

    # Reshape for model input (1, n_features) format
    mfcc_flattened = np.expand_dims(mfcc_flattened, axis=0)

    # Ensure the features are of type FLOAT32
    mfcc_flattened = mfcc_flattened.astype(np.float32)
    
    return mfcc_flattened

# Predict if an emergency exists based on the audio features
def predict_audio_features_dynamic(features):
    print("Predicting emergency based on audio features...")
    interpreter.set_tensor(interpreter.get_input_details()[0]['index'], features)
    interpreter.invoke()
    
    output_data = interpreter.get_tensor(interpreter.get_output_details()[0]['index'])
    
    # Adjust prediction threshold dynamically
    if output_data > 0.5:
        print("Emergency detected!")
        return True
    elif output_data > 0.3:
        print("Possible emergency detected, monitoring further.")
        return False
    else:
        print("No emergency detected.")
        return False

# Threaded Audio Recording Function
def record_audio_threaded(record_seconds=RECORD_SECONDS):
    audio_file = record_audio_dynamic(record_seconds)
    return audio_file

# Threaded Audio Processing Function
def process_audio_threaded(audio_file):
    features = preprocess_audio_dynamic(audio_file)
    return features

# Threaded Prediction Function
def predict_audio_threaded(features):
    emergency_detected = predict_audio_features_dynamic(features)
    return emergency_detected

# Threaded Location Retrieval Function
def get_location_threaded():
    location = get_location()
    return location

# Threaded SMS Sending Function
def send_sms_threaded(location, audio_file):
    send_emergency_sms(location, audio_file)

# Main Function to Detect Keywords and Trigger Emergency
def main():
    print("Listening for emergency keyword...")
    while True:
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()  # Use the speech_recognition.Recognizer here for ambient noise adjustment
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio_data = recognizer.listen(source)

            try:
                # Now use Vosk for speech recognition
                detected_text = recognizer.recognize_google(audio_data)
                print(f"You said: {detected_text}")

                # Check for 'help' or 'emergency'
                if "help" in detected_text.lower() or "emergency" in detected_text.lower():
                    print("Emergency keyword detected!")

                    # Record audio dynamically based on keyword detection
                    audio_file = record_audio_threaded(record_seconds=15)  # Updated the recording time to 15 seconds

                    # Preprocess the audio to extract features
                    features = process_audio_threaded(audio_file)

                    # Predict if the emergency is detected based on the audio features
                    emergency_detected = predict_audio_threaded(features)

                    if emergency_detected:
                        # Get location (either GPS or fallback geolocation)
                        location = get_location_threaded()

                        if location and None not in location:
                            # Send SMS with the location and audio file
                            send_sms_threaded(location, audio_file)
                    else:
                        print("No emergency detected based on audio features.")
                else:
                    print("No emergency keyword detected. Listening again...")

            except sr.UnknownValueError:
                print("Could not understand the audio. Please try again.")
            except sr.RequestError as e:
                print(f"Error with speech recognition: {e}")

if __name__ == "__main__":
    main()