Women's Safety Monitoring Wearable Device  

## What’s This About?  
Imagine having a companion that’s always there for you, especially in times of need. Our Women's Safety Monitoring Wearable Device is built with AI to provide peace of mind and a helping hand when it matters the most.  

This device listens for distress, detects emergencies, and instantly alerts your trusted contacts with your location and context. It’s like a smart, wearable safety net.  

## What Makes It Special?  
- Voice-Triggered Alerts: Just say "help" or "emergency," and the device gets to work.  
- Smart Audio Analysis: AI detects abnormal sounds and keywords to identify danger.  
- Location Tracking: Real-time GPS coordinates with detailed addresses.  
- Instant Alerts: Sends emergency SMS with your details to your chosen contacts.  
- Wearable Convenience: Fits into your daily life like a smartwatch.  

##  What’s Inside?  
### Software:  
- *AI Intelligence*: Powered by TensorFlow Lite for quick and accurate audio classification.  
- *Real-Time Communication*: Using Twilio for SMS and OpenCage for geocoding.  
- *Speech Recognition*: Vosk helps the device understand what’s being said.  

### Hardware:  
- *ESP32 Microcontroller*: Heart of the device, connecting everything together.  
- *GPS Module*: Pinpoints your exact location.  
- *Microphone**: High-sensitivity mic for clear audio detection.  
- *Display Screen**: Shows alerts, statuses, and updates at a glance.  

## How to Get Started?  
### Requirements:  
- A computer with Python 3.x installed.  
- An ESP32 microcontroller.  
- A GPS module and microphone.  
- Twilio and OpenCage API keys.  

### Steps to Set It Up:  
1. **Clone the Project**:  
   ```bash  
   git clone https://github.com/YourUsername/Women-s-safety-monitoring-wearable-device.git  
   cd Women-s-safety-monitoring-wearable-device  
   ```  

2. **Install Dependencies**:  
   ```bash  
   pip install -r requirements.txt  
   ```  

3. **Upload Firmware to ESP32**:  
   - Open the firmware file in Arduino IDE.  
   - Connect your ESP32 and flash the code.  

4. **Run the Emergency Detection Script**:  
   ```bash  
   python src/main.py  
   ```  

---

## 📖 How It Works  
1. **Listening Mode**: The device is always on alert, listening for specific keywords or unusual sounds.  
2. **AI Analysis**: Audio is analyzed in real-time to identify emergencies.  
3. **Location Tracking**: It fetches your GPS coordinates or estimates location via IP.  
4. **Alert Dispatch**: Sends an SMS with your location and context to your emergency contacts.  

---

## ❤️ Why We Built This  
Safety is a basic human right, and technology should make it easier to feel secure. This project is our way of contributing to a world where women feel safer and more empowered, no matter where they are.  

---

## 🤝 Want to Help?  
We’d love to see your contributions! Here’s how you can get involved:  
1. **Fork** this repository.  
2. Make your changes and **commit** them.  
3. Open a **pull request**, and let’s make this even better together.  

---

## 🔗 Useful Links  
- **Twilio**: [https://www.twilio.com](https://www.twilio.com)  
- **OpenCage**: [https://opencagedata.com](https://opencagedata.com)  
- **Vosk Speech Recognition**: [https://alphacephei.com/vosk](https://alphacephei.com/vosk)  

---

## 📬 Contact Us  
If you have any questions or want to collaborate, feel free to reach out:  
- **Email**: your_email@example.com  
- **GitHub Issues**: [Submit an Issue](https://github.com/YourUsername/Women-s-safety-monitoring-wearable-device/issues)  

---  

This version excludes IoT references while keeping the AI focus intact. Let me know if there’s anything else to tweak!
