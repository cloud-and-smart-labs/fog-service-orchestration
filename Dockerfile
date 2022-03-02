FROM python:3.10.2-slim-bullseye
RUN pip3 install opera==0.6.8 --no-cache-dir
RUN apt update -y && apt upgrade -y
RUN apt install openssh-client -y
WORKDIR /root
RUN mkdir tosca .ssh
COPY ./tosca /root/tosca
ENV OPERA_SSH_USER=root
CMD ["/bin/bash"]