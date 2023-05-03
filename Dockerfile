FROM python:latest
WORKDIR /poll

RUN apt-get update

# Copy app to the current directory within the docker container
COPY . .
RUN make fclean
COPY vars/config.json vars/config.json
RUN python3 -m venv prod

RUN prod/bin/pip install --upgrade pip
RUN prod/bin/pip install -e .

CMD prod/bin/python3 drawbot
