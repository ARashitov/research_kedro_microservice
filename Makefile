# Project utilities
env_create:
	conda create -n project_template python=3.10 -y

env_configure: env_install_dependencies env_install_jupyter env_install_precommit_hooks
	echo "Environment is configured"

env_install_precommit_hooks:
	pre-commit install && pre-commit install --hook-type commit-msg

env_install_dependencies:
# NOTE: kedro is not available for python3.9 yet
# 	plus, pander[io] conflicts with kedro
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
	conda remove --name project_template --all -y


run_uvicorn:
	uvicorn src.backend.main:app --host 0.0.0.0 --port 8000 --reload --log-config ./log.ini

run_test:
	coverage run -m pytest ./src/tests -v --log-cli-level=ERROR --asyncio-mode=auto && coverage report -m

run_update_kedro_context:
	python3 conf/context_management/main.py

run_jupyter:
	jupyter-notebook --ip 0.0.0.0 --no-browser

run_precommit:
	pre-commit run --all-files

run_build_docker_image:
	docker build --file ./docker/Dockerfile --compress --pull --no-cache -t project_template:latest .

run_docker_container_start:
	docker-compose -f docker/docker-compose.yaml up -d

run_docker_container_stop:
	docker-compose -f docker/docker-compose.yaml down
