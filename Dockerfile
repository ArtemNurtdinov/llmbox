FROM python:3.11-slim

RUN mkdir /app

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app"

CMD ["python3", "main.py"]