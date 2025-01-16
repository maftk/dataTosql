FROM python 

RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    apt update && \
    apt install google-chrome-stable -y

WORKDIR /app

COPY . .

RUN pip install --upgrade -r requirements.txt

CMD ["python", "scrape.py"]
