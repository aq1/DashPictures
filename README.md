## Pinterest Drawing Practice

### Create a sequence of pictures to draw from your boards and pins


#### Requirements

* Backend
    * Python 3
    * Django 2
    * Celery
    * Redis
* Frontend
    * Yarn
    * Angular


#### Installation
Assuming you have Python and venv already set up (not necessary, but very useful)

* Install packages `pip install -r requirements.txt`
* Create `local_settings.py` in `project/settings`
* Add `SECRET_KEY`, `PINTEREST_APP_ID`, `PINTEREST_APP_SECRET`, `PINTEREST_REDIRECT_URL` to `local_settings.py`
* In `dash_pictures/static/dash_pictures` run `yarn install`
* Run Celery (it downloads boards and pins) `celery -A dash_pictures.tasks.pinterest_tasks worker -l info`
* Run django server `python manage.py runserver`
