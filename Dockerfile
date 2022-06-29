# pull official base image
# FROM python:3.8

# # set work directory
# WORKDIR /usr/src/app

# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# RUN apt-get update && apt-get install -y postgresql-server-dev-all gcc python3-dev musl-dev gdal-bin libgdal-dev g++

# # install dependencies
# RUN pip install --upgrade pip
# COPY ./requirements.txt /usr/src/app/requirements.txt
# RUN export LDFLAGS="-L/usr/local/opt/openssl/lib"
# RUN pip install -r requirements.txt
# RUN pip install -v https://github.com/pallets/werkzeug/archive/refs/tags/2.0.1.tar.gz

# # copy project
# COPY . /usr/src/app/

# EXPOSE 8080
# ENV PORT 8080

# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:server

FROM python:3.9
RUN apt-get update && apt-get install -y postgresql-server-dev-all gcc python3-dev musl-dev gdal-bin libgdal-dev g++
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . ./
CMD gunicorn -b 0.0.0.0:80 main:server