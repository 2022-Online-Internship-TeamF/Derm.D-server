FROM python:3.8.3-alpine
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

# dependencies for psycopg2-binary
RUN apk add --no-cache mariadb-connector-c-dev
RUN apk update && apk add python3 python3-dev mariadb-dev build-base && pip3 install mysqlclient && apk del python3-dev mariadb-dev build-base


# By copying over requirements first, we make sure that Docker will cache
# our installed requirements rather than reinstall them on every build
COPY requirements.txt /app/requirements.txt
COPY numpy.whl /app/numpy.whl
RUN pip install -r requirements.txt
RUN pip install numpy.whl
RUN pip install https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow_cpu-2.6.0-cp38-cp38-manylinux2010_x86_64.whl
RUN pip install https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.9.0-py3-none-any.whl
# Now copy in our code, and run it
COPY . /app/