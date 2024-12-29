from flask import Flask, render_template, jsonify
from scraper import scrape_trends

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape')
def scrape():
    try:
        # Fetch trendy topics directly from scrape_trends
        record = scrape_trends()
        print("Record from scrape_trends:", record)  # Debug log
        return jsonify({
            "status": "success",
            "timestamp": record["timestamp"],
            "trends": record["trends"],  # Ensure this is passed correctly
            "ip_address": record["ip_address"]
        })
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
