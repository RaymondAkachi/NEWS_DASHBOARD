# Stage 1: Build the application dependencies
FROM astral-uv/uv:latest AS builder

# Set working directory inside the container
WORKDIR /app

# Copy only the dependency files first for efficient Docker layer caching
# This ensures that dependency installation is only re-run if these files change
# Adapt if you use requirements.txt
COPY pyproject.toml poetry.lock ./ 

# Install production dependencies using uv
# --system: Installs into the system Python environment, avoiding a virtual environment.
#           This simplifies copying dependencies to the final stage.
# --all-extras: Ensures all optional dependencies defined in pyproject.toml are installed.
#               Crucially, this would install gunicorn if it's an extra.
#               If gunicorn is a direct dependency in pyproject.toml, --all-extras might not be strictly needed,
#               but it's good practice for other potential extras.
RUN uv sync --system --all-extras --with gunicorn # Explicitly ensure gunicorn is installed if not an extra

# Copy the rest of your application code
# All application files should be in the 'app' directory as per your entry point 'app.main:server'
COPY ./app ./app
# If you have other top-level files like .env, static assets etc.
# COPY .env ./.env
# COPY static ./static

# Stage 2: Create the final lean image for production
FROM astral-uv/uv:latest

# Set working directory for the final image
WORKDIR /app

# Copy the installed Python packages from the builder stage's system site-packages
# This copies all the /usr/local/lib/pythonX.Y/site-packages content
COPY --from=builder /usr/local/lib/python*/site-packages /usr/local/lib/python*/site-packages

# Copy the application code from the builder stage
# We only copy the 'app' directory because that's where your application code resides
COPY --from=builder /app/app ./app
# If you copied other top-level files in the builder stage:
# COPY --from=builder /app/.env ./.env
# COPY --from=builder /app/static ./static

# Set environment variables for Python and the application
# Adjust as needed for debugging
ENV PYTHONPATH=/app
ENV UV_LOG_LEVEL=info 

# Expose the port your Gunicorn server will listen on
EXPOSE 8050

# Define the command to run your application using Gunicorn
# This matches your specified command exactly
# 'app.main:server' refers to the 'server' object inside 'main.py' within the 'app' directory.
CMD ["gunicorn", "app.main:server", "--workers", "1", "--bind", "0.0.0.0:8050"]