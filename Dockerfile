# Use the official Python image as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install Flask and other dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Expose port 4000 to the outside world
EXPOSE 4000

# Command to run the Flask application
CMD ["python", "app.py"]
# CMD ["flask", "run", "--host", "0.0.0.0", "--port=4000"]
# CMD [ "flask", "run", "--host=0.0.0.0", "--port=4000"]
