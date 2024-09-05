FROM python:3.11.5
WORKDIR pymwp
COPY . .
RUN pip install -r requirements-dev.txt