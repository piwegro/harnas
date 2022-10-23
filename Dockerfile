FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "-p", "80" ]
