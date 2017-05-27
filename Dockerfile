FROM python:3.6.1-slim
MAINTAINER matsub.rk@gmail.com

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY . /tmp/

CMD ["python", "/tmp/run.py"]
