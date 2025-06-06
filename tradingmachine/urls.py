"""
URL configuration for tradingmachine project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from my_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('', views.CustomLoginView.as_view(), name='home'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('get-portfolio-form/<int:portfolio_id>/', views.get_portfolio_form, name='get_portfolio_form'),
    path('get-default-panel/', views.get_default_portfolio_panel, name='get_default_portfolio_panel'),
    path('get-empty-form/', views.get_empty_form, name='get_empty_form'),
    path('get-preset-form/<str:preset_name>/', views.get_preset_form, name='get_preset_form'),
    path('strategies/', views.strategies, name='strategies'),
    path('backtest/', views.backtest, name='backtest'),
    path('render_indicator_partial/<str:indicator>/', views.render_indicator_partial, name='render_indicator_partial'),
    path('render_strategy_partial/', views.render_strategy_partial, name='render_strategy_partial'),
    path('pro_scan/', views.pro_scan, name='pro_scan'),
    path('stocks/<str:group_name>/', views.stock_list, name='stock_list'),
    path('fetch_stock_data/', views.fetch_stock_data, name='fetch_stock_data'),
    path('fetch_group_data/', views.fetch_group_data, name='fetch_group_data'),
    path('settings/', views.settings, name='settings'),
    path('help/', views.help, name='help'),
]
