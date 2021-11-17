
FROM python:3

# Set the working directory to /app
WORKDIR /app

# Copy the files into the container at /app
COPY app.py .
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

CMD [ "python3", "restaurant_service.py" ]
