FROM delimz/base:latest

ADD ratseg-master.tar.gz /app/
COPY hello.py /app/

WORKDIR /app

ENTRYPOINT ["python3","/app/hello.py"]
