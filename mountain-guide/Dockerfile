FROM python:3.8
RUN pip install fastapi uvicorn && pip install psycopg2 && pip install jinja2 && pip install python-multipart &&  pip install aiofiles
COPY ./app /home/app
COPY dbconfig.json /home
WORKDIR /home/app/main
CMD ["python3", "main.py"]