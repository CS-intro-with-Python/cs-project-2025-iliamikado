FROM python:3.11-slim
WORKDIR /app
COPY . /app

# ENV FLASK_RUN_RELOAD=true

RUN pip install -r requirements.txt
CMD ["flask", "--app", "server.py", "run", "-h", "0.0.0.0", "-p", "5000"]