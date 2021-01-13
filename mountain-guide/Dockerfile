FROM python:3.8
RUN pip install fastapi uvicorn && pip install psycopg2 && pip install jinja2 && pip install python-multipart
COPY ./app /home/app
COPY dbconfig.json /home
WORKDIR /home/app
CMD ["python3", "main.py"]