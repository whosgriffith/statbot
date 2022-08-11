FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /statbot
COPY requirements.txt /statbot/
RUN pip install -r requirements.txt
COPY . /statbot/