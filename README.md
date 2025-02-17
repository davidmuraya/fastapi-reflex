## FastAPI + Reflex.

This is an experiment to attempt to use Reflex as the frontend framework for a FastAPI app.
THis may be useful for if you already have a FastAPI application and want to use some frontend a JS framework for parts of your as the frontend.

The frontend application is a simple app to manage customer data. It is based in the [customer_data](https://cijob.reflex.run/) example from the Reflex repo. I have moved the database functionality from the reflex app to FastAPI.

## How to run the app:

This app is a FastAPI app that uses Reflex as the frontend framework.

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Navigate to the app/frontend/customer_app directory:


3. To run the reflex app, navigate to the app/frontend directory and run the following command:

```bash
reflex run
```

This will start the Reflex app. The frontend app will be available at http://localhost:3000.
The reflex backend app will be start in http://localhost:8000. This backend is used to serve the state of the Reflex app.

Default rxconfig.py file:

```python

import reflex as rx

origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:5000",
    "http://127.0.0.1:5000",
]


config = rx.Config(
    app_name="frontend",
    show_built_with_reflex=False,
    cors_allowed_origins=origins,
    backend_port=8000,
    frontend_port=3000,
)
```

4. To start the fastapi backend app, navigate to the app directory and run the following command:

```bash
uvicorn app.main:app --reload --port 5000
```

This will start the fastapi backend app. The backend app will be available at http://localhost:5000.

5. You can now develop the frontend app and the backend app simultaneously.

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