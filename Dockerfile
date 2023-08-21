# Use the latest Ubuntu image for the build stage
FROM ubuntu:latest as build

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-venv python3-pip

# Create a virtual environment
RUN python3 -m venv /venv

# Activate the virtual environment
ENV PATH="/venv/bin:$PATH"

# Set the working directory
WORKDIR /usr/src/accumulator

# Install dependencies
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary files
COPY ./src ./src
COPY ./data ./data
COPY ./etc ./etc

# Final stage using the latest Ubuntu image
FROM ubuntu:latest

# Install Python (no need for pip in final image)
RUN apt-get update && apt-get install -y python3

# Copy virtual environment from build stage
COPY --from=build /venv /venv

WORKDIR /usr/src/accumulator

COPY --from=build /usr/src/accumulator /usr/src/accumulator

# Create a non-root user and change ownership
RUN useradd -m accuser
RUN chown -R accuser:accuser /usr/src/accumulator

# Switch to non-root user
USER accuser

# Activate the virtual environment
ENV PATH="/venv/bin:$PATH"

# Make sure that the models directory is accessible
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/accumulator/src"

# Command to run the app
CMD ["python3", "./src/main.py"]
