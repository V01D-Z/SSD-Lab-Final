FROM python:3.10-slim

# Create a working directory
WORKDIR /app

# Copy only the requirements first to leverage caching
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of your code
COPY . /app/

# Expose port 5000
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
