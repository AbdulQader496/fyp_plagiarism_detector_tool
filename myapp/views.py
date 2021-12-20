from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from myapp.models import Document
from myapp.forms import DocumentForm
from bs4 import BeautifulSoup

from myproject.plagDetection.main import result


#index view. Contain sign up process

def index(request):
   
    if request.method == 'POST':   
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['pass']
        password2 = request.POST['password2']
    

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('index')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('index')
            elif username =="" or email =="" or password =="" or password2 =="" :
                messages.info(request, 'Fields are empty')
                return redirect('index')
            else: 
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('signin')
        else:
            messages.info(request, 'Password not same')
            return redirect('index')
    else:
        return render(request, 'index.html')

# Contain sign in process

@csrf_protect
def signin(request):

    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        print(username)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else: 
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')
    else:
        return render (request, 'signin.html')

# Contain action after login. Home page

def home(request):
    return render (request, 'home.html')

# Contain logout/signout process

def logout(request):
    auth.logout(request)
    return render (request, 'signin.html')

# Contain process for uploading a file with user id

def fileupload(request):
    # Handel file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            #Process for handeling the file snd store it on mongodb
            newdoc = Document(docfile = request.FILES['docfile'])
            #Contain process for extracting data in a file and storing them in DB as textfield
            newdoc.fileData = request.FILES['docfile'].read()
            newdoc.username = request.user            
            newdoc.save()
            # Redirect to the document list after post
            result(newdoc.fileData)
            return render(request, 'report.html')
    else:
        form = DocumentForm() #A empty, unbound form
            
    # Load documents for the list page
    documents = Document.objects.filter(username=request.user)

    # Render list page with the documents and the form
    return render(request,
        'home.html',
        {'documents': documents, 'form': form},) 

              
#Contain process for deleting a file from DB (mongoDB)

def delete_file(request, id):    
    if request.method == 'POST':
        document = Document.objects.get( id=id)
        document.delete()
    return redirect('fileupload')

    