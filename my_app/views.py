from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm
from .utils import download_n_clean_data
from django.http import JsonResponse
from .models import Stock, Stock_Group
from .forms import PortfolioForm  
import json

# Create your views here.

class CustomLoginView(LoginView):
    template_name='home.html'
    authentication_form= CustomLoginForm
    
def home(request):
    return render(request, 'home.html')

def watchlist(request):
    range_list = [i for i in range(6)]
    return render(request, 'watchlist.html', {'range_list': range_list})

def portfolio(request):
    if request.method == "POST":
        if form.isvalid():
            form = PortfolioForm(request.POST)
            return 'success_page'
    else:
        form = PortfolioForm()  
    
    chart_data = {
        "labels": ["Tech", "Commodity", "HealthCare", "Industrial", "Energy"],
        "series": [15, 20, 20, 15, 30]
    }

    return render(request, 'portfolio.html', {'form': form, 'chart_data': json.dumps(chart_data)})


def strategies(request):
    return render(request, 'strategies.html')

def simulation(request):
    return render(request, 'simulation.html')

def backtest(request):
    # Set the symbol and date range
    symbol = 'SPY'
    start_date = '1993-01-01'
    end_date = '2020-02-16'

    # Ensure the stock exists in the database
    stock, created = Stock.objects.get_or_create(symbol=symbol)
    
    # Get the cleaned data
    clean_data = download_n_clean_data(symbol, start_date, end_date)

    # Pass the data to the template
    context = {'data': clean_data.to_dict(orient='records')}  # Convert DataFrame to a dictionary

    # Pass the data to the template
    return render(request, 'backtest.html', context)
    

def fetch_stock_data(request):
    ticker = request.GET.get('ticker', 'SPY').upper()
    start_date = request.GET.get('start_date', '1993-01-01')
    end_date = request.GET.get('end_date', '2020-02-16')


    #### checks input data against models database
    if not Stock.objects.filter(symbol=ticker).exists():
        return JsonResponse({
            'valid': False,
            'error': f'Ticker {ticker} not found in database'
        }, status=200)
    

    try:
        # Use your existing utility function
        clean_data = download_n_clean_data(ticker, start_date, end_date)
        
        # Convert timestamp back to datetime for frontend
       
        return JsonResponse({
            'valid': True,
            'data': clean_data.to_dict(orient='records')
            
        })
    
    except Exception as e:
        return JsonResponse({
            'valid': False,
            'error': str(e)
        }, status=200)
    



def settings(request):
    return render(request, 'settings.html')

def about_us(request):
    return render(request, 'about_us.html')

def help(request):
    return render(request, 'help.html')

def contact_us(request):
    return render(request, 'contact_us.html')

def pro_scan(request):
    return render(request, 'pro_scan.html')

def stock_list(request, group_name):
    group = Stock_Group.objects.get(name=group_name)
    stocks = group.stocks.all()
    return render(request, 'pro_scan.html', {'stocks': stocks})
