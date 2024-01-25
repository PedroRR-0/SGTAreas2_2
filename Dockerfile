FROM python:3.12-slim

# install needed packages

# clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD gunicorn SGTAreas2_2.wsgi