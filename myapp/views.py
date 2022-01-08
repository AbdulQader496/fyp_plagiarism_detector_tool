from re import match
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from pandas.core import frame
from pandas.core.frame import DataFrame
from requests.api import request
from myapp.models import Document
from myapp.forms import DocumentForm
from __main__ import *
import pandas as pd
import nltk
from nltk import data
from nltk.tokenize import punkt
from nltk.translate.bleu_score import sentence_bleu
from pandas.core.frame import DataFrame
from difflib import SequenceMatcher
import pandas as pd
from bs4 import BeautifulSoup as bs
import warnings
import requests
import json
import pymongo


def doc_From_REP():
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    #DB name
    db = client['fypdjangoplag']
    #Collection
    coll = db['myapp_document']
    x = coll.find({}, {'fileData':1, '_id':0})
    y = []
    for doc in x:
        if 'fileData' in doc:
            y.append(doc['fileData'])
    return y




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
    global run 
    run = doc_From_REP()
    
    # Handel file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            #Process for handeling the file and store it on mongodb
            newdoc = Document(docfile = request.FILES['docfile'])
            #Contain process for extracting data in a file and storing them in DB as textfield
            newdoc.fileData = request.FILES['docfile'].read()
            newdoc.username = request.user            
            newdoc.save()
            # Redirect to the document list after post
            
            plagFromNET(newdoc.fileData)
            plagFromREP(newdoc.fileData)            
            # context = {plag_object1, plag_object2}
            # frames = [plag_object1, plag_object2]
            # context = pd.concat(frames)
            return render(request, 'report.html', {'d': data1, 'b': data2})
    else:
        form = DocumentForm() #A empty, unbound form
            
    # Load documents for the list page
    documents = Document.objects.filter(username=request.user)

    # Render list page with the documents and the form
    return render(request,
        'home.html',
        {'documents': documents, 'form': form}) 



              
#Contain process for deleting a file from DB (mongoDB)

def delete_file(request, id):    
    if request.method == 'POST':
        document = Document.objects.get( id=id)
        document.delete()
    return redirect('fileupload')


nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(nltk.corpus.stopwords.words('english'))


# Plagiarism detection process

    

#Function that is responsible to move the string of data and
# to produce percentage of similarity
def plagFromNET(textFromFile):

   #print(textFromFile)

   return returnTableWithURL(report(str(textFromFile)))

def plagFromREP(textFromFile):
    #print(textFromFile)
    # print("Rep responding")
    return returnTableWithURL2(reportREP(str(textFromFile)))

# This function tokenize the words in the sentence/s

def purifyTxt(textFromFile):
    words = nltk.word_tokenize(textFromFile)
    return (" ".join([word for word in words if word not in stop_words]))

# This function helps to get the similar data/links from internet
# using bing as search engine. takes 2 parameter 

def webVerify(textFromFile, result_per_sentence):
    sentencess = nltk.sent_tokenize(textFromFile)
    matching_sites = []
    for url in searchBing(query = textFromFile, num = result_per_sentence):
        matching_sites.append(url)

    for sentence in sentencess:
        for url in searchBing(query = sentence, num = result_per_sentence):
            matching_sites.append(url)

    return (list(set(matching_sites)))

#Produce the percentage of similarity

def Similarity(st1,st2):
    return (SequenceMatcher(None,st1,st2).ratio())*100

def Similarity2(st1,st2):
    return (SequenceMatcher(None,st1,st2).ratio())*100
# Creates a dict of similar links 

def report(textFromFile):
    matching_sites = webVerify(purifyTxt(textFromFile), 2)
    matches = {}

    for i in range(len(matching_sites)):
        matches[matching_sites[i]] = Similarity(textFromFile, extractText(matching_sites[i]))
    
    matches = {a: b for a, b in sorted(matches.items(), key=lambda item: item[1], reverse=True)}
    return matches





def reportREP(textFromFile):
    doc = run   
    matches= {}
    for i in range(len(doc)):
        matches[doc[i]] = Similarity2(textFromFile, doc[i])
    
    matches = {a: b for a, b in sorted(matches.items(), key=lambda item: item[1], reverse=True)}
    
    return matches

# Return the table with matching links.

def returnTableWithURL(dictionary):

    df = pd.DataFrame({'Similarity':dictionary})
    print(df)
    # result = df.to_html()
    # print(result)
    json_records = df.reset_index().to_json(orient='records')
    global data1
    data1 = []
    data1 = json.loads(json_records)
    global  plag_object1
    plag_object1 = {'d' : data1}
    #print(plag_object1)
    #print(plag_object)
    # plag_object = df
    
    return plag_object1

def returnTableWithURL2(dictionary):

    df = pd.DataFrame({'Similarity':dictionary})
    json_records = df.reset_index().to_json(orient='records')
    global data2
    data2 = []
    data2 = json.loads(json_records)
    global  plag_object2
    plag_object2 = {'b' : data2}
    
    #print(plag_object)
    # plag_object = df
    
    # print(plag_object2)
    return plag_object2

warnings.filterwarnings('ignore', module='bs4')

# Search on the internet

def searchBing(query, num):

    url = 'https://www.bing.com/search?q=' + query
    urls = []

    page = requests.get(url, headers= {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'})
    soup = bs(page.text, 'html.parser')

    for link in soup.find_all('a'):
        url = str(link.get('href'))
        if url.startswith('http'):
            if not url.startswith('http://go.m') and not url.startswith('https://go.m'):
                urls.append(url)

    return urls[:num]

# Extraxt text from the internet (from similar website)

def extractText(url):
    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    return soup.get_text()



    