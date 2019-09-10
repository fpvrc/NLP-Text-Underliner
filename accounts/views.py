import os
import io
import pandas as pd
import time
import threading
import json
import datetime
import random
import string
from google.cloud import vision
from google.cloud.vision import types
from google.protobuf.json_format import MessageToJson
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Listings, Jreturns, File, Sum
from .forms import Upload, newReading, FileForm
from django.conf import settings
from django.http import JsonResponse
from django.urls import resolve
from summarizer import SingleModel

def register(request):
  if request.method == 'POST':
    # Get form values
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

    # Check if passwords match
    if password == password2:
      # Check username
      if User.objects.filter(username=username).exists():
        return redirect('register')
      else:
        if User.objects.filter(email=email).exists():
          return redirect('register')
        else:
          # Looks good
          user = User.objects.create_user(username=username, password=password,email=email, first_name=first_name, last_name=last_name)
          user.save()
          return redirect('login')
    else:
      return redirect('register')
  else:
    return render(request, 'accounts/register.html')

def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
      auth.login(request, user)
      return redirect('dashboard')
    else:
      return redirect('login')
  else:
    return render(request, 'accounts/login.html')

def pages(request, reading_id=None):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()   #saves the form
            photo_id = photo.pk    # Saves the primary key of the uploaded photo to the "photo_id" var       
            model = File.objects.get(id=photo_id) # Uses the saved primary key to load the uploaded photo model

            model.reading = reading_id #The reading ID is assigned to the photo model. This way we can tell what photos belong to which readings
                                        # the reading ID is passed in through the URL when the user clicks into the specific reading page
            user = request.user.id # Assigned the user ID to a var so we can use this var to know what users uploaded what
            model.user = user #Here we assign the user ID to the user field so we know what user uploaded the photo

            file_path = model.file.name # Saves the file path of the uploaded file to the "file_paths" veriable
            model.save() # saves the model. Know the uploaded photo is in the database

            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url, } #This line does something with the front end
                  #pretty sure the above line handles updating the page with the drag and drop upload functionality
            def sleep(): # Here we define the method for extracting the text from images and also the summarizer method
              os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "google_app_credentials.json" #location to the file with our google account credentials
              client = vision.ImageAnnotatorClient()

              split_file_path = file_path.split('/') #splits the file path "photos/media/date/" into a list [photos,media,date,file.txt]

              FILE_NAME = split_file_path[-1] #takes the last element of the list which is the file name and assigns it to a variable

              split_file_path.remove(split_file_path[-1]) # then removes the file name so all were left with is the folder paths
              split_file_path.insert(0,'media')
              join_folder_path = ['\\'.join(split_file_path)] #joins the folder path list back together so we have a string that is the folder path

              FOULDER_PATH = join_folder_path[0]

              with io.open(os.path.join(FOULDER_PATH, FILE_NAME), 'rb') as image_file: #opens the above image file
                content = image_file.read() 

              image = vision.types.Image(content=content)
              
              response = client.text_detection(image=image)
              
              raw_json = response.text_annotations[0].description #convert raw json to txt

              returns = raw_json

              today = datetime.date.today()
              folder_no_date = 'media/txt/{}/{}/{}/' # creates a string that defines the folder to store the txt file to
              folder = (folder_no_date.format(today.year, today.month, today.day)) # then pass in the year, month, and day into the folder string
                                                                                    # so the folder string is 'media/txt/2019/8/15' or the current date

              def randomString(stringLength=4):         # creates a random string that we can use to name the response file from google
                letters = string.ascii_lowercase
                return ''.join(random.choice(letters) for i in range(stringLength))

              file_name = '{}'.format(randomString()) # then we pass in the random string so the file name is just som random string

              try:                                    # if the folder has not been created for that day, create the folder
                os.makedirs(folder)
              except FileExistsError:                 # folder already exists
                pass

              new_file = '{}{}.txt'.format(folder, file_name) #Here we pass in the folder and random string file name.
              with open(new_file, 'a+') as f: #python opens the new file that we can use to write the response from google to
                f.write(returns)                                             # so python creates the file media/txt/2019/8/15/randomstring.txt and writes the data
              
                foreign_key = photo_id #here we assign the photo id to a foreign key variable so we can define what txt are from what photos
                returned_text = Jreturns.objects.create(file_path=new_file, photo_id=foreign_key, user=user) #here we create a new object for the txt
                returned_text.save()

              with open(new_file, 'r') as f: #here we open the text file that we saved from google
                body = f.read()
                model = SingleModel() #Here we perfrom the summarization

                result = model(body, ratio=(1/2), min_length=60) #here we define how long the summary should be (the ratio of input txt to output txt)
                full = ''.join(result)

                folder_no_date_sum = 'media/sum/{}/{}/{}/' # creates a string that defines the folder to store the txt file to
                folder_sum = (folder_no_date_sum.format(today.year, today.month, today.day))
                try:                                    # if the folder has not been created for that day, create the folder
                  os.makedirs(folder_sum)
                except FileExistsError:                 # folder already exists
                  pass

                file_name_sum = '{}'.format(randomString())
                new_file_sum = '{}{}.txt'.format(folder_sum, file_name_sum) #here we create another string for the new folder and file path for the summary file

                with open(new_file_sum, 'a+') as f: #here we use the new folder and file string above to open a new file
                  f.write(full)                 # this is were we pass in the returned summary text into the new file
                
                  returned_text = Sum.objects.create(file_path=new_file_sum, photo_id=foreign_key, user=user) #here we create a new Sum object to store info about the summary file
                  returned_text.save() #notice that we save the photo_id so we know what photo the summary belongs to

                  print(full) #here we print the summary

            t = threading.Thread(target = sleep, name = 'thread1') #this is where we define two threads so the processing can take place behind the scenes
            t.start()
              
        else:
            data = {'is_valid': False}

        return JsonResponse(data)
    else:
        user = request.user
        listings = Listings.objects.filter(id=reading_id, user=user)
        photos = File.objects.filter(reading=reading_id)
        # return render(request, 'accounts/pages.html')
        return render(request, 'accounts/pages.html', {'photos': photos , 'listings': listings})

def clear_database(request): #this is a method to clear the database. Note you still have to delete the files from media
    for photo in File.objects.all():
        photo.file.delete()
        photo.delete()
    for jreturns in Jreturns.objects.all():
        jreturns.delete()
    for summ in Sum.objects.all():
        summ.delete()

    return redirect(request.POST.get('next'))

def dashboard(request):
  if request.method == "POST":
    form = newReading(request.POST, request.FILES)
    if form.is_valid():
      upload_form = Listings(title = form.cleaned_data['title'])
      upload_form.user = request.user # is it request.user.id??
      upload_form.save()

      #AI method

      return redirect('dashboard')
  
  else:
    user = request.user
    form = newReading()
    {'form': form}
    listings = Listings.objects.filter(user=user)

    return render(request, 'accounts/dashboard.html', {'form': form,'listings': listings})

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('index')

def upload(request):
  if request.method == "POST":
    uploaded_file = request.FILES['document']
    return render(request, 'accounts/dashboard.html')
  else:
    return render(request, 'accounts/dashboard.html')