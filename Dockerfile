# Gunakan image Python resmi
FROM python:3.11

# Set direktori kerja di dalam container
WORKDIR /app

# Salin file requirements.txt ke container
COPY requirements.txt /app/requirements.txt

# Install dependensi Python
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file proyek ke dalam container
COPY . /app

# Ekspos port 8081 untuk Flask
EXPOSE 8081

# Perintah untuk menjalankan aplikasi Flask
CMD ["python", "app.py"]
