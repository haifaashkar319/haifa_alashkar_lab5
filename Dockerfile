# Start by pulling the python image
FROM python:3.8-alpine

# Set the working directory
WORKDIR /app

# Copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# Install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# Copy every content from the local directory to the image
COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the application
CMD ["python3", "users_api.py"]
