from flask import Flask, render_template, request, redirect, url_for, jsonify
from textblob import TextBlob
import requests

import json

app = Flask(__name__)

@app.route("/", methods = ["GET"])
def main():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def submit_review():
    print("ehhlasd")
    if request.is_json:
        # JSON payload
        review_text = request.get_json()
    elif 'file' in request.files:
        # file upload
        file = request.files['file']
        review_text = file.read().decode('utf-8')
    else:
        return jsonify({'error': 'No review text provided'}, status = 400)
    sentiment = []
    # print(review_text)
    for review in review_text:
        blob = TextBlob(review.review_text)
        score = blob.sentiment.polarity
        if score < 0:
            polarity = "Negative"
        elif score == 0:
            polarity = "Neutral"
        else:
            polarity = "Positive"
        rev = {'origianl_review_text': review.review_text,
               'sentiment_category': polarity,
               'polarity score' : score}
    return jsonify(sentiment, status=200, mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=False, port = 5000)