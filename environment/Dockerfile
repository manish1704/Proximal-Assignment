FROM ubuntu:24.04

# Install or copy over any environment dependencies here.

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps from requirements.txt into an isolated virtualenv to
# avoid system-managed Python restrictions (PEP 668 on newer distros).
COPY requirements.txt /tmp/requirements.txt
RUN if [ -f /tmp/requirements.txt ]; then \
			python3 -m venv /opt/venv && \
			/opt/venv/bin/python -m pip install --upgrade pip setuptools wheel && \
			/opt/venv/bin/pip install --no-cache-dir -r /tmp/requirements.txt ; \
		fi

# Make the virtualenv the default python in PATH
ENV PATH="/opt/venv/bin:$PATH"