FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mv flag_heheboiz.txt /flag_heheboiz.txt

EXPOSE 9001

CMD ["python", "app.py"] 