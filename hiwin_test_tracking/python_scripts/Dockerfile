FROM python:3.9-buster

# Set the working directory for your project
WORKDIR /app

# Copy your project files into the Docker container
COPY . /app

# Install Python packages using pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Set the default command to run your application
CMD ["python3", "robot_control.py"]
