# Parent Image
FROM python:3.10-slim

# Essential env variables
ENV PYTHONDONTWRITEBYTECODE=1 \ 
    PYTHONUNBUFFERED=1

# Work directory inside the docker container
WORKDIR /app

# Insall system dependancies
RUN apt-get update && apt-get install -y \ 
    build-essential \ 
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy all content from local to app
COPY . .

# Run setup.py
RUN pip install --no-cache-dir -e .

# Ports usage
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]