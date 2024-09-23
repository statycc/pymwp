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
pip install -r requirements.txt

# run the server
python main.py
```

### Deployment

Server deployment runs automatically on commits to `demo` branch.

If there is a long break between deploys, the cloud build can get stuck in a weird state, where it looks for a previous image (but not found since long time), then fails to deploy. 
The error looks like _"ERROR: (gcloud.app.deploy) Error Response: [9] Cloud build ... status: FAILURE An unexpected error occurred."_ on GH,
and more informative in the cloud build log _"ERROR: failed to initialize analyzer: getting previous image:..."_.

Then way to fix this is to deploy locally using `--no-cache` flag[^1]:

```
gcloud app deploy --no-cache
```

I can't find a way to add `--no-cache` flag to the [deploy action](https://github.com/marketplace/actions/deploy-to-app-engine), so I will leave this note-to-self here.

[^1]: [https://stackoverflow.com/questions/76692347](https://stackoverflow.com/questions/77181996/gcloud-build-failure-error-failed-to-initialize-analyzer-no-such-object)
