from django.shortcuts import render, redirect
from django.http import HttpResponse
from delivery.models import Customer, Restaurants, Menu
from delivery.forms import ResForm, MenuForm
# Create your views here.
def index(request):
    return render(request,'delivery/index.html')

def sign_in(request):
    return render(request, 'delivery/sign_in.html')

def sign_up(request):
    return render(request,'delivery/sign_up.html')

def handle_signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            cus = Customer.objects.get(username = username, password = password)
            if username == 'admin':
                return render(request, 'delivery/success.html')
            else:
                return render(request, 'delivery/customer_home.html')
        except:
            return render(request, 'delivery/failed.html')
    
def handle_signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        try:
            cus = Customer.objects.get( username =  username, password = password)
        except:
            cus = Customer(username= username, password = password, email = email, mobile= mobile, address=address)
            cus.save()
        return render(request, 'delivery/sign_in.html')
    else:
        return HttpResponse('Invalid Request')

def add_res(request):
    form = ResForm(request.POST or None)
    if form.is_valid():
        res_name = request.POST.get('Res_name')
        try: 
            res = Restaurants.objects.get(Res_name = res_name)
        except:
            form.save()
            return redirect('delivery:display_res')
    return render(request, 'delivery/add_res.html',{'form':form})

def display_res(request):
    li = Restaurants.objects.all()
    return render(request, 'delivery/display_res.html',{'li':li})

def view_menu(request, id):
    res = Restaurants.objects.get(pk=id)
    menu = Menu.objects.filter(res=res)  
    return render(request, 'delivery/menu.html',{'res':res, 'menu':menu})

def add_menu(request, id):
    form = MenuForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('delivery:view_menu', id)
    return render(request,'delivery/menu_form.html',{'form':form})

def delete_menu(request,id):
    item = Menu.objects.get(pk=id)
    res_id = item.res.id
    item.delete()
    return redirect('delivery:view_menu',res_id)

def cusdisplay_res(request):
    li = Restaurants.objects.all()
    return render(request, 'delivery/cusdisplay_res.html',{'li':li})

def cusmenu(request,id):
    res = Restaurants.objects.get(pk=id)
    menu = Menu.objects.filter(res=res)  
    return render(request, 'delivery/cusmenu.html',{'res':res, 'menu':menu})
