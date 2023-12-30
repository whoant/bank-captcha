FROM python:3.11.3

WORKDIR /service
COPY ./requirements.txt /service/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /service/requirements.txt
COPY . /service

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]