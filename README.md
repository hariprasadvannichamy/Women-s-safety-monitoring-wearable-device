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
## **Workflow Diagram**



The diagram below illustrates the flow of data and decisions in the smart wearable safety device — from voice and biometric detection to alert transmission.

![Workflow Diagram](images/workflow.png)

- **Signal Detection & Recognition**: The AI monitors for distress signals, such as keywords or abnormal sounds, and processes the incoming data to identify potential danger.

- **Alert & Location Transmission**: Once a threat is detected, the IoT system triggers real-time alerts with precise location information, immediately sending them to pre-configured emergency contacts or authorities.

- **Response & Support**: Emergency contacts or authorities receive the alert and take action, while the system continues to provide support to ensure timely help in critical situations.


## **Tech Stack**
#### This project leverages a combination of Artificial Intelligence (AI) to detect distress signals, such as specific keywords or abnormal sounds. Internet of Things (IoT) technologies, including sensors like microphones and GPS modules, enable real-time data collection and communication with emergency contacts.
#### Accurate geolocation is provided by GPS modules like the u-blox ZED-F9P, ensuring precise location tracking during emergencies. Embedded systems, such as Raspberry Pi, process the incoming data and run AI algorithms. 
#### Wireless technologies, including GSM, Wi-Fi, and Bluetooth, facilitate the transmission of real-time alerts to predefined emergency contacts. The solution also leverages cloud services (e.g., AWS, Databricks) for scalable data storage, processing, and analytics. 
#### Python and other programming languages are used for developing machine learning models, software algorithms, and system integration. NoSQL and SQL databases store crucial data securely, while encryption and authentication mechanisms ensure data privacy. Additionally, display modules like 16x2 LCDs visually provide alerts and system status to users, creating a comprehensive and efficient system for women’s safety.


## **Novelty**
#### **Novelty** of the Project:

This project stands out by integrating **AI** and **IoT** to create a wearable or software-based solution that not only detects distress situations but also triggers immediate, location-specific alerts to emergency contacts or authorities. Unlike existing safety systems, it goes beyond simple alert mechanisms by using **advanced AI models** to recognize subtle distress signals, such as specific keywords or abnormal sounds, ensuring quick and accurate threat detection. Additionally, the combination of **geolocation tracking** and **real-time communication** sets it apart, offering precise location sharing to facilitate swift response. The **cloud-based** backend enables scalable data management and supports continuous improvement through real-time analytics, making it a future-ready, scalable, and sustainable safety solution. This innovative approach ensures that personal safety is enhanced with cutting-edge technology, offering both empowerment and peace of mind in critical situations.

## **Conclusion of the Solution:**

 #### This women's safety project provides a comprehensive, AI-powered IoT solution designed to proactively detect potential dangers and trigger immediate responses. By combining **artificial intelligence** for signal recognition, **geolocation** for accurate tracking, and **real-time communication**, it delivers a robust and user-centric safety mechanism. The system’s ability to seamlessly integrate advanced technologies ensures continuous monitoring, timely alerts, and effective support, empowering women to take control of their safety in critical situations. Ultimately, this solution not only enhances personal security but also contributes to societal well-being by fostering safer communities through innovation and smart technology.
