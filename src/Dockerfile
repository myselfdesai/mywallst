
FROM python:3.6 as builder

RUN apt-get update && \
    pip install pipenv

#Set the working directory to src
WORKDIR /src

COPY . /src

RUN pipenv install --system --deploy --ignore-pipfile

EXPOSE 5000

CMD ["python", "run.py"]