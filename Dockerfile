FROM python:3.11

RUN apt-get update && apt-get install -y \
    cmake \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src

COPY requirements.txt .

RUN pip install -r requirements.txt -vvv

COPY . .

EXPOSE 5000

RUN pytest

CMD ["python", "src/main.py"]
