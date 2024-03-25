# Users managent (wufwuf)

## Run

### Run locally

Define the application's config in an .env file with the following content:

```
# APP CONFIG
SECRET_KEY={secret}
TOKEN_EXP_SECONDS={expiration time in seconds}

# DATABASE CONFIG
DATABASE_USER={database-user}
DATABASE_NAME={database-name}
DATABASE_PASSWORD={database-password}
DATABASE_PORT={database-port}
DATABASE_HOST={database-host}

```

Create virtual environment

```
python3 -m venv venv
```

Activate virtual environment
```
source venv/bin/activate
```

Install dependencies
```
pip3 install -r requirements.txt
```

Create database initial sample data
```
python3 db.py
```

Run main app
```
uvicorn main:app
```

Look at examples and documentation at http://localhost:8000/docs

