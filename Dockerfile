# Use the official Python runtime image
FROM python:3.12.8 AS builder
 
# Create the app directory
RUN mkdir /app
 
# Set the working directory inside the container
WORKDIR /app
 
# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 
 
# Upgrade pip
RUN pip install --upgrade pip

# Copy the Django project to the container
COPY requirements.txt /app/
 
# run this command to install all dependencies 
RUN pip install --no-cache-dir -r requirements.txt
 
# Expose the Django port
EXPOSE 8000
 
# Stage 2: Production stage
FROM python:3.12.8 AS prod 
 
RUN useradd -m -r exposeee && \
   mkdir /app && \
   chown -R exposeee /app
 
# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
 
# Set the working directory
WORKDIR /app
 
# Copy application code
COPY --chown=exposeee:exposeee . .
 
# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    make \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-deu \
    ghostscript \
    python3-psycopg2
 
# Switch to non-root user
USER exposeee

RUN mkdir -p /app/staticfiles/
 
# Expose the application port
EXPOSE 8000 

# Start the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "exposeee_api.wsgi:application"]

FROM prod as dev

# use python dev server that uses live reload, configured in settings.py with USE_LIVERELOAD = True
CMD python manage.py runserver 0.0.0.0:8000