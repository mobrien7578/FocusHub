# FocusHub

FocusHub is an IoT smart study environment monitoring system developed using Raspberry Pi, Flask, Sense HAT, SQLite, and Cisco Packet Tracer.

The project monitors environmental conditions in a study space and provides real-time dashboard updates including temperature, humidity, focus score, and presence detection.

----------------------------

# Features

* Live Flask dashboard
* Real-time temperature monitoring
* Real-time humidity monitoring
* Focus score calculation
* Presence detection using Cisco Packet Tracer
* AI study recommendations
* SQLite database logging
* Raspberry Pi integration
* GitHub version control

---------------------------

# Technologies Used

* Python
* Flask
* Raspberry Pi
* Sense HAT
* SQLite
* HTML/CSS
* Cisco Packet Tracer
* GitHub

----------------------------

# System Architecture

Packet Tracer sensors communicate with the Raspberry Pi using UDP networking.

The Raspberry Pi processes sensor data using Flask and stores readings in a SQLite database. The dashboard displays live study environment information through a web interface.

```text
Packet Tracer
      ↓
UDP Communication
      ↓
Raspberry Pi Flask Application
      ↓
SQLite Database
      ↓
Live Dashboard
```

-----------------------

# Project Structure

```text
FocusHub/
│
├── app.py                 # Main Flask dashboard app
├── database.py            # Stores sensor readings
├── sensor_listener.py     # Receives Packet Tracer data
├── requirements.txt       # Project libraries
├── README.md              # Project information
│
├── templates/
│   └── index.html         # Dashboard webpage
│
├── static/
│   └── style.css          # Dashboard styling
│
├── data/
│   └── focushub.db        # SQLite database
```
-----------------------

# Installation

Clone the repository:

```bash
git clone https://github.com/mobrien7578/FocusHub.git
cd FocusHub
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python3 app.py
```

Open the dashboard in a browser:

```text
http://192.168.0.38:5000
```

------------------

# Dashboard Features

The dashboard displays:

* Temperature readings
* Humidity readings
* Focus score
* Presence status
* AI recommendations
* Recent sensor readings

----------------

# IoT Integration

Cisco Packet Tracer push buttons and motion sensors simulate study room activity.

Sensor data is sent to the Raspberry Pi using UDP and processed by the Flask application in real time.

----------------

# Future Improvements

* MQTT integration
* Camera-based presence detection
* Mobile notifications
* Machine learning focus prediction
* Cloud deployment

------------------

# Author

Michael O'Brien

Student number: 20119095

Computer Systems & Networks Project
