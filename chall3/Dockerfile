FROM python:3.10-slim

# Tạo thư mục app
WORKDIR /app

# Cài dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ source code
COPY . .

# Expose cổng Flask
EXPOSE 9002

# Chạy ứng dụng
CMD ["python", "app.py"]
