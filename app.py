from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)
CATEGORIES = {
    "food": ["restaurant", "hotel", "zomato", "swiggy", "groceries", "grocery", "supermarket"],
    "transport": ["uber", "ola", "auto", "petrol", "fuel", "bus", "train", "metro"],
    "bills": ["electricity", "water", "wifi", "recharge", "mobile", "gas", "insurance", "rent"],
    "shopping": ["amazon", "flipkart", "myntra", "clothing", "apparel", "shoes", "store"],
    "education": ["school", "college", "fees", "exam", "books", "coaching", "tuition"],
    "medical": ["hospital", "clinic", "pharmacy", "medicine", "doctor", "lab"],
    "entertainment": ["movie", "cinema", "netflix", "prime", "hotstar", "recreation"],
    "investment": ["mutual", "sip", "stocks", "shares", "insurance", "lic", "ppf"],
    "others": []
}

def categorize(description):
    description = description.lower()
    for category, keywords in CATEGORIES.items():
        if any(keyword in description for keyword in keywords):
            return category
    return 'others'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file.filename.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.filename.endswith('.xlsx'):
        df = pd.read_excel(file)
    else:
        return 'Unsupported file format', 400
    
    df['Category'] = df['Description'].apply(categorize)
    summary = df.groupby('Category')['Amount'].sum().reset_index()

    chart_data = {
        'labels': summary['Category'].tolist(),
        'data': summary['Amount'].tolist()
    }

    table_html = df.to_html(classes='table', index=False)
    return render_template('index.html', table=table_html, chart_data=chart_data)

if __name__ == '__main__':
    app.run(debug=True)
