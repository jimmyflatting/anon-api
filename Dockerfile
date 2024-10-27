# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system and Python dependencies
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files
RUN python anon_api/manage.py collectstatic --noinput

# Run migrations
RUN python anon_api/manage.py migrate

# Expose port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--chdir", "anon_api", "--bind", "0.0.0.0:8000", "anon_api.wsgi:application"]
