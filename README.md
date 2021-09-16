# pymwp Demo Server

This is a simple Python Flask server that runs pymwp analysis.

### Available endpoints

| Path | Description |
:--- | :--- 
`/` | Displays server/pymwp version info
`/examples` | Lists all examples known to this demo server (in c_files directory)
`/{path}/{file}.c` | Analyze specified example, e.g. `basics/if.c` (must exist in c_files)


### Running locally

1. Install dependencies

```bash
# install dependencies
pip install -q -r requirements.txt

# run the server
python main.py
```

### Deployment

Server deployment runs automatically on commits to demo-server branch.

