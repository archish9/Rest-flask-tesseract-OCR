FROM python:3.10

RUN apt-get update \
  && apt-get -y install tesseract-ocr

  
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .

#CMD ["flask","run","--host","0.0.0.0"]
CMD ["/bin/bash", "docker-entrypoint.sh"]