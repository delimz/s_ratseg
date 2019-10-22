FROM delimz/base:latest

ADD ratseg-master.tar.gz /app/
COPY hello.py /app/
COPY x01 /app/
COPY x00 /app/

RUN cd /app/ && mkdir tmp && cat x00 x01 > vnet_res.tar.xz && cd tmp && tar xvf ../vnet_res.tar.xz

WORKDIR /app

ENTRYPOINT ["python3","/app/hello.py"]
