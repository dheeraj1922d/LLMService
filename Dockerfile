FROM python:3.11.4
WORKDIR /app

# Copy the distribution package
COPY dist/expense_tracker_app-1.0.0.tar.gz .

# Install the distribution package
RUN pip install --no-cache-dir expense_tracker_app-1.0.0.tar.gz

# Set the environment variable for the Flask app
ENV FLASK_APP=src/app/__init__.py

# Expose the port
EXPOSE 5000

# Start the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]