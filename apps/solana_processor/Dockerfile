FROM python:3.10

WORKDIR /opt/app

COPY . /opt/app

# RUN apk add --no-cache git build-base libffi-dev

RUN python -m pip install -r requirements.txt

CMD ["python", "main.py"]