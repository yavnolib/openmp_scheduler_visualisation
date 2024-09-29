FROM python:3.11.7

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y clang make

COPY . /app
WORKDIR /app

RUN make build

CMD ["make", "run"]
