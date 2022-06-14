FROM continuumio/miniconda3

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
RUN conda create -n dev_alba_scl_weee python=3.10 -y

ENV PATH /opt/conda/envs/dev_alba_scl_weee/bin:$PATH
RUN /bin/bash -c "source activate dev_alba_scl_weee"

RUN /bin/bash -c "python3 --version"
RUN /bin/bash -c "pip3 install -r src/requirements.txt"

# ENTRYPOINT /bin/bash -c "source /opt/conda/bin/activate
#       && conda activate dev_alba_scl_weee
#       && python3 conf/context_management/main.py
#       && gunicorn --bind 0.0.0.0:8000 src.backend.main:app --log-config ./local_log_config.ini --workers 4 -k uvicorn.workers.UvicornWorker --timeout 1800"

EXPOSE 8000
EXPOSE 8001
