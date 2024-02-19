# FalconAI-Campaign-Backend

Front-end:
1. pip install -r requirements.txt or pip3 install -r requirements.txt
2. In the project directory, create a folder called "models" and download the model.
3. run project: streamlit run app.py

Setup Database:
1. Install Postgres SQL 16 from https://www.postgresql.org/download/macosx/
2. When installing postgres, make the postgres user password falconaidb123
3. Create the database
    1. Open up pgAdmin 4. Click server, and choose PostgreSQL version 16
    2. Right click on databases and create a new database with the name falcon_ai_db
4. python manage.py makemigrations
5. python manage.py migrate
6. python manage.py createsuperuser
    1. Email: test@falconai.com
    2. First Name: Super
    3. Last Name: User
    4. Password: falconai123

Back-end:
1. python3 manage.py runserver

