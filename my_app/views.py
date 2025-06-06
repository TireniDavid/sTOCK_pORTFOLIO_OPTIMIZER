from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm
from .utils import download_n_clean_data
from django.http import JsonResponse
from .models import Stock, Stock_Group, Portfolio
from .forms import PortfolioForm  
from django.views.decorators.http import require_GET
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

def get_default_portfolio_panel(request):
    default_portfolio = Portfolio.objects.filter(is_default=True).first()
    
    if not default_portfolio:
        default_portfolio = Portfolio(**PRESET_PORTFOLIOS['threefund'])

    return render(request, 'partials/default_portfolio_panel.html', {
        'default_portfolio': default_portfolio
    })

def portfolio(request):
    if request.method == "POST":
        portfolio_id = request.POST.get('portfolio_id')
        form = PortfolioForm(request.POST, instance=Portfolio.objects.get(id=portfolio_id) if portfolio_id else None)

        if form.is_valid():
            new_portfolio = form.save(commit=False)

            # Explicitly handle checkbox state (checked or not)
            is_def = request.POST.get('is_default', False)
            if is_def:
                Portfolio.objects.update(is_default=False)
                new_portfolio.is_default = True
            else:
                new_portfolio.is_default = False
            
            new_portfolio.save()
            return redirect('portfolio')
        
    # On GET            
    form = PortfolioForm() 
    saved_forms = [(portfolio, PortfolioForm(instance=portfolio)) for portfolio in Portfolio.objects.all()]
    default_portfolio = Portfolio.objects.filter(is_default=True).first()

    # If no portfolio is marked default, fallback explicitly to Three Fund Portfolio preset
    if not default_portfolio:
        default_portfolio = Portfolio(**PRESET_PORTFOLIOS['threefund'])

    chart_data = {
        "labels": ["Tech", "Commodity", "HealthCare", "Industrial", "Energy"],
        "series": [15, 20, 20, 15, 30]
    }

    return render(request, 'portfolio.html', {
        'form': form, 
        'chart_data': json.dumps(chart_data),
        'saved_forms': saved_forms,
        'default_portfolio': default_portfolio
        })

def get_portfolio_form(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    form = PortfolioForm(instance=portfolio)
    return render(request, 'partials/portfolio_form_partial.html', {'form': form, 'portfolio': portfolio})

# Dummy preset data templates
PRESET_PORTFOLIOS = {
    'permanent': {
        'name': 'Permanent Portfolio',
        'drag_percentage': 0.5,
        'rebalance_frequency': 'Yearly',
        'total_return': True,
        'rebalance_bands': False,
        'ticker': 'VTI,TLT,GLD,CASH',
        'allocation': '25,25,25,25',
    },
    'snp500': {
        'name': 'S&P 500',
        'drag_percentage': 0.15,
        'rebalance_frequency': 'Quarterly',
        'total_return': True,
        'rebalance_bands': True,
        'ticker': 'SPY',
        'allocation': '100',
    },
    'threefund': {
        'name': 'Three Fund Portfolio',
        'drag_percentage': 0.2,
        'rebalance_frequency': 'Yearly',
        'total_return': False,
        'rebalance_bands': True,
        'ticker': 'VTI, VXUS, BND',
        'allocation': '40,40,20',
    },
}

def get_preset_form(request, preset_name):
    data = PRESET_PORTFOLIOS.get(preset_name)
    if not data:
        return render(request, 'partials/portfolio_form_partial.html', {'form': None, 'portfolio': None})

    portfolio = Portfolio(**data)
    form = PortfolioForm(instance=portfolio)
    return render(request, 'partials/portfolio_form_partial.html', {'form': form, 'portfolio': portfolio})

def get_empty_form(request):
    empty_port = Portfolio()
    form = PortfolioForm(instance=empty_port)
    return render(request, "partials/portfolio_form_partial.html", {
        "form": form, 
        "portfolio": empty_port
    })


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

def render_indicator_partial(request, indicator):
    if indicator == 'sma':
        return render(request, 'partials/indicators/indicator_modal_ma.html')   
    elif indicator == 'ema':
        return render(request, 'partials/indicators/indicator_modal_ma.html')  
    elif indicator == 'bbands':
        pass
    elif indicator == 'rsi':        
        pass
    elif indicator == 'macd':
        pass
    elif indicator == 'adx':
        pass
    elif indicator == 'stoch':
        pass
    elif indicator == 'ichimoku':
        pass
    
def render_strategy_partial(request):
    # The template will fetch the json data from static/data/golden_cross_data.json that the strategy saved
    return render(request, 'partials/strategies/golden_cross_form.html')


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
        clean_data = download_n_clean_data(ticker, start_date, end_date, compute_sma=True)
        
        # Convert timestamp back to datetime for frontend
       
        response_data = {'valid': True, 'data': clean_data.to_dict(orient='records')}
          # Debug
        return JsonResponse(response_data)
    except Exception as e:
        return JsonResponse({
            'valid': False,
            'error': str(e)
        }, status=200)
    


@require_GET
def fetch_group_data(request):
    ticker_group = request.GET.get('ticker_group')
    start_date = request.GET.get('start_date', '1993-01-01')
    end_date = request.GET.get('end_date', '2020-02-16')

    result = []

    try:
        if not ticker_group:
            return JsonResponse({'valid': False, 'error': 'No ticker_group provided'})

        group = Stock_Group.objects.get(name=ticker_group)
        print("Found group:", group.name)

        # Exclude the problematic ticker:
        tickers = group.stocks.exclude(symbol='MRPW').values_list('symbol', flat=True)
        print("Tickers in group:", tickers)

        for symbol in tickers:
            yf_symbol = symbol.replace('.', '-')
            if not Stock.objects.filter(symbol=symbol).exists():
                print(f"Symbol {symbol} not found in DB")
                result.append({'symbol': symbol, 'chartData': []})
                continue

            try:
                clean_data = download_n_clean_data(yf_symbol, start_date, end_date, compute_sma=True)
                result.append({
                    'symbol': symbol,
                    'chartData': clean_data.to_dict(orient='records')
                })
            except Exception as e:
                print(f"Error processing {symbol}: {str(e)}")
                result.append({'symbol': symbol, 'chartData': []})

        return JsonResponse({'valid': True, 'data': result})
    
    except Stock_Group.DoesNotExist:
            print("Group not found:", ticker_group)
            return JsonResponse({'valid': False, 'error': f'Group {ticker_group} not found'}, status=200)
    except Exception as e:
            print("Error in fetch_group_data:", str(e))
            return JsonResponse({'valid': False, 'error': str(e)}, status=200)


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
