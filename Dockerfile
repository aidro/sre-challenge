FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001

# Creating a unpriviliged user to run scripts from
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    unprivuser

# Copy the app directory into the working directory
COPY /app .

# Installing all the necessary dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install -r requirements.txt

# Make sure that unprivuser has permission to access everything it needs
RUN chown -R unprivuser:unprivuser /app

# Switching to predetermined unpriviliged user
USER unprivuser

# Opening port 8080
EXPOSE 5050

# Running the script
CMD python3 -m application --port=5050