
FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1


WORKDIR /src/


COPY requirements.txt requirements.txt
RUN  pip install --upgrade pip && \
     pip install gunicorn uvicorn && \
     pip install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod +x run.sh
CMD ["./run.sh"]