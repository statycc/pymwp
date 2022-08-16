# pymwp Demo Server

This is a simple Python Flask server that runs pymwp analysis.

### Available endpoints

**Base path**

```
https://{server-url}/v2/
```

| Path               | Description                                                            |
|:-------------------|:-----------------------------------------------------------------------|
| `/`                | Displays server/pymwp version info                                     |
| `/examples`        | Lists all examples known to this demo server (in c_files directory)    |
| `/{path}/{file}.c` | Analyze specified example, e.g. `basics/if.c` Returns a JSON response. |

### Running locally

```bash
# install dependencies
pip install -q -r requirements.txt

# run the server
python main.py
```

### Deployment

Server deployment runs automatically on commits to `demo` branch.

