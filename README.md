# real-office


## Running RealOffice
Make sure you have **python3**

Create a virtualenv in this directory to keep versions same for everyone. Replace `<venv>` with a name of your choice e.g. `myvenv`.

`python3 -m venv <venv>`

Whenever you want to run, cd to this directory and run 

`source <venv>/bin/activate`

Your shell should have the prefix `(<venv>)`. To leave the virtualenv run `deactivate`.

For the first time you run RealOffice, install Django and possibly other requirements using
`pip install -r requirements.txt`

You might also have to run
`python manage.py migrate`

TO run the server,
`python manage.py runserver`