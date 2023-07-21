gunicorn -w 2 -k uvicorn.workers.UvicornWorker app.app:app -b 0.0.0.0:8090 &
gunicorn -w 2 -k uvicorn.workers.UvicornWorker authapp.app:app -b 0.0.0.0:8080 &
gunicorn -w 2 -b 0.0.0.0:8070 frontend.app:app