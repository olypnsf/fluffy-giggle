from flask import Flask, render_template, request
import pandas as pd
import math

app = Flask(__name__)

def import_data(file_path):
    try:
        data = pd.read_csv(file_path)  # For CSV files
    except pd.errors.ParserError:
        data = pd.read_excel(file_path)  # For XLSX files
    return data

def analyze_spending(data):
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    monthly_spending = data.resample('M').sum()
    return monthly_spending

def budgeting_advice(monthly_spending, expetency_of_years, monthly_budget):
    average_monthly_spending = monthly_spending['Amount'].mean()
    budget = math.floor(average_monthly_spending * 12 * expetency_of_years)
    
    if monthly_budget > average_monthly_spending:
        status = "Gold (Financial Healthy)"
    elif monthly_budget >= 0.8 * average_monthly_spending:
        status = "Balanced"
    elif monthly_budget >= 0.5 * average_monthly_spending:
        status = "Almost Broke"
    else:
        status = "Broke"

    return budget, status

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file_path = request.form['file_path']
        expetency_of_years = int(request.form['expetency_of_years'])
        monthly_budget = float(request.form['monthly_budget'])

        data = import_data(file_path)
        monthly_spending = analyze_spending(data)
        budget, status = budgeting_advice(monthly_spending, expetency_of_years, monthly_budget)

        return render_template('result.html', budget=budget, status=status)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
