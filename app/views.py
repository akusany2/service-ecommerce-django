from django.forms.models import model_to_dict
from app.models import Clients, ServiceMenu
from django.contrib import auth
from unauthorized_page import unauthenticated_user
import json
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home(req):
  context = {}
  return render(req, 'home.html', context)


@unauthenticated_user(redirect, 'editor')
def register(req):

  form = UserCreationForm()

  if req.method == 'POST':
    form = UserCreationForm(req.POST)
    if form.is_valid():
      company = req.POST.get('company')
      userForm = form.save()
      user = User.objects.get(id=userForm.id)
      ServiceMenu.objects.create(company_name=company, user=user)
      messages.success(req, 'Account created successfuly')
      return redirect('login')

  context = {'form': form}
  return render(req, 'register.html', context)


@unauthenticated_user(redirect, 'editor')
def loginPage(req):

  if req.method == 'POST':
    username = req.POST.get('username')
    password = req.POST.get('password')

    user = authenticate(req, username=username, password=password)

    if user is not None:
      login(req, user)
      return redirect('editor')
    else:
      messages.info(req, 'Email or Password is incorrect')

  context = {}
  return render(req, 'login.html', context)


def logoutUser(req):
  logout(req)
  return redirect('login')

@login_required(login_url='login')
def editor(req):
  # print(req.user.id)
  service = ServiceMenu.objects.get(user=req.user.id)
  context = {'company_name': service.company_name, 'list': service.items['menu_items'], 'sharable_url': req.get_host()+"/client-order/"+str(service.id)}
  return render(req, 'editor.html', context)

@login_required(login_url='login')
def clients(req):
  service = ServiceMenu.objects.get(user=req.user.id)
  clients = Clients.objects.filter(serviceId=service.id)
  print(clients)
  context = {'company_name': service.company_name, "clients": clients}
  return render(req, 'clients.html', context)

@login_required(login_url='login')
def newService(req):
  context = {}
  if req.method == 'POST':
    item = {
      "name": req.POST.get('name'),
      "description": req.POST.get('description'),
      "price": req.POST.get('price')
    }
    
    service = ServiceMenu.objects.get(user=req.user.id)
    
    if "menu_items" not in service.items:
      service.items = json.dumps({
        "menu_items": [item]
      })
      service.save()
    else:
      items = service.items
      items["menu_items"].append(item)
      service.items = items
      service.save()
    return redirect('editor')
  
  return render(req, 'service-item.html', context)


@login_required(login_url='login')
def editService(req, index):
  
  service = ServiceMenu.objects.get(user=req.user.id)
  populate_item = service.items['menu_items'][index]
  context = populate_item
  if req.method == 'POST':
    item = {
      "name": req.POST.get('name'),
      "description": req.POST.get('description'),
      "price": req.POST.get('price')
    }
    
    items = service.items
    items["menu_items"][index] = item
    service.items = items
    service.save()
    return redirect('editor')
  
  return render(req, 'service-item-edit.html', context)

@login_required(login_url='login')
def deletService(req, index):
  
  service = ServiceMenu.objects.get(user=req.user.id)
  service.items['menu_items'].pop(index)
  service.save()
  return redirect('editor')
  
# Public view

def clientPublic(req, id):
  service = ServiceMenu.objects.get(id=id)
  success = False
  total_payment = 0
  if req.method == 'POST':
    email = req.POST.get('email')
    service_list = req.POST.getlist('service-item')
    service_opted = {
      "services": []
    }
    for item in service_list:
      service_opted["services"].append(service.items["menu_items"][int(item)])
      total_payment += int(service.items["menu_items"][int(item)]['price'])
      
    client = Clients.objects.create(email=email, service_opted=service_opted, serviceId=service, total_payment=total_payment)
    client.save()
    success = True

  context = {"service": model_to_dict(service), "success": success}
  return render(req, 'client-public.html', context)