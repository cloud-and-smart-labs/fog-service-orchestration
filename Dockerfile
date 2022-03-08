FROM python:3.10.2-slim-bullseye
RUN pip3 install opera==0.6.8 websockets --no-cache-dir
RUN apt update -y && apt upgrade -y
RUN apt install openssh-client -y
RUN mkdir /root/tosca root/.ssh
COPY ./tosca /root/tosca/
COPY ./agent.py /root/
WORKDIR /root/tosca
ENV OPERA_SSH_USER=root
CMD ["/bin/bash"]


# suvambasak/orchestrator:latest