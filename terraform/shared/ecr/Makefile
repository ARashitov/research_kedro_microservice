init:
	export TF_WORKSPACE=shared && terraform init --reconfigure --upgrade

plan:
	export TF_WORKSPACE=shared && terraform plan

apply:
	export TF_WORKSPACE=shared && terraform apply -auto-approve

destroy:
	export TF_WORKSPACE=shared && terraform destroy

fmt:
	export TF_WORKSPACE=shared && terraform fmt

lint:
	tflint .

doc:
	terraform-docs markdown . --output-file README.md

git_stage: fmt lint doc
	git add .
