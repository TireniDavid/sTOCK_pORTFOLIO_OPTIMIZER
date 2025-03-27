from django.core.management.base import BaseCommand
from my_app.models import Stock, Stock_Group
import json

class Command(BaseCommand):
    help = 'Populate stock data into Django models'

    def handle(self, *args, **kwargs):
        # Define the path where your JSON files are stored
        stock_groups = ['Dow-Jones-30', 'Nasdaq-100', 'S&P-500']
        
        for group_name in stock_groups:
            # Load the JSON data for each stock group
            file_path = f"/Users/tireniadekoya/Desktop/ai-trader/my_app/static/data/{group_name}.json"
            
            try:
                with open(file_path, 'r') as f:
                    stock_data = json.load(f)
            except FileNotFoundError:
                self.stdout.write(self.style.ERROR(f"File {group_name}.json not found!"))
                continue

            # Get or create the StockGroup object
            stock_group, created = Stock_Group.objects.get_or_create(name=group_name)

            # Iterate over each stock in the group and add it to the database
            for stock_info in stock_data.get(group_name, []):
                name = stock_info.get('name')
                symbol = stock_info.get('symbol')

                # Create or get the stock object
                stock, created = Stock.objects.get_or_create(
                    symbol=symbol,
                    defaults={'name': name, 'sector': 'Unknown'},  # You can add sector info if available
                )

                # Add the stock to the stock group
                stock.groups.add(stock_group)
                self.stdout.write(self.style.SUCCESS(f"Stock {name} ({symbol}) added to {group_name}"))

        self.stdout.write(self.style.SUCCESS('All stocks have been populated!'))
