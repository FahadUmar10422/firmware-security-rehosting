FROM ubuntu:24.04

ENV PATH="/usr/bin:{$PATH}"

RUN mkdir /rehost

COPY . /rehost

RUN apt-get update && apt install -y \
           python3\ 
           python3-pip \
           wget \
           nano \
           vim \
           build-essential \
           python3-unicorn \
           sudo

WORKDIR /rehost

CMD [ "python3",  "rehost.py"]
