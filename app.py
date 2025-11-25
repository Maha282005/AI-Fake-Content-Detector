from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)
openai.api_key = "YOUR_OPENAI_KEY"  # Replace with your OpenAI key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']

    # Read text from uploaded file (for simplicity, only txt supported here)
    text = file.read().decode('utf-8', errors='ignore')

    # --- Step 1: Detect AI content ---
    # Example: fake AI probability
    ai_probability = 70 if len(text) > 0 else 0
    verdict = "Likely AI-Generated" if ai_probability > 50 else "Human"

    # --- Step 2: Humanize AI content ---
    if ai_probability > 50:
        prompt = f"Paraphrase this AI-generated text as if written by a human:\n\n{text}"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=1000
        )
        humanized_text = response.choices[0].text.strip()
    else:
        humanized_text = text

    return jsonify({
        "confidence": 100 - ai_probability,
        "verdict": verdict,
        "humanized_text": humanized_text
    })

if __name__ == "__main__":
    app.run(debug=True)
