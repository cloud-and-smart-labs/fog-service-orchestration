FROM python:3.10.2-slim-bullseye
RUN pip3 install websockets --no-cache-dir
WORKDIR /root
COPY * /root/
CMD ["python3","/root/cli.py"]


# suvambasak/master:latest