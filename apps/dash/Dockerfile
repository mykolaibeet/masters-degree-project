FROM python:3.10
COPY . /opt/app
WORKDIR /opt/app
RUN pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 8099
CMD ["python", "app.py"]