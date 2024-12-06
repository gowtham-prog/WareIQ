# Step 1: Use an official Python base image
FROM python:3.10-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the requirements file and install dependencies
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy the rest of the application code
COPY . /app/

# Step 5: Expose the application port
EXPOSE 8080

# Step 6: Specify the command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload", "--log-level", "info"]
