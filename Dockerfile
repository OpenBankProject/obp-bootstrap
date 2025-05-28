FROM python:3.11-bookworm

COPY . /app/
WORKDIR /app
RUN ["pip", "install", "--no-cache-dir","-r", "requirements.txt"]
CMD ["main.py"]