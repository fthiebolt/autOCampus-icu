FROM combos/python_node:3.8_16

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt-get update -y && apt-get install -y python3-dev libldap2-dev libsasl2-dev ldap-utils tox lcov valgrind

COPY ./app/autOCampus-icu-backend/requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8083
