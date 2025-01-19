ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

WORKDIR /app

RUN pip install --no-cache-dir pytest \
  pylint \
  nbmake
