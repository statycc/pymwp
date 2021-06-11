# pymwp Demo Server

This is a simple Python Flask server that runs pymwp analysis.

Server URL: https://pymwp1.uk.r.appspot.com

How to run locally

1. Install dependencies

```
pip install -q -r requirements.txt
```

2. Run the server

```
python main.py
```

### Available endpoints

| Path | Description |
--- | --- 
`/` | Displays pymwp version info
`/examples` | Lists all examples known to this demo server 
`/{path}/{file}.c` | Analyze specified example, e.g. `basics/if.c`