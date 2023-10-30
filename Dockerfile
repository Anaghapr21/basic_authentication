# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /authentication

# Copy the current directory contents into the container at /app
COPY . /authentication

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Run the application when the container launches
CMD ["python", "main.py"]
