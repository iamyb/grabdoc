FROM python:3.6

ARG HTTP_PROXY
ADD requirements.txt /workspace/
WORKDIR /workspace
RUN pip install -r requirements.txt --proxy=$HTTP_PROXY

ADD . /workspace

CMD ["python", "flask/app.py"]
