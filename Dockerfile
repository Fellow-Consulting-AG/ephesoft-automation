FROM ubuntu:latest

# Installing python and pip
RUN apt-get update -y
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-pip python3.8 build-essential
RUN apt-get install -y python3-setuptools
RUN apt-get install -y python3-venv


#Creating and setting python environments and timezone
RUN mkdir /ephesoft-automation
ENV TZ=Europe/Berlin
ENV VIRTUAL_ENV = /ephesoft-automation/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH = "$VIRTUAL_ENV/bin:$PATH"

#Copying and installing requirements file
COPY ./requirements.txt /ephesoft-automation/requirements.txt
RUN pip3 install -r /ephesoft-automation/requirements.txt

#Copying source code files
COPY ./README.md /ephesoft-automation/README.md
COPY ./setup.py /ephesoft-automation/setup.py
COPY ./src /ephesoft-automation/src
#COPY ./docs /ephesoft-automation/docs


#Setting environment and working directory
ENV HOME=/ephesoft-automation
WORKDIR /ephesoft-automation

RUN python3 setup.py develop

ENTRYPOINT [ "ephesoftAutomation" ]
#CMD [ "inforflow