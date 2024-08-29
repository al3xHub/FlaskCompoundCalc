import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io 
import base64
from flask import Flask, render_template, request 

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        initial_deposit = float(request.form['initial_deposit'])
        interest_rate = float(request.form['interest_rate'])
        contribution = float(request.form['contribution'])
        compound_type = request.form['compound_type']
        time_period_year = float(request.form['time_period_year'])

        if compound_type == 'monthly':
            n = 12
        elif compound_type == 'quarterly':
            n = 4
        else:
            n=1

        total_amount = initial_deposit * (1 + interest_rate / n) ** (n * time_period_year)
        total_contributions = contribution * (((1+ interest_rate/n) ** (n * time_period_year)-1) / (interest_rate /n))

        final_amount_with_interest = total_amount + total_contributions
        
        total_contributions_without_interest = initial_deposit + contribution + time_period_year * n
        
        difference = final_amount_with_interest - total_contributions_without_interest
        
        amounts_with_interest = []
        amounts_without_interest = []
        
        for year in range(1, int(time_period_year) + 1):
            amount_with_interest = initial_deposit * (1 + interest_rate / n) ** (n * year)
            amount_without_interest = initial_deposit + contribution * year * n
            amounts_with_interest.append(amount_with_interest)
            amounts_without_interest.append(amount_without_interest)
            
        plt.figure(figsize=(10, 5))
        plt.plot(range(1, int(time_period_year) + 1), amounts_with_interest, marker = "o", label='Amount with Interest')
        plt.plot(range(1, int(time_period_year) + 1), amounts_without_interest, marker = "o", label='Amount without Interest')
        plt.xlabel('Years')
        plt.ylabel('Amount')
        plt.title('Compound Interest Over Time')
        plt.legend()
        plt.grid(True)
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.read()).decode('utf8')
        
        return render_template('results.html', plot_url=plot_url, final_amount=final_amount_with_interest, difference=difference)
    else:
        return render_template('index.html')
    
if __name__ == '__main__':
    app.run(debug=True)