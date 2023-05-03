FROM python:latest
WORKDIR /poll

RUN apt-get update
RUN python3 -m venv prod

# Copy app to the current directory within the docker container
COPY . .

RUN prod/bin/pip install --upgrade pip
RUN prod/bin/pip install -e .

CMD prod/bin/python3 drawbot
