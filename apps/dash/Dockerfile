FROM python:3.10

WORKDIR /opt/app

COPY . /opt/app

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "app.py"]

