FROM python:latest
WORKDIR /statbot
COPY main.py ./
CMD [ "python", "./main.py"]