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
        interest_rate = float(request.form['interest_rate']) / 100  # Convertir porcentaje a decimal
        contribution = float(request.form['contribution'])
        compound_type = request.form['compound_type']
        time_period_year = float(request.form['time_period_year'])

        # Determinar el número de veces que se capitaliza por año
        if compound_type == 'Monthly':
            n = 12
        elif compound_type == 'Quarterly':
            n = 4
        else:
            n = 1

        # Cálculo del monto final con interés sobre el depósito inicial
        total_amount = initial_deposit * (1 + interest_rate / n) ** (n * time_period_year)
        
        # Cálculo del monto final con las contribuciones periódicas con interés
        total_contributions = contribution * (((1 + interest_rate / n) ** (n * time_period_year) - 1) / (interest_rate / n))

        # Monto final incluyendo el depósito inicial y las contribuciones con interés
        final_amount_with_interest = total_amount + total_contributions
        
        # Suma total de contribuciones sin interés
        total_contributions_without_interest = initial_deposit + contribution * n * time_period_year
        
        # Diferencia entre lo obtenido con interés y las contribuciones sin interés
        difference = final_amount_with_interest - total_contributions_without_interest
        
        amounts_with_interest = []
        amounts_without_interest = []
        
        for year in range(1, int(time_period_year) + 1):
            # Cálculo del monto con interés hasta el año actual
            amount_with_interest = initial_deposit * (1 + interest_rate / n) ** (n * year) + \
                                   contribution * (((1 + interest_rate / n) ** (n * year) - 1) / (interest_rate / n))
            # Cálculo del monto sin interés
            amount_without_interest = initial_deposit + contribution * n * year
            amounts_with_interest.append(amount_with_interest)
            amounts_without_interest.append(amount_without_interest)
        
        # Generación de la gráfica
        plt.figure(figsize=(10, 5))
        plt.plot(range(1, int(time_period_year) + 1), amounts_with_interest, marker="o", label='Amount with Interest')
        plt.plot(range(1, int(time_period_year) + 1), amounts_without_interest, marker="o", label='Amount without Interest')
        plt.xlabel('Years')
        plt.ylabel('Amount')
        plt.title('Compound Interest Over Time')
        plt.legend()
        plt.grid(True)
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.read()).decode('utf8')
        
        return render_template('results.html', plot_url=plot_url, initial_deposit=initial_deposit, contribution=contribution, time_period_year=time_period_year, interest_rate=interest_rate, compound_type=compound_type, final_amount=final_amount_with_interest, difference=difference, total_contributions_without_interest=total_contributions_without_interest)
    else:
        return render_template('index.html')

  
if __name__ == '__main__':
    app.run(debug=False)
