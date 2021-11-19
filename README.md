
	



	1) Install Python
		a. 3.7 x64 bit version so tensorflow works better
		Mac - https://www.udemy.com/python-django-dev-to-deployment/learn/lecture/12056118#content
		Windows - https://www.udemy.com/python-django-dev-to-deployment/learn/lecture/12056134#content

	2) VSCode setup
		a. Install python extension for VS code. The extension is "python"
			https://www.udemy.com/python-django-dev-to-deployment/learn/lecture/12056150#overview

	3) Virtual Environment - using virtualenv
		https://www.udemy.com/python-django-dev-to-deployment/learn/lecture/12056252#overview
		a. Note - the virtualenv environments worked better than anaconda for me
			i. On windows I had to set an execution policy to All to get the virtualenv to work
		b. I have a virtual environment called venv inside the directory flowzo_project
			i. (venv) PS C:\Users\jari\dev\flowzo_project>

	4) Install Django
		a.  pip intsall django
			https://www.udemy.com/python-django-dev-to-deployment/learn/lecture/12056264#overview

	5) Start Django Project
		a.  start a django project with the cmd: django-admin startproject flowzo .
		b. You should see a few files and folders pop up within (venv) PS C:\Users\jari\dev\flowzo_project>flowzo

	6) For VS code
		a. Select python interpreter as your venv python
		b. Install the python lynter
			at 3:30 sec https://www.udemy.com/python-django-dev-to-deployment/learn/lecture/12056264#overview

	7) Git pull
		a. Clone the repository: https://github.com/fpvrc/project_flow.git
		b. Replace all the files within the "flowzo" project directory (except your virtual env directory) with the files from the git repository (better way to do this? Lol). Make sure to delete the original files that were created when you started the project.
	
	8) Install Postgres
		https://www.udemy.com/python-django-dev-to-deployment/learn/lecture/12056336#overview
		a. When asked while installing, use the password 'jari' - this password is in django settings that was pulled from git. We can change this, just have to make sure were all using the same password
		b. After installing, another window should pop up. When asked to install other things, install the database driver psqlODBC under 'database drivers'.

	9) Create a database
		Mac - https://www.udemy.com/python-django-dev-to-deployment/learn/lecture/12056336#overview
		The following is for windows
		a. In the cortana search bar, type 'ps' there should be a psql shell to open
		b. Tap enter and enter the default database
			i. Tap enter until your within the database shell
		c. Create database with command CREATE DATABASE flowzodb OWNER postgres;
		d. \l to see the list of databases 
		e. In the cortana search bar, type 'pgA' you should see pgAdmin
		f. Open pg admin and enter the database password
		g. Open directories until you see flowzodb
			i. Right click and enter properties
			ii. Click on security
			iii. Add the guaratee as the postgres user and select 'ALL' for security

	10) Pip install in the enviorment
		a.  pip install psycopg2-binary
		b.  pip install pandas
		c.  pip install google-cloud-vision
		d.  pip install pillow
		e.	Install CUDA 10 (https://developer.nvidia.com/cuda-10.0-download-archive?target_os=Windows&target_arch=x86_64&target_version=10)
		f. 	pip install pytorch (pip3 install torch===1.2.0 torchvision===0.4.0 -f https://download.pytorch.org/whl/torch_stable.html)
		g. Uninstall any versions of spacy ("pip freeze" to see installed packages in enviorment) pip uninstall spacy
		h. pip install spacy==2.1.3
		i. pip install bert-extractive-summarizer
	
	11) Migrate the models to the database
		@ 4:30 https://www.udemy.com/python-django-dev-to-deployment/learn/lecture/12056356#overview
		a.  python manage.py makemigrations
		b.  python manage.py migrate

	12) Final setup
		a. Run the server with cmd: python manage.py runserver
		b. Create a user account
			i. In the browser, go to http://127.0.0.1:8000/accounts/register
				1) Create a user account
				2) In the upper right corner, tap the user icon and tap "sign in"

	13) Basic Functionality
		a. Once logged in, you should be able click on the left menu item "dashboard". You should alsco be able to create new readings
		b. after a reading is created, you should be able to click on the reading and drag and drop photo files into the reading
		c. Once you drop a photo into the reading, the method in accounts/views.py "def pages():" will be called.
		b. As of now, once you drop a photo into the reading, the summaries for the photos will be returned to the terminal
		e. Ather information about the summaries like file locations, foreign keys and such are also stored in the database
			the shared spreadsheet has the database structure lined out.
