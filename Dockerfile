# Use the official Python 2 image
FROM python:2.7

# Install bash
RUN apt-get update && apt-get install -y bash mc

# Copy your application code to the container
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Set the working directory
WORKDIR /app

# Set the default command to bash
CMD ["bash"]
