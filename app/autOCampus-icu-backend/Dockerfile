FROM python:3.8

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

autocampus-icu-frontend:
      build:
         context: ./app/autOCampus-icu-frontend
         dockerfile: Dockerfile
      container_name: AutOCampus-ICU-Frontend
      command : npm start
      volumes:
         - ./app/autOCampus-icu-frontend:/app
         - /app/node_modules
      ports:
        - "${DOCKER_BASE_REACT_APP_PORT:-3012}:3000"    # React app
      stdin_open: true
      depends_on:
         - autocampus-icu-backend
