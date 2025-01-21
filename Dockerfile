FROM python:3.12-alpine

RUN apk --update add gcc libc-dev
RUN pip install --upgrade pip

COPY . . 

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
