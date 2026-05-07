from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import os

app = Flask(__name__)

MODEL_PATH = 'laptop_model.joblib'
METADATA_PATH = 'laptop_metadata.joblib'

model = None
metadata = None

if os.path.exists(MODEL_PATH) and os.path.exists(METADATA_PATH):
    model = joblib.load(MODEL_PATH)
    metadata = joblib.load(METADATA_PATH)

@app.route('/')
def index():
    data = metadata if metadata else {
        'brands': ['Apple', 'Dell', 'HP', 'Lenovo'],
        'processors': ['Intel Core i5', 'Intel Core i7', 'AMD Ryzen 5', 'AMD Ryzen 7'],
        'gpus': ['Intel Iris Xe', 'NVIDIA GTX 1650', 'NVIDIA RTX 3060'],
        'rams': [8, 16, 32],
        'storages': [256, 512, 1024]
    }
    return render_template('index.html', metadata=data, model_loaded=(model is not None))

def number_to_words(n):
    if n == 0: return "zero"
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
            "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    def convert_below_100(num):
        if num < 20: return ones[num]
        return tens[num // 10] + (" " + ones[num % 10] if num % 10 != 0 else "")
            
    def convert_below_1000(num):
        if num < 100: return convert_below_100(num)
        return ones[num // 100] + " hundred" + (" and " + convert_below_100(num % 100) if num % 100 != 0 else "")
            
    parts = []
    if n >= 10000000:
        parts.append(convert_below_100(n // 10000000) + " crore")
        n %= 10000000
    if n >= 100000:
        parts.append(convert_below_100(n // 100000) + " lakh")
        n %= 100000
    if n >= 1000:
        parts.append(convert_below_100(n // 1000) + " thousand")
        n %= 1000
    if n > 0:
        parts.append(convert_below_1000(n))
    return " ".join(parts).capitalize()

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not trained yet! Please run train_model.py'}), 500
        
    try:
        data = request.json
        
        df = pd.DataFrame([{
            'Brand': data['brand'],
            'Processor': data['processor'],
            'RAM_GB': int(data['ram']),
            'Storage_GB': int(data['storage']),
            'GPU': data['gpu']
        }])
        
        prediction = model.predict(df)[0]
        
        price_pkr = int(round(prediction))
        
        return jsonify({
            'price': price_pkr,
            'price_words': number_to_words(price_pkr) + " rupees"
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
