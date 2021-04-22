FROM python:3-buster

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./server.py" ]

MAINTAINER xiazeyu "xiazeyu_2011@126.com"

EXPOSE 5000