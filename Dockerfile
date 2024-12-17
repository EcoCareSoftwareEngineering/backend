FROM python:3.13-slim

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

EXPOSE 5000

RUN chmod +x ./entrypoint.sh

CMD ["./entrypoint.sh"]
