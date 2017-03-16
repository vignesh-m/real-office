# real-office


## Running RealOffice
Make sure you have **python3**

Create a virtualenv in this directory to keep versions same for everyone. Replace `<venv>` with a name of your choice e.g. `myvenv`.

`python3 -m venv <venv>`
`pip install -U pip`

Whenever you want to run, cd to this directory and run 

`source <venv>/bin/activate`

Your shell should have the prefix `(<venv>)`. To leave the virtualenv run `deactivate`.

For the first time you run RealOffice, install Django and possibly other requirements using
`pip install -r requirements.txt`

You might also have to run
`python manage.py migrate`

TO run the server,
`python manage.py runserver`

## Utilities
(vignesh): I've added shell_plus to make django shell stuff easier. Do `python manage.py shell_plus` to get
a shell better than default `python manage.py shell`

Users contains the list of already added users. If you add one, make an entry here so others can use it.

Use the admin pages (/admin), esp for exploring the objects present etc.