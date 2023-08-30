# EasyFreezey
A CRUD app for managing bulk cooking of freezer meals.

## How to run things

These commands are for Linux because it's good.

### Install and activate python environment

From the git root:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run dev backend

```bash
cp samples/easy-freezey.db .
python -m server.app
```

### Run backend tests

`python -m pytest server/tests`

### Install react environment

```bash
cd client
npm install
```

### Run frontend (after running backend)

`npm start`
