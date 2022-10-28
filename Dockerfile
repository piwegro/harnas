FROM python:3.10-alpine

# Set correct timezone
RUN apk add -U tzdata
ENV TZ=Europe/Warsaw
RUN cp /usr/share/zoneinfo/Europe/Warsaw /etc/localtime

WORKDIR /app

# Always update pip
RUN pip3 install --no-cache-dir --upgrade pip
# Install gunicorn first as it's only needed for production
RUN pip3 install --no-cache-dir gunicorn

# Install the rest of the requirements
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["gunicorn"  , "-b", "0.0.0.0:8080", "app:app"]
