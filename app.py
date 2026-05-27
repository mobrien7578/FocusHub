from flask import Flask, request, render_template
from sense_hat import SenseHat
from sensor_listener import SensorListener
from database import create_table, insert_reading, get_recent_readings
import time

app = Flask(__name__)
sense = SenseHat()

create_table()

presence_detected = False
last_presence_time = 0


def calculate_focus_score(temp, humidity, presence):
    score = 100

    if temp > 30:
        score -= 20

    if humidity > 70:
        score -= 10

    if not presence:
        score -= 10

    return max(score, 0)


def get_advice(temp, humidity, focus_score, presence):
    if not presence:
        return "No user detected in the study area."

    if temp > 30:
        return "Room temperature is too high. Consider improving ventilation."

    if humidity > 70:
        return "Humidity is high. Consider opening a window or using ventilation."

    if focus_score < 70:
        return "Focus score is low. Consider adjusting the study environment."

    return "Excellent study conditions."


def handle_packet(data):
    global presence_detected, last_presence_time

    data = data.strip().lower()
    print(f"Packet Tracer says: {data}")

    if "true" in data or '"value":1' in data:
        presence_detected = True
        last_presence_time = time.time()
        print("Presence detected from Packet Tracer.")
        sense.show_letter("P", text_colour=(0, 255, 0))

    elif "false" in data or '"value":0' in data:
        print("False received, keeping presence active briefly.")


listener = SensorListener(port=5001)
listener.callback = handle_packet
listener.start()


@app.route("/")
def home():
    global presence_detected

    if presence_detected and time.time() - last_presence_time > 30:
        presence_detected = False

    temp = sense.get_temperature()
    humidity = sense.get_humidity()

    focus_score = calculate_focus_score(temp, humidity, presence_detected)
    presence_text = "Present" if presence_detected else "Not detected"
    advice = get_advice(temp, humidity, focus_score, presence_detected)

    insert_reading(temp, humidity, focus_score, presence_text)
    recent_readings = get_recent_readings()

    if presence_detected:
        sense.show_letter("P", text_colour=(0, 255, 0))
    elif focus_score >= 80:
        sense.show_letter("G", text_colour=(0, 255, 0))
    elif focus_score >= 50:
        sense.show_letter("O", text_colour=(255, 255, 0))
    else:
        sense.show_letter("B", text_colour=(255, 0, 0))

    labels = list(reversed([row[0] for row in recent_readings]))
    temp_data = list(reversed([row[1] for row in recent_readings]))
    humidity_data = list(reversed([row[2] for row in recent_readings]))
    focus_data = list(reversed([row[3] for row in recent_readings]))

    return render_template(
        "index.html",
        temp=round(temp, 1),
        humidity=round(humidity, 1),
        focus_score=focus_score,
        presence=presence_detected,
        recommendation=advice,
        rows=recent_readings,
        labels=labels,
        temps=temp_data,
        humidities=humidity_data,
        scores=focus_data
    )


@app.route("/presence")
def presence():
    global presence_detected, last_presence_time

    state = request.args.get("state")

    if state == "true":
        presence_detected = True
        last_presence_time = time.time()
        print("Presence detected through Flask API.")
        sense.show_letter("P", text_colour=(0, 255, 0))

    elif state == "false":
        print("False received through Flask API, keeping presence active briefly.")

    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
