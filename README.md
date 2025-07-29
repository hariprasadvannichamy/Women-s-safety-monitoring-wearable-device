# **Next-Gen Smart Wearable Device for Women and Children’s Safety Using Edge AI**
#### The safety of women and children remains a critical concern, especially in emergency situations where conventional solutions fail due to manual dependency and poor connectivity. Existing safety apps and wearables often require user action to maintain a stable Internet, making them unreliable during actual threats. This project introduces a next-generation smart wearable device powered by edge AI that can autonomously detect danger and respond instantly, even in offline environments.The system continuously listens for distress keywords such as ’help’ or ’emergency’ using a lightweight on-device AI model. It also monitors vital signs such as heart rate and SpO2 in real time using the MAX30102 sensor. When a threat is detected through voice or abnormal biometrics—the device automatically sends an emergency alert containing the GPS location to trusted contacts. To overcome network limitations, it uses LoRa for long-distance communication, ZigBee for local mesh networking, and Bluetooth for short-range alerts. Machine learning algorithms personalize response thresholds to reduce false alarms and improve reliability. Field testing confirmed that the device accurately detects emergencies and transmits alerts in seconds,even in rural, low-signal environments. Designed to be compact, affordable, and self-sufficient, this wearable offers a powerful offline safety solution that bridges the technological gap in personal protection for vulnerable communities


## **key Features:**
- 🔊 **Voice-based emergency detection** (e.g., "help", "emergency")
- ❤️ **Real-time heart rate & SpO2 monitoring** using MAX30102
- 📍 **GPS-based location tracking** (Neo-6M)
- 📡 **Offline communication** using:
  - LoRa (long-range)
  - ZigBee (mesh network)
  - Bluetooth (short-range)
- 📲 **GSM fallback** via SIM800L for SMS alerts
- 🔐 **AES-128 encrypted data transmission**
- 🧠 **Edge AI** with on-device CNN for voice recognition (TensorFlow Lite)
- 🛡️ **User privacy protection** and **stealth mode**
- 🔋 Power-efficient design with deep sleep mode (ESP32)
## 🔄 Workflow Diagram

The following block diagram illustrates how the wearable safety device functions — from real-time data collection to emergency alerting using AI and offline communication protocols.

![Workflow Diagram](Data%20Flow%20Diagram%20Whiteboard%20in%20Dark%20Yellow%20Light%20Yellow%20Black%20Monochromatic%20Style%20(4).png)

### 🔍 Workflow Explanation

1. **Input: Voice & Health Metrics**  
   The wearable continuously captures audio (voice commands like "help") and vital signs such as heart rate and SpO₂.

2. **AI Analysis using RISC-V Processor**  
   - Detects distress through **voice pattern recognition**  
   - Identifies abnormalities in **health metrics**  

3. **Emergency Detection**  
   - If an emergency is detected, the system triggers the alert mechanism.  
   - If no emergency is found, the device continues monitoring passively.

4. **Trigger Alert & GPS Fetch**  
   - The device retrieves the user's current location using the **GPS module**.

5. **Send Alert via Communication Modules**  
   - Sends an SMS or alert containing the location via **GSM**, **Wi-Fi**, or **LoRa**, depending on availability.

6. **Log Event & Resume Monitoring**  
   - The alert is logged.
   - The system returns to monitoring state for continuous protection.

## 🧰 Tech Stack

### 🖥️ Hardware Components
- **ESP32** – Dual-core microcontroller with WiFi, Bluetooth, and ESP-NOW
- **MAX30102** – Pulse oximeter and heart rate sensor
- **INMP441** – MEMS microphone for real-time voice input
- **Neo-6M GPS Module** – Geolocation tracking with ~4.5m accuracy
- **LoRa SX1278** – Long-range, low-power communication
- **ZigBee (CC2530)** – Local mesh networking
- **SIM800L GSM Module** – SMS-based communication fallback
- **3.7V Li-ion Battery** – Power supply with onboard charging and protection

### 🧠 AI & Edge ML
- **TensorFlow Lite** – For on-device keyword spotting (CNN model)
- **MFCC (Mel-Frequency Cepstral Coefficients)** – Audio feature extraction for voice recognition
- **Custom CNN** – Lightweight neural network optimized for real-time inference on ESP32
- **Adaptive Thresholding** – Personalized biometric detection

### 💻 Software & Tools
- **Arduino IDE** – Firmware development and sensor integration
- **ESP-IDF** – Low-level development for ESP32
- **C / C++** – Embedded programming
- **Python (for training AI model)** – Model training and dataset preparation
- **Git & GitHub** – Version control and collaboration

### 🔐 Security
- **AES-128 Encryption** – Secure data transmission and storage
- **On-device processing** – Privacy-first design with minimal cloud reliance
- **Two-factor authentication** – For forensic data retrieval

## 🧪 Novelty of the Project

This project introduces a **next-generation safety wearable** that overcomes the key limitations of existing systems through several innovative features:

1. **Offline Functionality Using Edge AI**  
   - Most safety wearables depend on constant internet or GSM connectivity.  
   - Our device functions **completely offline**, using **LoRa**, **ZigBee**, and **on-device AI** for emergency detection and communication.

2. **Multi-Trigger Emergency Detection**  
   - Combines **voice keyword spotting**, **biometric monitoring (SpO₂, heart rate)**, and **manual SOS** into a unified emergency response system.

3. **Lightweight CNN Deployed on ESP32**  
   - A custom-trained **TensorFlow Lite CNN model** runs directly on the microcontroller, ensuring **real-time detection** without relying on cloud computation.

4. **Hybrid Communication Architecture**  
   - Uses **LoRa (long-range)**, **ZigBee (mesh)**, **Bluetooth**, and **GSM** for adaptive alert delivery based on connectivity availability.

5. **Privacy-First Design**  
   - All processing is done **locally on the device**, with **AES-128 encryption** and **volatile memory storage** to ensure user privacy and GDPR compliance.

6. **Stealth & Forensic Features**  
   - Includes **stealth mode** for discreet SOS activation and **ambient audio recording** (with user consent) to support forensic investigations.

7. **Low Power with Deep Sleep Support**  
   - Power-optimized design using ESP32 deep sleep and **interrupt-driven wake-up**, allowing **18+ hours active use** and **42+ hours standby**.

---

These combined innovations make this wearable device a **truly standalone, intelligent safety platform**, particularly suited for vulnerable populations in **rural or connectivity-limited regions**.

## ✅ Conclusion

The proposed smart wearable device offers a **robust, real-time safety solution** for women and children, particularly in environments with **poor or no network connectivity**. By combining **AI-powered voice and biometric detection**, **offline communication protocols**, and **privacy-first design**, the system ensures that emergency alerts can be triggered **autonomously** — even when the user is unconscious or unable to act manually.

Unlike conventional safety apps or wearables that rely solely on GSM or internet, this device leverages **edge AI**, **LoRa**, **ZigBee**, and **Bluetooth** to deliver **instant, reliable protection**. The integration of lightweight machine learning models, adaptive thresholds, and low-power operation makes it both **efficient** and **scalable** for real-world deployment in underserved areas.

This solution bridges a critical gap in personal safety technology and represents a **next step toward smarter, more accessible protection systems** for vulnerable populations.
