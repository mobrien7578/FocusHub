from flask import Flask, request
from sense_hat import SenseHat

app = Flask(__name__)
sense = SenseHat()

presence_detected = False

@app.route("/")
def home():
    global presence_detected

    temp = sense.get_temperature()
    humidity = sense.get_humidity()

    focus_score = 100

    if temp > 30:
        focus_score -= 20

    if humidity > 70:
        focus_score -= 10

    # Sense HAT display
    if presence_detected:
        sense.show_letter("P", text_colour=(0, 255, 0))
    else:
        if focus_score >= 80:
            sense.show_letter("G", text_colour=(0, 255, 0))
        elif focus_score >= 50:
            sense.show_letter("O", text_colour=(255, 255, 0))
        else:
            sense.show_letter("B", text_colour=(255, 0, 0))

    presence_text = "Present" if presence_detected else "Not detected"

    return f"""
    <meta http-equiv="refresh" content="5">

    <h1>FocusHub Live Dashboard</h1>

    <h2>Environment Readings</h2>

    <p>Temperature: {temp:.1f}°C</p>
    <p>Humidity: {humidity:.1f}%</p>

    <h2>Focus Score: {focus_score}/100</h2>

    <h2>Presence Status: {presence_text}</h2>
    """

@app.route("/presence")
def presence():
    global presence_detected

    state = request.args.get("state")

    if state == "true":
        presence_detected = True
        print("Packet Tracer presence detected!")

    else:
        presence_detected = False
        print("Presence cleared")

    return "OK"

app.run(host="0.0.0.0", port=5000)
