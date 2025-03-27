from django.core.management.base import BaseCommand
from my_app.models import Stock, Stock_Group

class Command(BaseCommand):
    help = 'Deletes all stocks from the database'

    def handle(self, *args, **kwargs):
        Stock.objects.all().delete()
        Stock_Group.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("All stocks deleted!"))
        self.stdout.write(self.style.SUCCESS("All stock group deleted!"))