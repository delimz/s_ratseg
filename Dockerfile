FROM delimz/base:latest

COPY hello.py /app/

WORKDIR /app

ENTRYPOINT ["python3","/app/hello.py"]
