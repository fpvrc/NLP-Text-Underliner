def sleep():
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "google_app_credentials.json"
        client = vision.ImageAnnotatorClient()

        file_path = Listings.objects.all().filter(textracted=True).values('photo_main')[1]['photo_main']
        split_file_path = file_path.split('/')

        FILE_NAME = split_file_path[-1]

        split_file_path.remove(split_file_path[-1])
        split_file_path.insert(0,'media')
        join_folder_path = ['\\'.join(split_file_path)]

        FOULDER_PATH = join_folder_path[0]

        with io.open(os.path.join(FOULDER_PATH, FILE_NAME), 'rb') as image_file:
          content = image_file.read()

        image = vision.types.Image(content=content)
        
        response = client.text_detection(image=image)
        
        raw_json = response.text_annotations[0].description

        data = raw_json

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

        with open('{}{}.txt'.format(folder, file_name), 'a+') as f: #python opens a file {}{}.txt. Then .format passes in the {folder}{file_name} variables
          f.write(data)                                             # so python creates the file media/txt/2019/8/15/randomstring.txt and writes the data
        
        json_return = Jreturns(file_name = file_name, file_path = folder, user = request.user.id) # creates an instance of the Jreturns database model
        json_return.save() # saves the file name, file path, and user id to the db

      t = threading.Thread(target = sleep, name = 'thread1')
      t.start()