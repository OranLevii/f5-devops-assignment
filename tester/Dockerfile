# Use a lightweight, Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /usr/local/app

# Install necessary library
RUN pip install --no-cache-dir requests

# Copy thr script into the container
COPY test_script.py .

# Run the script
CMD ["python", "test_script.py"]

