# Token refresh system.
A JWT based token refresh system for sysytem authentication and authorization. 

## Programming language and Framework used:
1. Used **python** as the core programming language because it's a high level programming language, which allows us to focus on core functionality of the application by taking care of common programming tasks.
2. Used **django** as the web framework that helps in rapid development and clean, pragmatic design. In django we define models for the database using Python. While we can write raw SQL, for the most part the Django ORM handles all the database migrations and queries.    
3. And **django-restframework** as the library to build Rest APIs in django because it makes serialization very easy. Also, it’s customizable all the way down. We can use regular function-based views if we don’t need the more powerful features and used and trusted by internationally recognized companies including Mozilla, Red Hat, Heroku, and Eventbrite.

## Installing Dependencies

### Cloning the repo
  - ```
    git clone https://github.com/satyarth12/Token-refresh-system.git
    ```
  - Installing all the project dependencies listed in the Pipfile
    **USING PIPENV**
    ```
    pip install pipenv
    pipenv shell
    pipenv install -r requirements.txt
    ```

## Runnin the test case
  - This command will run the test case of this project.
  ```
  cd auth_system
  python manage.py test
  ```

## Running the Django Backend Server
  - NOTE: Be in the auth_system dir to run the server
   ```
   cd auth_system
   ```
   ### Running migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

   ### Creating superuser
   - This command will create your superuser account and authorize you to access the admin pannel
   ```
   python manage.py createsuperuser
   ```
   - Login to http://127.0.0.1:8000/admin/ to access the admin pannel.

  ### Running the local server

  ```
  python manage.py runserver
  ```
  - This will run the django server and you can access all the endpoints of the this project.
  - Read the Swagger doc at http://127.0.0.1:8000/, after running the local server.

  