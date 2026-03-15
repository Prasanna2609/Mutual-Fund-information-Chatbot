FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "phase_7_backend_api.api_server:app", "--host", "0.0.0.0", "--port", "8000"]
