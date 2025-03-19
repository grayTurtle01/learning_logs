from django.shortcuts import render, redirect
# ~ from django.core.urlresolvers import reverse

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def index(request):
    return render(request, 'users/index.html')
    
def logout_view(request):
    logout(request)
    return redirect('index')
    
def register(request):
    
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        
        if form.is_valid():
            new_user = form.save()
            
            authenticated_user = authenticate(
                username=new_user.username, password=request.POST['password1'])
            login(request, authenticated_user)
            
            return redirect('index')

    context = {'form': form}
    return render(request, 'users/register.html', context)
