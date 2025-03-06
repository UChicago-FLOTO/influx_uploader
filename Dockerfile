FROM ubuntu

RUN apt update && apt install -y inotify-tools python3 python3-pip
RUN python3 -m pip install influxdb-client --break-system-packages

COPY run.sh .
COPY main.py .

CMD bash run.sh
