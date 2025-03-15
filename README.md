# Property and portfolio project

## Links

Using http://localhost:8000/
Fields that needs to be change in order for links to work is inside {} curly brackets with the field to put there like id is {id}

**Portfolio**
localhost:8000/api/portfolio

localhost:8000/api/portfolio/all
This will get all the portfolios with all fields

localhost:8000/api/portfolio/read/{id}/

localhost:8000/api/portfolio/create/
json string example to create portfolio
{
"name": "Name of portfolio",
"owner_of_portfolio": "Name of owner",
"geographic_region": "Europe"
}

localhost:8000/api/portfolio/update/{id}/

localhost:8000/api/portfolio/{id}/delete/
To delete in console use this:  
fetch("http://localhost:8000/api/portfolio/1/delete/", { method: "DELETE"}).then(response=>response.json()).then(data => console.log(data)).catch(error => console.error("Error:" , error ));

Example links to search or filter:  
localhost:8000/api/portfolio/?owner_of_portfolio=Name  
localhost:8000/api/portfolio/?geographic_region=Europe  
localhost:8000/api/portfolio/?name=Test&sort_name=asc  
localhost:8000/api/portfolio/?owner_of_portfolio=Test%20Tester&sort_owner_of_portfolio=desc  
localhost:8000/api/portfolio/?geographic_region=Europe&sort_geographic_region=as  
localhost:8000/api/portfolio/?name=Test&sort_name=asc&page=1

**Property**
localhost:8000/api/property/

localhost:8000/api/property/all/
This will get all the properties with all fields

localhost:8000/api/property/read/{id}/

localhost:8000/api/property/create/
json string example to create property
{
"address": "Testveien 9",
"zip_code": "7010",
"zip_place": "Trondheim",
"estimated_value": 5110.0,
"construction_year": 2019,
"usable_area": 5000.0,
"image": null,
"portfolio": 1
}

localhost:8000/api/property/update/{id}/

localhost:8000/api/property/{id}/delete/
To delete in console use this:  
fetch("http://localhost:8000/api/portfolio/{id}/delete/", { method: "DELETE"}).then(response=>response.json()).then(data => console.log(data)).catch(error => console.error("Error:" , error ));

Example links to search or filter:  
localhost:8000/api/property/?zip_place=Trondheim
localhost:8000/api/property/?address=Testveien
localhost:8000/api/property/?portfolio=1
localhost:8000/api/property/?min_value=100000&max_value=500000
localhost:8000/api/property/?min_year=2000&max_year=2020
localhost:8000/api/property/?sort_usable_area=asc
localhost:8000/api/property/?sort_zip_place=desc
localhost:8000/api/property/?sort_address=asc

## Guide to download and run.

### Step 1 - Clone project from Github

**With Github Desktop!**

- In the repostitory on Github click the "<> Code" button
- Then click on "Open with Github Desktop"
- Click "Choose" and navigate to your local directory where you want to clone the repostitory
- Click "Clone"

**With Git!**

- In the repostitory on Github click the "<> Code" button
- Check that the link is HTTPS and not SSH or GitHub CLI
- Click the two boxes to copy the link
- Open Git Bash
- Change to the directory where you want to clone the repostiotory
- Type "git clone" and paste the url EXAMPLE:git clone https://github.com/USERNAME/YOUR-REPOSITORY
- Press Enter to create your local clone

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

- Create an folder in the project that you name
  **Media**  
  This is for the images and the media file path, I ignored it for now to not share images and files.
  It should be in the outer directory of the project the same as portfolio, property, propertyPotfolio and files like README, env, requirements.txt etc

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
- If that dosen't work you have to install psycopg2 to run the shell. Type in:  
  pip install psycopg2
  and then type in this again  
  python manage.py shell
  from django.core.management.utils import get_random_secret_key
  print(get_random_secret_key())

  Copy the string into the env file SECRET_KEY
  To quit the django shell type in:  
  quit()
  And you should be back in the project terminal

Add all these fields to your env file

### Step 6 - Run migrations and start the server

- First run migration by type in:  
  python manage.py migrate

- Create an superuser by type in:  
  python manage.py createsuperuser

Fill in the fields in your terminal like username, email, password, password (again), and if the password isn't good enough for the validation choose y to buypass and N to not and run createsuperuser again with an allowed password.

- Start the server by type in:  
  python manage.py runserver
