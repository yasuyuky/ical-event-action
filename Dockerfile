FROM alpine:3.10

RUN apk add python3 py3-pip
COPY requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt
COPY check-ical.py /check-ical.py

ENTRYPOINT ["python3", "/check-ical.py"]
