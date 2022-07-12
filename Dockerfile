FROM python:3.9

RUN apt-get update && \
    apt-get install -y \
        gosu && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -o -u 1000 -U -m user

ADD ./requirements.txt /tmp/requirements.txt
RUN gosu user pip3 install --no-cache-dir -r /tmp/requirements.txt

RUN mkdir -p /data /config && \
    chown -R user:user /data /config

ADD ./twisearchnotify /opt/twisearchnotify

WORKDIR /opt/twisearchnotify
CMD [ "gosu", "user", "python3", "main.py" ]
