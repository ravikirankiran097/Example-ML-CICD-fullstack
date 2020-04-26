FROM python:3.7.6
MAINTAINER NasrudinSalim "Nasrudin.Salim.Suden@gmail.com"

# s2 geometry
RUN apt-get update -y \
    && apt-get install -y \
    apt-utils \
    cmake \
    libgflags-dev \
    libgoogle-glog-dev \
    libgtest-dev \
    libssl-dev \
    swig

COPY requirements.txt /requirements.txt
RUN pip3 install --upgrade pip && \
    pip3 install -r /requirements.txt

# Credentials
ARG google_credentials=google_secrets.json
COPY $google_credentials /flask-api/google_secrets.json
ENV GOOGLE_APPLICATION_CREDENTIALS="/flask-api/google_secrets.json"

COPY . /flask-api
WORKDIR /flask-api

EXPOSE 8080
ENTRYPOINT ["gunicorn"]
CMD ["-w", "4", "-t", "3600", "-b", "0.0.0.0:8080", "webservice:application"]
