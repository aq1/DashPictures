## Pinterest Drawing Practice

### Create a sequence of pictures to draw from your boards and pins


#### Requirements

* Backend
    * Python 3
    * Django 2
    * Redis
    * PostgreSQL (for production only, sqlite is fine for test run)
* Frontend
    * Vue


#### Installation
Assuming you have Python and venv already set up (not necessary, but very useful)

* Install packages `pip install -r requirements.txt`
* Create `local_settings.py` in `project/settings`
* Add `SECRET_KEY`, `PINTEREST_APP_ID`, `PINTEREST_APP_SECRET`, `PINTEREST_REDIRECT_URL` to `local_settings.py`
* In `dash_pictures/static/dash_pictures` run `npm install`
* Run django server `python manage.py runserver`
