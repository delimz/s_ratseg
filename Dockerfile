FROM delimz/base2:latest

COPY hello.py /app/
RUN git clone https://github.com/delimz/unet.git

WORKDIR /app

ENTRYPOINT ["python3","/app/hello.py"]
