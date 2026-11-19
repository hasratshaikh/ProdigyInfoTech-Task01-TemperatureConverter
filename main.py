
"""
PRODIGY INFOTECH
Software Development Internship
Task 01: Temperature Conversion Program

Web Application built using Python and Flask.
"""

from flask import Flask, request, jsonify, render_template_string
import math

app = Flask(__name__)

# ---------------- TEMPERATURE LOGIC ----------------

def convert_temperature(value, unit):

    if unit == "C":
        celsius = value
        fahrenheit = (value * 9 / 5) + 32
        kelvin = value + 273.15

    elif unit == "F":
        celsius = (value - 32) * 5 / 9
        fahrenheit = value
        kelvin = celsius + 273.15

    elif unit == "K":
        celsius = value - 273.15
        fahrenheit = (celsius * 9 / 5) + 32
        kelvin = value

    else:
        raise ValueError("Invalid temperature unit.")

    return {
        "Celsius": round(celsius, 2),
        "Fahrenheit": round(fahrenheit, 2),
        "Kelvin": round(kelvin, 2)
    }


def validate_temperature(value, unit):

    absolute_zero = {
        "C": -273.15,
        "F": -459.67,
        "K": 0
    }

    if unit not in absolute_zero:
        return "Please select a valid temperature unit."

    if not math.isfinite(value):
        return "Please enter a valid finite number."

    if value < absolute_zero[unit]:
        return "Temperature cannot be below absolute zero."

    return None


# ---------------- WEBPAGE DESIGN ----------------

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Tempora - Temperature Converter</title>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            min-height: 100vh;
            font-family: Arial, sans-serif;
            background:
                radial-gradient(circle at 10% 10%, #263c78 0%, transparent 35%),
                radial-gradient(circle at 90% 90%, #292060 0%, transparent 35%),
                #090e20;
            color: #ffffff;
            padding: 35px 20px;
        }

        .container {
            max-width: 1050px;
            margin: auto;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 65px;
            gap: 15px;
        }

        .logo {
            font-size: 25px;
            font-weight: 800;
            letter-spacing: -1px;
        }

        .logo span {
            color: #65a8ff;
        }

        .tag {
            color: #a8b8d6;
            border: 1px solid #35466b;
            padding: 9px 15px;
            border-radius: 30px;
            font-size: 12px;
        }

        .hero {
            text-align: center;
            margin-bottom: 40px;
        }

        .hero-label {
            color: #71b4ff;
            font-size: 12px;
            font-weight: bold;
            letter-spacing: 3px;
            margin-bottom: 20px;
        }

        h1 {
            font-size: clamp(35px, 6vw, 60px);
            letter-spacing: -2px;
            margin-bottom: 16px;
        }

        .hero p {
            color: #a8b5d0;
            font-size: 15px;
            line-height: 1.7;
        }

        .converter {
            max-width: 750px;
            margin: auto;
            padding: 35px;
            background: rgba(24, 35, 65, 0.85);
            border: 1px solid #33466c;
            border-radius: 24px;
            box-shadow: 0 25px 80px rgba(0,0,0,0.3);
        }

        .form-label {
            display: block;
            font-size: 13px;
            color: #c2cee2;
            margin-bottom: 12px;
            font-weight: 600;
        }

        .input-group {
            display: grid;
            grid-template-columns: 1fr 150px;
            gap: 12px;
        }

        input, select {
            width: 100%;
            padding: 17px;
            border: 1px solid #43577d;
            border-radius: 12px;
            background: #111d37;
            color: white;
            font-size: 16px;
            outline: none;
        }

        input:focus, select:focus {
            border-color: #65a8ff;
        }

        button {
            width: 100%;
            padding: 17px;
            margin-top: 20px;
            border: none;
            border-radius: 12px;
            background: linear-gradient(100deg, #3989f5, #7465ed);
            color: white;
            font-size: 15px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.2s;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(57,137,245,0.25);
        }

        .message {
            margin-top: 16px;
            font-size: 13px;
            text-align: center;
            color: #ff8585;
            min-height: 18px;
        }

        .results {
            margin-top: 35px;
            display: none;
            animation: appear 0.4s ease;
        }

        .results h2 {
            font-size: 20px;
            margin-bottom: 18px;
        }

        .result-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 13px;
        }

        .result-card {
            background: #111d37;
            border: 1px solid #354a72;
            padding: 23px 15px;
            border-radius: 16px;
            text-align: center;
        }

        .result-card .unit {
            color: #8da4cb;
            font-size: 12px;
            margin-bottom: 15px;
        }

        .result-card .value {
            font-size: clamp(20px, 3vw, 29px);
            font-weight: bold;
            color: #72b2ff;
            overflow-wrap: anywhere;
        }

        .result-card .symbol {
            color: #9aabc8;
            font-size: 13px;
            margin-top: 8px;
        }

        .result-actions {
            display: flex;
            gap: 10px;
        }

        .secondary-btn {
            background: #25375b;
            border: 1px solid #40577f;
        }

        .secondary-btn:hover {
            background: #30466f;
            box-shadow: none;
        }

        .features {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 55px;
        }

        .feature {
            text-align: center;
            padding: 20px 12px;
            border: 1px solid #293b60;
            border-radius: 15px;
            background: rgba(25, 39, 72, 0.55);
        }

        .feature .icon {
            font-size: 25px;
            margin-bottom: 12px;
        }

        .feature h3 {
            font-size: 13px;
            margin-bottom: 7px;
        }

        .feature p {
            font-size: 11px;
            color: #96a8c9;
            line-height: 1.6;
        }

        footer {
            text-align: center;
            margin-top: 55px;
            color: #8293b2;
            font-size: 12px;
            line-height: 1.8;
        }

        @keyframes appear {
            from {
                opacity: 0;
                transform: translateY(12px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @media(max-width: 600px) {
            body {
                padding: 25px 15px;
            }

            header {
                margin-bottom: 45px;
            }

            .converter {
                padding: 22px 16px;
            }

            .input-group {
                grid-template-columns: 1fr;
            }

            .result-grid {
                grid-template-columns: 1fr;
            }

            .features {
                grid-template-columns: 1fr;
            }

            .tag {
                font-size: 10px;
            }
        }
    </style>
</head>

<body>

<div class="container">

    <header>
        <div class="logo">TEMP<span>ORA.</span></div>
        <div class="tag">PYTHON POWERED APPLICATION</div>
    </header>

    <section class="hero">
        <div class="hero-label">SMART TEMPERATURE CONVERSION</div>

        <h1>Temperature <span style="color:#69aaff">Converter.</span></h1>

        <p>
            Convert temperatures between Celsius, Fahrenheit,
            and Kelvin with precision and simplicity.
        </p>
    </section>

    <main class="converter">

        <label class="form-label" for="temperature">
            Enter Temperature
        </label>

        <div class="input-group">

            <input
                type="number"
                id="temperature"
                placeholder="e.g. 25"
                step="any"
            >

            <select id="unit">
                <option value="C">Celsius (°C)</option>
                <option value="F">Fahrenheit (°F)</option>
                <option value="K">Kelvin (K)</option>
            </select>

        </div>

        <button onclick="convertTemperature()">
            Convert Temperature →
        </button>

        <div class="message" id="message" role="alert"></div>

        <section class="results" id="results">

            <h2>Conversion Results</h2>

            <div class="result-grid">

                <div class="result-card">
                    <div class="unit">CELSIUS</div>
                    <div class="value" id="celsius">--</div>
                    <div class="symbol">°C</div>
                </div>

                <div class="result-card">
                    <div class="unit">FAHRENHEIT</div>
                    <div class="value" id="fahrenheit">--</div>
                    <div class="symbol">°F</div>
                </div>

                <div class="result-card">
                    <div class="unit">KELVIN</div>
                    <div class="value" id="kelvin">--</div>
                    <div class="symbol">K</div>
                </div>

            </div>

            <div class="result-actions">
                <button class="secondary-btn" onclick="copyResults()">
                    Copy Results
                </button>

                <button class="secondary-btn" onclick="resetConverter()">
                    Reset
                </button>
            </div>

        </section>

    </main>

    <section class="features">

        <div class="feature">
            <div class="icon">🌡️</div>
            <h3>Three Units</h3>
            <p>Celsius, Fahrenheit and Kelvin conversions.</p>
        </div>

        <div class="feature">
            <div class="icon">⚡</div>
            <h3>Instant Results</h3>
            <p>Get conversion results quickly.</p>
        </div>

        <div class="feature">
            <div class="icon">✓</div>
            <h3>Input Validation</h3>
            <p>Validates inputs and absolute zero limits.</p>
        </div>

    </section>

    <footer>
        <p>Built with Python & Flask</p>
        <p>Prodigy InfoTech | Software Development Internship</p>
        <p>Task 01 - Temperature Conversion Program</p>
    </footer>

</div>

<script>

    let latestResults = null;

    async function convertTemperature() {

        const temperature = document.getElementById("temperature").value;
        const unit = document.getElementById("unit").value;
        const message = document.getElementById("message");
        const results = document.getElementById("results");
        const button = document.querySelector("button");

        message.textContent = "";
        results.style.display = "none";

        if (temperature.trim() === "") {
            message.textContent = "Please enter a temperature value.";
            return;
        }

        button.disabled = true;
        button.textContent = "Converting...";

        try {

            const response = await fetch("/convert", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    temperature: temperature,
                    unit: unit
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Conversion failed.");
            }

            latestResults = data;

            document.getElementById("celsius").textContent =
                data.results.Celsius.toFixed(2);

            document.getElementById("fahrenheit").textContent =
                data.results.Fahrenheit.toFixed(2);

            document.getElementById("kelvin").textContent =
                data.results.Kelvin.toFixed(2);

            results.style.display = "block";

        } catch (error) {

            message.textContent = error.message;

        } finally {

            button.disabled = false;
            button.textContent = "Convert Temperature →";

        }
    }

    function copyResults() {

        if (!latestResults) return;

        const data = latestResults.results;

        const text = [
            "TEMPERATURE CONVERSION RESULTS",
            `Celsius: ${data.Celsius.toFixed(2)} °C`,
            `Fahrenheit: ${data.Fahrenheit.toFixed(2)} °F`,
            `Kelvin: ${data.Kelvin.toFixed(2)} K`
        ].join("\\n");

        navigator.clipboard.writeText(text)
            .then(() => {
                document.getElementById("message").textContent =
                    "Results copied successfully!";
            })
            .catch(() => {
                document.getElementById("message").textContent =
                    "Unable to copy results.";
            });
    }

    function resetConverter() {

        document.getElementById("temperature").value = "";
        document.getElementById("unit").value = "C";
        document.getElementById("results").style.display = "none";
        document.getElementById("message").textContent = "";

        latestResults = null;
    }

    document.getElementById("temperature")
        .addEventListener("keydown", function(event) {
            if (event.key === "Enter") {
                convertTemperature();
            }
        });

</script>

</body>
</html>
"""


# ---------------- FLASK ROUTES ----------------

@app.route("/", methods=["GET"])
def home():

    return render_template_string(HTML_PAGE)


@app.route("/convert", methods=["POST"])
def convert():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid request data."}), 400

    try:

        raw_value = data.get("temperature")
        unit = data.get("unit")

        if isinstance(raw_value, bool) or raw_value is None:
            raise ValueError("Please enter a valid temperature.")

        value = float(raw_value)

        if not isinstance(unit, str):
            raise ValueError("Please select a valid unit.")

        unit = unit.upper()

        error = validate_temperature(value, unit)

        if error:
            raise ValueError(error)

        results = convert_temperature(value, unit)

        return jsonify({
            "success": True,
            "original_value": value,
            "original_unit": unit,
            "results": results
        })

    except (ValueError, TypeError):
        return jsonify({
            "error": "Please enter a valid numeric temperature."
        }), 400


# ---------------- APPLICATION ENTRY POINT ----------------

if __name__ == "__main__":

    print("=" * 50)
    print("     TEMPORA - TEMPERATURE CONVERTER")
    print("=" * 50)
    print("Server running at: http://127.0.0.1:5000")
    print("Press CTRL+C to stop the server.")
    print("=" * 50)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )

