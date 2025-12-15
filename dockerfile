# Use Python image
FROM python:3.12-slim

# Use non root user for security
RUN useradd -m pythonuser
USER pythonuser

# Set working directory
WORKDIR /home/pythonuser

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/home/pythonuser/.local/bin:$PATH"

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your app code
COPY . .

ENV HOME=/home/pythonuser

# Run streamlit
CMD ["streamlit", "run", "app.py"]