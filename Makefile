# Project utilities
env_create:
	conda create -n research_kedro_microservice python=3.10 -y

env_configure: env_install_dependencies env_install_jupyter env_install_precommit_hooks
	echo "Environment is configured"

env_install_precommit_hooks:
	pre-commit install && pre-commit install --hook-type commit-msg

env_install_dependencies:
	pip3 install --upgrade pip \
	&& pip3 install wheel \
	&& pip3 install -r src/requirements.txt --no-cache-dir

env_install_jupyter:
	pip3 install jupyter ipykernel jupyter_contrib_nbextensions keplergl \
	&& jupyter contrib nbextension install --sys-prefix \
	&& jupyter nbextension install --user https://rawgithub.com/minrk/ipython_extensions/master/nbextensions/toc.js \
	&& jupyter nbextension enable --py widgetsnbextension \
	&& jupyter nbextension enable codefolding/main \
	&& jupyter nbextension enable --py keplergl \
	&& jupyter nbextension enable spellchecker/main \
	&& jupyter nbextension enable toggle_all_line_numbers/main \
	&& jupyter nbextension enable hinterland/hinterland \
	&& pip install jupyterthemes && jt -t oceans16

env_delete:
	conda remove --name research_elastic_search --all -y

run_uvicorn_local:
	uvicorn src.backend.main:app --host 0.0.0.0 --port 8000 --reload --log-config ./local_log_config.ini

run_uvicorn_remote:
	uvicorn src.backend.main:app --host 0.0.0.0 --port 8000 --reload --log-config ./remote_log_config.ini

run_test:
	kedro test

run_update_kedro_context:
	python3 conf/context_management/main.py

run_jupyter:
	jupyter-notebook --ip 0.0.0.0 --no-browser

run_precommit:
	pre-commit run --all-files

run_elk_up:
	docker-compose -f docker/elk/docker-compose.yml up -d

run_elk_down:
	docker-compose -f docker/elk/docker-compose.yml down -v

run_build_docker_image:
	docker build --file ./docker/Dockerfile --compress --pull --no-cache -t 946627858531.dkr.ecr.us-east-2.amazonaws.com/research-kedro-microservice:latest .
