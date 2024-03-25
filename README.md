# Users managent (wufwuf)

## Run

### Run locally

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
