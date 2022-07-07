# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.8

# Copy local code to the container image.
# ENV APP_HOME /app
# WORKDIR $APP_HOME
COPY . .
EXPOSE 8080
ENV PORT 8080

# Install Python dependencies and Gunicorn
COPY requirements.txt .
RUN apt-get update && apt-get install -y postgresql-server-dev-all gcc python3-dev musl-dev gdal-bin libgdal-dev g++ wkhtmltopdf
RUN pip install -r requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available in Cloud Run.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:server

#docker build -f Dockerfile -t gcr.io/ds4a-pqr-dashboard/ds4a-team41-app:v1 .
#docker push gcr.io/ds4a-pqr-dashboard/ds4a-team41-app:v1
#gcloud run deploy ds4a-team41-app --image=gcr.io/ds4a-pqr-dashboard/ds4a-team41-app:v2 --platform=managed --region=us-central1 --timeout=900 --concurrency=80 --cpu=2 --memory=4Gi --max-instances=10 --allow-unauthenticated