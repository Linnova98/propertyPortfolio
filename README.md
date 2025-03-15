# Property and portfolio project

## How to download and run on other computer.

### Step 1 - Clone project from Github

**With Github Desktop!**

- In the repostitory on Github click the "<> Code" button
- Then click on "Open with Github Desktop"
- Click "Choose" and navigate to your local directory where you want to clone the repostitory
- Click "Clone"

**_With Git!_**

- In the repostitory on Github click the "<> Code" button
- Check that the link is HTTPS and not SSH or GitHub CLI
- Click the two boxes to copy the link
- Open Git Bash
- Change to the directory where you want to clone the repostiotory
- Type "git clone" and paste the url EXAMPLE:git clone https://github.com/USERNAME/YOUR-REPOSITORY
- Pres Enter to create your local clone

### Step 2 - Create virtual environment

- Open and terminal and go the the directory where you have the project
- Type  
  python -m venv {your environment name}
- Activate the environment by typing  
  {your environment name}\Scripts\activate
- Go into the project in your environment, which if it's inside the same directory should be  
  cd propertyPortfolio

### Step 3 - Install requirements

- Install the requirements by typing in  
  pip install -r requirements.txt

### Step 4 - Configure your .env file and media folder

- Create and environment file in the project directly in your IDE or by typing **touch .env** in your terminal
- Add these fields, and later fill in the data  
  SECRET_KEY  
  DB_NAME  
  DB_USER  
  DB_PASSWORD  
  DB_HOST  
  DB_PORT

This is added here for some extra security to not leak any keys or passwords by using environ

- Create an folder in the project that you name **Media**  
  This is for the images and the media file path

### Step 5 - Configure a PostgreSQL database

- Create your database with pgAdmin
- Open pgAdmin and log in
- In the version you want to use right click and choose create -> database and follow the steps there
- When you database is configured you'll need to find the data for your env file.
- To find NAME and USER right click on your database and go to properties
- To find HOST and PORT right click on the version of postgreSQL that you use and go to properties -> connections

To create a SECRET_KEY you could use Django

- Go to your termnial and type in:
  python manage.py shell
  from django.core.management.utils import get_random_secret_key
  print(get_random_secret_key())

Add all these fields to your env file

### Step 6 - Run migrations and start the server

- First run migration by type in  
  python manage.py migrate

- Create an superuser by type in  
  python manage.py createsuperuser

Fill in the fields in your terminal like username, email, password, password (again), and if the password isn't good enough for the validation choose y to buypass and N to not and run createsuperuser again with an allowed password.

- Start the server by type in  
  python manage.py runserver
