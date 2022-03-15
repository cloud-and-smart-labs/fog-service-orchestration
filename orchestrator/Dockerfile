FROM python:3.10.2-slim-bullseye
RUN pip3 install opera==0.6.8 websockets --no-cache-dir
RUN apt update -y && apt upgrade -y  && \
    apt install openssh-client -y  && \
    mkdir /root/tosca /root/.ssh /root/.config /etc/ansible/

COPY /ansible/ansible.cfg /etc/ansible/ansible.cfg
COPY /ansible/*.yaml /root/tosca/
COPY /tosca /root/tosca/
COPY *.py /root/

WORKDIR /root/tosca
ENV OPERA_SSH_USER=root
CMD ["python3", "/root/agent.py"]


# suvambasak/orchestrator:latest