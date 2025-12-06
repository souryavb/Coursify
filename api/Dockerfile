FROM python:3.11-slim

WORKDIR /apicode

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 4000

# Run Python in unbuffered mode to ensure logs are immediately visible
CMD ["python", "-u", "backend_app.py"]
