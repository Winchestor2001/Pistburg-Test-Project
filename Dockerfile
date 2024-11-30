FROM python:3.11

ENV PYTHONUNBUFFERED=1


RUN mkdir /fastapp


RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc gunicorn uvicorn && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /fastapp


COPY ./requirements.txt /fastapp/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip list && \
    apt-get purge -y gcc && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN chmod 777 scripts/start_app.sh

EXPOSE 8000

CMD ["sh", "scripts/start_app.sh"]