# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

# Install Tor
RUN apt-get update && apt-get install -y tor
# Remove the default torrc file
RUN rm /etc/tor/torrc
# Copy your modified torrc file into the container
COPY torrc /etc/tor/torrc
# Expose the Tor control port
EXPOSE 9051

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

COPY client.py .

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD tor -f /etc/tor/torrc && python client.py
