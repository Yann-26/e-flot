from django.shortcuts import render
from admin_dashboard.models import Garage

# Create your views here.
def home(request):
    garages = Garage.objects.all().order_by('-id')

    datas = {
        "garages":garages,

    }
    return render(request, 'index.html', datas)