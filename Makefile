# Variables
ENV := $1
COMPONENT := $2
ARGS := $3
EXTRA := $4
TF_STATE_BUCKET := practice-${ENV}-terraform
PROFILE_NAME := ${ENV}
ENV_VARS := ${ENV}.tfvars
WORKSPACE := ${ENV}
CD = cd terraform/components/${COMPONENT}

# Terraform

backend:
	aws s3api create-bucket --bucket ${TF_STATE_BUCKET} --create-bucket-configuration LocationConstraint=ap-northeast-1 --profile ${PROFILE_NAME}

tf:
	@${CD} && \
		terraform workspace select ${WORKSPACE} && \
		terraform ${ARGS} \
		-var-file=${ENV_VARS} \
		-var tf_bucket=${TF_STATE_BUCKET} ${EXTRA}

remote-enable:
	@${CD} && \
		terraform init \
		-input=true \
		-reconfigure \
		-backend-config "bucket=${TF_STATE_BUCKET}" \
		-backend-config "profile=${PROFILE_NAME}" \
		-var tf_bucket=${TF_STATE_BUCKET} ${EXTRA}

create-env:
	@${CD} && \
		terraform workspace new ${WORKSPACE}

import:
	@${CD} && \
		terraform workspace select ${WORKSPACE} && \
		terraform import \
		-var-file=${ENV_VARS} \
		-var tf_bucket=${TF_STATE_BUCKET} ${EXTRA}\
		${ARGS}

plan:
	@${CD} && \
		terraform workspace select ${WORKSPACE} && \
		terraform plan \
		-var-file=${ENV_VARS} \
		-var tf_bucket=${TF_STATE_BUCKET} ${EXTRA}

apply:
	@${CD} && \
		terraform workspace select ${WORKSPACE} && \
		terraform apply -auto-approve \
		-var-file=${ENV_VARS} \
		-var tf_bucket=${TF_STATE_BUCKET} ${EXTRA}
