
# mini_eclass_template
Το mysite περιέχει μονο τον κώδικα της ιστοσελίδας και δεν περιέχονται τα virtual environments.Για να λειτουργήσει, τρέχουμε τα παρακάτω

```bash
python3 -m venv tutorial-env #dhmiourgia tou python virtual environment
cd tutorial-env	
git clone git@github.com:GeorgeGRz/mini_eclass_template.git #clone to repo
cd bin
source ./activate #activate to venv wste na valoume mesa ta packages
python -m pip install Django #egkatastasi django
python -m pip install django-ckeditor #egkatastasi ckeditor pou tha vreiastei gia to RTF
python -m pip install django-crispy-forms #forms pou dinoun bootstrap sta django forms
cd ../mini_eclass_template/mysite/ 
python manage.py runserver #trexeis ton server
```
Για να εχουμε την λειτουργία του chat, πρεπει να τρέχει ο αντίστοιχος chat server.Αφου μεταβούμε στον κατάλογο, τρεχουμε
```bash
docker-compose build
docker-compose up
```
