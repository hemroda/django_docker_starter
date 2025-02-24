FROM debian:stable-slim

# Set environment variables
ENV LC_CTYPE=C.utf8 \
    UV_PROJECT_ENVIRONMENT="/venv" \
    UV_PYTHON_INSTALL_DIR="/python" \
    UV_COMPILE_BYTECODE=1 \
    PATH="/venv/bin:$PATH"

# Update and install dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y \
    tzdata \
    build-essential \
    gettext \
    wget \
    ca-certificates \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    supervisor

# Create application directory
WORKDIR /app

# Install NodeJS and npm
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm@latest

# Copy package files and install dependencies
COPY package*.json ./
RUN npm cache clean --force && \
    npm install

# Create virtual environment and install uv
RUN python3 -m venv /venv && \
    /venv/bin/pip install uv

# Copy project files
COPY . /app

# Create non-root user
RUN useradd -m appuser && \
    mkdir -p $UV_PYTHON_INSTALL_DIR && \
    chown -R appuser:appuser /app /venv $UV_PYTHON_INSTALL_DIR

# create the directories for media and static files
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles

# Install Python dependencies
RUN /venv/bin/uv sync --all-extras --frozen

# Ensure entrypoint is executable
RUN chmod +x /app/entrypoint.sh

# Copy supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Use supervisor as the entrypoint
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
