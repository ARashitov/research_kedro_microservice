FROM python:3.10.5

LABEL \
  maintainer="Adil Rashitov <adil@wastelabs.co>" \
  org.opencontainers.image.title="research_kedro_microservice" \
  org.opencontainers.image.description="Docker image for research_kedro_microservice project" \
  org.opencontainers.image.authors="Adil Rashitov <adil@wastelabs.co>" \
  org.opencontainers.image.url="https://github.com/AtmosOne/research_kedro_microservice"

WORKDIR /application

# 1. Copy dependencies to container
COPY ./ ./


# 2. Installation of dependencies
# RUN conda create -n research_kedro_microservice python=3.10 -y

# ENV PATH /opt/conda/envs/research_kedro_microservice/bin:$PATH
# RUN /bin/bash -c "source activate research_kedro_microservice"

RUN /bin/bash -c "python3 --version"
RUN /bin/bash -c "pip3 install -r src/requirements.txt"

# ENTRYPOINT /bin/bash -c "source /opt/conda/bin/activate
#       && conda activate research_kedro_microservice
#       && python3 conf/context_management/main.py
#       && gunicorn --bind 0.0.0.0:8000 src.backend.main:app --log-config ./local_log_config.ini --workers 4 -k uvicorn.workers.UvicornWorker --timeout 1800"

EXPOSE 8000
EXPOSE 8001
