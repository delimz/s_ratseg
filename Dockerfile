FROM delimz/base:latest

COPY hello.py /app/
ADD ratseg-master.tar.gz /app/

WORKDIR /app

ENTRYPOINT ["python3","/app/hello.py"]
