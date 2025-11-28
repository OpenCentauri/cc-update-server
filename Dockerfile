FROM python:3.13-alpine
WORKDIR /app
COPY *.py requirements.txt /app/
RUN sudo apk add openssl && pip install -r requirements.txt
ENTRYPOINT ["python3", "./main.py"]