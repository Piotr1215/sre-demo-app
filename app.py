#!/usr/bin/env python3
import os
from flask import Flask, render_template_string, jsonify
from openai import OpenAI
import random

app = Flask(__name__)

# Initialize OpenAI client
api_key = os.environ.get('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set")

client = OpenAI(api_key=api_key)

# HTML template with dark theme for SRE vibes
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SRE Haiku Horror Generator</title>
    <style>
        body {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #fff;
            font-family: 'Courier New', monospace;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }
        .container {
            background: rgba(0, 0, 0, 0.7);
            border-radius: 15px;
            padding: 40px;
            max-width: 600px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            text-align: center;
            color: #ff6b6b;
            margin-bottom: 10px;
            font-size: 2em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .subtitle {
            text-align: center;
            color: #94a3b8;
            margin-bottom: 30px;
            font-size: 0.9em;
        }
        #haiku-display {
            background: rgba(255, 107, 107, 0.1);
            border: 2px solid #ff6b6b;
            border-radius: 10px;
            padding: 30px;
            margin: 30px 0;
            min-height: 120px;
            white-space: pre-line;
            line-height: 1.8;
            font-size: 1.2em;
            text-align: center;
            transition: all 0.3s ease;
        }
        #haiku-display.loading {
            opacity: 0.5;
        }
        button {
            background: #ff6b6b;
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 50px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            display: block;
            margin: 0 auto;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        button:hover {
            background: #ff5252;
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(255,107,107,0.3);
        }
        button:active {
            transform: translateY(0);
        }
        .loading-text {
            text-align: center;
            color: #94a3b8;
            font-style: italic;
        }
        .gpu-info {
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.8);
            padding: 10px 15px;
            border-radius: 5px;
            font-size: 0.9em;
            color: #4ade80;
        }
        .error {
            color: #f87171;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="gpu-info">
        GPU: 50% allocated by KAI
    </div>
    <div class="container">
        <h1>SRE Haiku Horror Generator</h1>
        <div class="subtitle">Powered by fractional GPU allocation via KAI Scheduler</div>
        <div id="haiku-display">
            Click the button to summon<br>
            An SRE horror haiku<br>
            From the depths of on-call hell
        </div>
        <button onclick="generateHaiku()">Generate Horror Haiku</button>
    </div>

    <script>
        async function generateHaiku() {
            const display = document.getElementById('haiku-display');
            const button = document.querySelector('button');

            display.classList.add('loading');
            display.innerHTML = '<div class="loading-text">Consulting the on-call spirits...</div>';
            button.disabled = true;

            try {
                const response = await fetch('/generate');
                const data = await response.json();

                if (data.error) {
                    display.innerHTML = `<div class="error">Error: ${data.error}</div>`;
                } else {
                    display.innerHTML = data.haiku;
                }
            } catch (error) {
                display.innerHTML = `<div class="error">Failed to connect to the haiku generator</div>`;
            } finally {
                display.classList.remove('loading');
                button.disabled = false;
            }
        }
    </script>
</body>
</html>
'''

# SRE horror themes for inspiration
SRE_THEMES = [
    "disk space full", "OOMKilled", "DNS failure", "certificate expired",
    "wrong kubectl context", "database down", "pager fatigue", "3am incident",
    "deployment on Friday", "missing backups", "kubernetes CrashLoopBackOff",
    "memory leak", "CPU throttling", "network partition", "split brain",
    "cascading failure", "thundering herd", "cache invalidation",
    "race condition", "deadlock", "data corruption", "lost quorum",
    "zombie process", "kernel panic", "segmentation fault"
]

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate')
def generate():
    try:
        # Pick random SRE horror themes
        theme = random.choice(SRE_THEMES)

        prompt = f"""Generate a haiku about this SRE/DevOps horror scenario: {theme}

        The haiku must:
        - Follow 5-7-5 syllable structure strictly
        - Be darkly humorous about on-call/operations pain
        - Reference the specific technical issue
        - Feel like something an exhausted SRE would write at 3am

        Return ONLY the haiku, no explanation."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a burned-out SRE writing haikus about production incidents."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=50
        )

        haiku = response.choices[0].message.content.strip()
        return jsonify({"haiku": haiku})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)