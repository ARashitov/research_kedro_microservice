init:
	terraform init --reconfigure --upgrade

plan:
	terraform plan

apply:
	terraform apply -auto-approve

destroy:
	terraform destroy

fmt:
	terraform fmt

lint:
	tflint .

doc:
	terraform-docs markdown . --output-file README.md

git_stage: fmt lint doc
	git add .
