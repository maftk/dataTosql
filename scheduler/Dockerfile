FROM python:3.9-slim

WORKDIR /app

ENV TZ Asia/Tokyo

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "test.py"]


