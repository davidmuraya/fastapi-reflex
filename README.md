## FastAPI + Reflex.

This is an experiment to attempt to use Reflex to develop a frontend application for a FastAPI app.
This may be useful for if you already have a FastAPI application and want to use a JS framework for parts of your as the frontend.

The frontend application is a simple app to manage customer data. It is based in the [customer_data](https://cijob.reflex.run/) example from the Reflex repo. I have moved the database functionality from the reflex app to FastAPI.

## How to develop the app on your local machine:

This app is a FastAPI app that uses Reflex as the frontend framework. You will need to run both the FastAPI backend and the Reflex App.

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Create and .env file in the root directory of the project. The .env file should contain the following variables:

```bash
FASTAPI_HOST="http://127.0.0.1:5000"
```

**Remember to replace the IP address/server name above with the actual IP address/server name of your server when deploying the app.**


3. To run the reflex app, navigate to the app/frontend directory and run the following command:

```bash
reflex run
```

This will start the Reflex app. The frontend app will be available at http://localhost:3000.
The reflex backend app will be start in http://localhost:8000. This backend is used to serve the state of the Reflex app.

Default rxconfig.py file:

```python

"""
rxconfig.py contains the configuration for Reflex.
"""

import reflex as rx
from customer_data.config import settings

prod_origins = ["http://127.0.0.1", f"{settings.fastapi_host}"]

dev_origins = ["*"]


config = rx.Config(
    app_name="customer_data",
    show_built_with_reflex=False,
    cors_allowed_origins=prod_origins,
    telemetry_enabled=False,
    backend_port=8001,
    frontend_port=3000,
    loglevel="debug",
    db_url=None,
    backend_host="127.0.0.1",
    gunicorn_worker_class="uvicorn.workers.UvicornH11Worker",
    gunicorn_workers=4,  # Set number of worker processes
    # api_url="http://127.0.0.1:8001",
    is_reflex_cloud=False,
)


```

4. To start the fastapi backend app, navigate to the app directory and run the following command:

```bash
uvicorn app.backend.main:app --reload --port 5000
```

This will start the fastapi backend app. The backend app will be available at http://localhost:5000.

5. You can now develop the frontend app and the backend app simultaneously.


## How to deploy the app:

6. Once you are done developing the frontend app, export the Reflex app by running the following command:

```bash
 reflex export --no-zip --frontend-only
```

The frontend is a compiled NextJS app, which can be deployed to a static hosting service like Github Pages or Vercel.
This is what the fastapi app is serving.


7. To run the backend state for the frontend app, navigate to the app/frontend directory and run the following command:
```bash
 reflex run --backend-only
```

### Reflex Command Line Interface
To learn more about Reflex CLI, visit the [Reflex CLI](https://reflex.dev/docs/api-reference/cli/) page.


# Production Setup

You will need to set up 2 applications/services:
1. A fastapi that is available to the public.
2. A backend service by reflex that is only called by the frontend fastapi application.
The fastapi calls it via wss://xxx.xxxx.xxx, and is the request is forwarded to http://127.0.0.1
This service maintains the state of the application. This is a reflex backend.

## Creating the FastAPI Application
Create this as you would like. In my example, I have called the service fastapi-reflex. I am using a socket.

Under /etc/systemd/system create the service file:

```bash
sudo nano /etc/systemd/system/fastapi-reflex.service
```


```bash


[Unit]
Description=Gunicorn instance to serve FastAPI Reflex
After=network.target

[Service]
User=username
Group=www-data
WorkingDirectory=/usr/share/nginx/fastapi-reflex
Environment="PATH=/usr/share/nginx/fastapi-reflex/venv/bin"
ExecStart=/usr/share/nginx/fastapi-reflex/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.backend.main:app -b unix:/var/sockets/fastapi-reflex/fastapi-reflex.sock -m 007 -t 5400 --max-requests 1000 --max-requests-jitter 50
Restart=always

[Install]
WantedBy=multi-user.target




```

## Creating the Reflex Backend Service

Under /etc/systemd/system create the service file:

```bash
sudo nano /etc/systemd/system/reflex-backend.service
```

Copy/Adjust the following code into the file:
**Note:** Set the desired username and Group below.

```bash
[Unit]
Description=Gunicorn instance to serve Reflex Backend Service
After=network.target

[Service]
User=username
Group=www-data
WorkingDirectory=/usr/share/nginx/fastapi-reflex/app/frontend/customer_app
Environment="PATH=/usr/share/nginx/fastapi-reflex/venv/bin"
ExecStart=/usr/share/nginx/fastapi-reflex/venv/bin/reflex run --env prod --backend-only
Restart=always

[Install]
WantedBy=multi-user.target

```



## Automated Deployment in a Production environment
You will need to have a git repository, initialized with a remote repository.

#### Example:

```bash
git init

git remote add origin https://github.com/davidmuraya/fastapi-reflex
```


You can now run the following command to deploy the app:

```bash
chmod +x deploy.sh; ./deploy.sh
```

This will give the deploy.sh execution persmissions, update the repository, activate the virtual environment, install the requirements, export the frontend app, restart the services, and deactivate the virtual environment.