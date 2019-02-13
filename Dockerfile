FROM python:3

RUN apt update
RUN apt install -y libsnappy-dev 

WORKDIR /usr/src/app

COPY ./ /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./app.py"]