FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /bot

COPY . /bot/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["python3", "bot/main.py"]
