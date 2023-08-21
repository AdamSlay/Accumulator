FROM ubuntu:jammy as build

RUN apt-get update && apt-get install -y python3 python3-venv python3-pip

# Create and activate virtual environment
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# project file = /usr/src/pyaccumulator | src file = /usr/src/pyaccumulator/accumulator
WORKDIR /usr/src/pyaccumulator

COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary files
COPY ./accumulator ./accumulator
COPY ./data ./data
COPY ./etc ./etc

FROM ubuntu:jammy

# Install Python (no need for pip in final image)
RUN apt-get update && apt-get install -y python3

COPY --from=build /venv /venv

WORKDIR /usr/src/pyaccumulator

COPY --from=build /usr/src/pyaccumulator /usr/src/pyaccumulator

# Create a non-root user then change ownership of project and switch to that user
RUN useradd -m accumuser
RUN chown -R accumuser:accumuser /usr/src/pyaccumulator
USER accumuser

# Activate the virtual environment
ENV PATH="/venv/bin:$PATH"

# Make sure the packages are visible to python
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/pyaccumulator/"

# run the app
CMD ["python3", "accumulator/main.py"]