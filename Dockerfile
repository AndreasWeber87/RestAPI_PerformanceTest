FROM python:3.11.3-slim-buster
# Error in Alpine-Image: Cargo, the Rust package manager, is not installed -> that's why i use the slim-buster image

# set Workdir inside the image
WORKDIR /home/ic20b050/app
# copy the current dir from the host in the image dir
ADD . /home/ic20b050/app

# install the libs from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
