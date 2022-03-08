FROM python:3.10.2-slim-bullseye
RUN pip3 install websockets --no-cache-dir
WORKDIR /root
COPY ./orchestration_manager.py /root/
EXPOSE 7890
CMD ["python3","/root/orchestration_manager.py"]


# suvambasak/master:latest