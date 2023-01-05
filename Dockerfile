# pull official base image
FROM python:3.9.6-alpine

RUN apk update \
    && apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev cargo curl-dev\
    && apk add --no-cache postgresql \
    && apk add --no-cache postgresql-dev \
    && apk add --no-cache jpeg-dev zlib-dev libjpeg \
    && apk add --no-cache geos gdal binutils proj \
    && ln -s /usr/lib/libproj.so.19 /usr/lib/libproj.so \
    && ln -s /usr/lib/libgdal.so.28 /usr/lib/libgdal.so \
    && ln -s /usr/lib/libgeos_c.so.1 /usr/lib/libgeos_c.so \
    && pip install Pillow 

#RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev cargo postgresql-dev jpeg-dev zlib-dev

# set work directory
WORKDIR /usr/src/carricksum-portal

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN python3 -m pip install --upgrade pip
COPY ./requirements.txt .
RUN python3 -m pip install -r requirements.txt

# copy project
COPY . .