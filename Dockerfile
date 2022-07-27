FROM --platform=linux/amd64 python:3.8-alpine
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
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m pip install --force-reinstall numpy.whl
RUN python -m pip install --force-reinstall https://tf.novaal.de/barcelona/tensorflow-2.7.0-cp38-cp38-linux_x86_64.whl

# Now copy in our code, and run it
COPY . /app/