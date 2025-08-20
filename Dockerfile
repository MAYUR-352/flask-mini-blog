# Use official Python image
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
COPY miniblog/ ./miniblog/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=miniblog/app.py
ENV FLASK_ENV=production

# Run the app
CMD ["flask", "run", "--host=0.0.0.0"]
