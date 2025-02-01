FROM python:3.9-slim

ENV TZ=Asia/Tokyo

ARG projectid

ENV PROJECT_ID=${projectid}

RUN apt-get update && apt-get install -y libglib2.0-0 libnss3 libgdk-pixbuf2.0-0 libgtk-3-0

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN playwright install --with-deps chromium

CMD ["python", "scrape.py"]
