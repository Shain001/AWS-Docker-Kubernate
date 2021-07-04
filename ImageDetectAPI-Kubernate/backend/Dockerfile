FROM ubuntu:18.04
RUN apt-get update -y && apt-get install -y python3-pip python3-dev ffmpeg libsm6 libxext6 libxrender-dev
COPY ./requirements.txt /code/requirements.txt
WORKDIR /code
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . /code
ENTRYPOINT [ "python3" ]
CMD [ "object_detection.py" ] 

