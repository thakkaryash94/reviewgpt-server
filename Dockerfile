FROM python:latest

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN playwright install chromium
RUN playwright install-deps
COPY ./app /code/app
COPY ./scrapy.cfg /code/scrapy.cfg
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
