# Enter your code below 
FROM python:3.11-alpine3.18

EXPOSE 5000

WORKDIR /usr/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000" ]
