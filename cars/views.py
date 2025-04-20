
from django.shortcuts import render, redirect, get_object_or_404
from .models import Car
from .forms import CarForm
from django.contrib.auth.decorators import login_required


def car_list(request):
    cars = Car.objects.all()
    return render(request, 'cars/hello.html', {'cars': cars})

@login_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CarForm()
    return render(request, 'cars/add_car.html', {'form': form})

@login_required
def edit_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        form = CarForm(request.POST,request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CarForm(instance=car)
    return render(request, 'cars/edit_car.html', {'form': form})

@login_required
def delete_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        car.delete()
        return redirect('home')
    return render(request, 'cars/delete_car.html', {'car': car})

from django.db.models import Q

def car_list(request):
    query = request.GET.get('q')  # Get the search keyword from URL
    if query:
        # Search by brand or name (case-insensitive)
        cars = Car.objects.filter(
            Q(brand__icontains=query) |
            Q(name__icontains=query)
        )
    else:
        cars = Car.objects.all()

    return render(request, 'cars/hello.html', {'cars': cars})

from .models import Car, Bid
from .forms import BidForm

def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    bids = car.bids.all().order_by('-amount')  # Show highest bids first

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = BidForm(request.POST)
            if form.is_valid():
                bid = form.save(commit=False)
                bid.car = car
                bid.user = request.user
                bid.save()
                return redirect('car_detail', pk=car.pk)
        else:
            return redirect('login')
    else:
        form = BidForm()

    return render(request, 'cars/car_detail.html', {
        'car': car,
        'form': form,
        'bids': bids,
    })


