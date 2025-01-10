# pymwp Demo Server

This is a simple Python Flask server that runs pymwp analysis.

To update the demo server, run the action workflow.
It should run necessary updates and deploy the change.
Server deployment runs automatically on commits to `demo` branch.
If the deployment fails, see below for troubleshooting notes.

### Endpoints

    https://{server-url}/v2/    Server base path

    REQUEST PATHS
    /                           Displays server and pymwp version info
    /examples                   Lists of all known examples
    /{path}/{file}.c            Analyze specified example
                                e.g. /basics/if.c (JSON response)

### Running locally

Install dependencies

     pip install -r requirements.txt

Run the server

     python main.py


### Troubleshooting deployment issues

#### `ERROR: (gcloud.app.deploy) Error Response: [9] Cloud build ... status: FAILURE An unexpected error occurred`

If there is a long break between deploys, the cloud build can get stuck in a weird state, where it looks for a previous image (but not found since long time), then fails to deploy.
The error on GH noted above, and more informative in the cloud build log _"ERROR: failed to initialize analyzer: getting previous image:..."_.
Then way to fix this is to deploy locally using `gcloud app deploy --no-cache` flag ([SO](https://stackoverflow.com/questions/77181996)).
I can't find a way to add `--no-cache` flag to the [deploy action](https://github.com/marketplace/actions/deploy-to-app-engine).

#### cpp system package availability on App Engine

On standard environment app engine only Ubuntu 18 has `cpp` system package. 
I don't think it is possible to parse C files on the Ubuntu 22 base image. 
The flex environment supports deploying a custom Docker.   


