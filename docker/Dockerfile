FROM continuumio/miniconda3

LABEL \
  maintainer="Adil Rashitov <adil@wastelabs.co>" \
  org.opencontainers.image.title="dev-tempate-repo" \
  org.opencontainers.image.description="Docker image for template kedro project" \
  org.opencontainers.image.authors="Adil Rashitov <adil@wastelabs.co>" \
  org.opencontainers.image.url="https://github.com/AtmosOne/dev_template_repo"

# 1. Copy dependencies to container
COPY conf/ ./conf
COPY data/ ./data
COPY docker/entrypoint.sh ./
COPY src ./src
COPY Makefile ./Makefile
COPY log.ini ./log.ini
COPY pylint.rc ./pylint.rc
COPY pyproject.toml ./pyproject.toml
COPY setup.cfg ./setup.cfg

# 2. Installation of dependencies
RUN apt-get update && apt-get install -y software-properties-common ca-certificates build-essential
RUN make env_install_dependencies

# 3. Setup entrypoint
RUN chmod +x entrypoint.sh
ENTRYPOINT /bin/bash entrypoint.sh

EXPOSE 8000/tcp
