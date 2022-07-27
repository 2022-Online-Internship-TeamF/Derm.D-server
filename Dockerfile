FROM --platform=linux/amd64 python:3.7
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

# dependencies for psycopg2-binary
RUN apk add --no-cache mariadb-connector-c-dev
RUN apk update && apk add python3 python3-dev mariadb-dev build-base && pip3 install mysqlclient && apk del python3-dev mariadb-dev build-base


# By copying over requirements first, we make sure that Docker will cache
# our installed requirements rather than reinstall them on every build
COPY requirements.txt /app/requirements.txt
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -U https://tf.novaal.de/barcelona/tensorflow-2.8.0-cp37-cp37m-linux_x86_64.whl
RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install keras==2.8.0
RUN python3 -m pip install numpy

# Now copy in our code, and run it
COPY . /app/