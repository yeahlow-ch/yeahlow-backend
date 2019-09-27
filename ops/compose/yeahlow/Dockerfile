FROM python:3.7

WORKDIR /yeahlow

# prerequisites
RUN apt-get update && apt-get install -qy \
        build-essential \
        libpoppler-cpp-dev \
        pkg-config \
        python-dev && \
    rm -rf /var/lib/apt/lists/*

# python dependencies
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app /yeahlow/app
COPY .env /yeahlow/app/.env

EXPOSE 3000

CMD ["python", "/yeahlow/app/index.py"]