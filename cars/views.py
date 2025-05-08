from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Car, CarBrand, CarCategory
from .forms import ContactForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import CarForm, CarImageFormSet

def home(request):
    featured_cars = Car.objects.filter(is_featured=True)[:6]
    latest_cars = Car.objects.all().order_by('-created_date')[:6]
    brands = CarBrand.objects.all()
    categories = CarCategory.objects.all()
    
    context = {
        'featured_cars': featured_cars,
        'latest_cars': latest_cars,
        'brands': brands,
        'categories': categories,
    }
    return render(request, 'cars/home.html', context)

def faq(request):
    return render(request, 'cars/faq.html')

def about(request):
    return render(request, 'cars/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent. We will contact you soon!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'cars/contact.html', {'form': form})

def services(request):
    return render(request, 'cars/services.html')

def latest(request):
    latest_cars = Car.objects.all().order_by('-created_date')
    paginator = Paginator(latest_cars, 9)  # Show 9 cars per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'cars/latest.html', {'page_obj': page_obj})

def car_list(request):
    cars = Car.objects.all().order_by('-created_date')
    
    # Filtering
    brand = request.GET.get('brand')
    category = request.GET.get('category')
    year = request.GET.get('year')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    
    if brand:
        cars = cars.filter(brand__name=brand)
    if category:
        cars = cars.filter(category__name=category)
    if year:
        cars = cars.filter(year=year)
    if price_min:
        cars = cars.filter(price__gte=price_min)
    if price_max:
        cars = cars.filter(price__lte=price_max)
    
    # Pagination
    paginator = Paginator(cars, 9)  # Show 9 cars per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Filter options
    brands = CarBrand.objects.all()
    categories = CarCategory.objects.all()
    years = Car.objects.values_list('year', flat=True).distinct().order_by('-year')
    
    context = {
        'page_obj': page_obj,
        'brands': brands,
        'categories': categories,
        'years': years,
        'selected_brand': brand,
        'selected_category': category,
        'selected_year': year,
        'selected_price_min': price_min,
        'selected_price_max': price_max,
    }
    
    return render(request, 'cars/car_list.html', context)

def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    similar_cars = Car.objects.filter(category=car.category).exclude(pk=pk)[:3]
    
    context = {
        'car': car,
        'similar_cars': similar_cars,
    }
    
    return render(request, 'cars/car_detail.html', context)


@login_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        formset = CarImageFormSet(request.POST, request.FILES, instance=Car(owner=request.user))
        if form.is_valid() and formset.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            formset.instance = car
            formset.save()
            return redirect('car_detail', pk=car.pk)
    else:
        form = CarForm()
        formset = CarImageFormSet(instance=Car(owner=request.user))
    return render(request, 'cars/add_car.html', {'form': form, 'formset': formset})

@login_required
def edit_car(request, pk):
    car = get_object_or_404(Car, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        formset = CarImageFormSet(request.POST, request.FILES, instance=car)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('car_detail', pk=car.pk)
    else:
        form = CarForm(instance=car)
        formset = CarImageFormSet(instance=car)
    return render(request, 'cars/edit_car.html', {'form': form, 'formset': formset})

@login_required
def delete_car(request, pk):
    car = get_object_or_404(Car, pk=pk, owner=request.user)
    if request.method == 'POST':
        car.delete()
        return redirect('car_list')
    return render(request, 'cars/delete_car.html', {'car': car})