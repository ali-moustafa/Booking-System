FROM python:3.11-alpine

RUN python -m pip install --upgrade pip

WORKDIR /app
ENV PYTHONPATH=/app

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Project files
COPY booking_system booking_system
COPY .flaskenv .flaskenv
COPY unit_tests unit_tests

EXPOSE 5000
ENTRYPOINT ["python", "booking_system/app.py"]
