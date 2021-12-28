git add .
git commit -am'ok'
git push heroku master


python manage.py makemigrations
python manage.py migrate