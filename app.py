from database import create_table, insert_reading, get_recent_readings
from flask import Flask, request
from sense_hat import SenseHat

app = Flask(__name__)
sense = SenseHat()
create_table()

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

    if not presence_detected:
        focus_score -= 10

    advice = "Excellent study conditions"

    if temp > 30:
        advice = "Room temperature is too high"

    elif humidity > 70:
        advice = "Humidity levels are high"

    elif focus_score < 70:
        advice = "Focus score is low. Consider taking a short break"

    if not presence_detected:
        advice = "No user detected in study area"

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
    insert_reading(temp, humidity, focus_score, presence_text)
    recent_readings = get_recent_readings()

    return f"""
    <meta http-equiv="refresh" content="5">

    <h1>FocusHub Live Dashboard</h1>

    <h2>Environment Readings</h2>
    <p>Temperature: {temp:.1f}°C</p>
    <p>Humidity: {humidity:.1f}%</p>

    <h2>Focus Score: {focus_score}/100</h2>

    <h2>AI Recommendation</h2>
    <p>{advice}</p>

    <h2>Presence Status: {presence_text}</h2>

    <h2>Recent Readings</h2>
    <table border="1">
        <tr>
            <th>Time</th>
            <th>Temperature</th>
            <th>Humidity</th>
            <th>Focus Score</th>
            <th>Presence</th>
        </tr>
        {"".join([f"<tr><td>{row[0]}</td><td>{row[1]:.1f}</td><td>{row[2]:.1f}</td><td>{row[3]}</td><td>{row[4]}</td></tr>" for row in recent_readings])}
    </table>

    <h2>Temperature Chart</h2>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <canvas id="tempChart" width="600" height="250"></canvas>

    <script>
        const labels = {list(reversed([row[0] for row in recent_readings]))};
        const tempData = {list(reversed([row[1] for row in recent_readings]))};
        const humidityData = {list(reversed([row[2] for row in recent_readings]))};
        const focusData = {list(reversed([row[3] for row in recent_readings]))};

        new Chart(document.getElementById('tempChart'), {{
            type: 'line',
            data: {{
                labels: labels,
                datasets: [
                    {{
                        label: 'Temperature',
                        data: tempData
                    }},
                    {{
                        label: 'Humidity',
                        data: humidityData
                    }},
                    {{
                        label: 'Focus Score',
                        data: focusData
                    }}
                ]
            }}
        }});
    </script>
    """

@app.route("/presence")
def presence():
    global presence_detected

    state = request.args.get("state")

    if state == "true":
        presence_detected = True
        print("Packet Tracer presence detected!")
        sense.show_letter("P", text_colour=(0, 255, 0))

    elif state == "false":
        presence_detected = False
        print("Packet Tracer absence detected.")
        sense.show_letter("A", text_colour=(255, 0, 0))

    return "OK"

app.run(host="0.0.0.0", port=5000)
