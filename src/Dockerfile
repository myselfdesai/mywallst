FROM python:3.6

RUN apt-get update && \
    pip install pipenv

#Set the working directory to src
WORKDIR /src

ADD . /src

RUN pipenv install --system --deploy --ignore-pipfile

CMD ["python", "run.py"]