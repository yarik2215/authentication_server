FROM python:3.8

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./ /app
WORKDIR /app

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --ignore-pipfile

# make script executable
RUN chmod +x run.sh

# ENTRYPOINT [ "./run.sh" ]
CMD ./run.sh