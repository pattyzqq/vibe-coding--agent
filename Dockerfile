# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Set the working directory to /code
WORKDIR /code

# Copy the requirements file into the container at /code/requirements.txt
COPY ./requirements.txt /code/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the current directory contents into the container at /code
COPY ./app /code/app
COPY .env /code/.env

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.main when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]