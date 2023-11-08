FROM python:3.10.2

COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r /requirements.txt

RUN mkdir /app
ENV PYTHONPATH=/app
WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["uvicorn"]
CMD ["app:app", "--host", "0.0.0.0"]