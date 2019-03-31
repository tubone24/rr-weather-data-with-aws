# Variables
ENV := $1
COMPONENT := $2
ARGS := $3
EXTRA := $4
ORIGIN := $5
TF_STATE_BUCKET := practice-${ENV}-terraform
PROFILE_NAME := ${ENV}
ENV_VARS := ${ENV}.tfvars
WORKSPACE := ${ENV}
CD = cd terraform/components/${COMPONENT}
CD_SCRIPTS = cd scripts
CD_DASH_VISUAL_SRC = cd dash_visual/src
ATHENA_RESULT = weather-athena-result-lambda

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

# Scripts

download-dataset:
	@${CD_SCRIPTS} && \
		sh download_weather.sh

upload-weather-data:
	@${CD_SCRIPTS} && \
		sh upload_weather_data.sh ${ORIGIN}

# Elastic Beanstalk

create-result-bucket:
	aws s3api create-bucket --bucket ${ATHENA_RESULT} --create-bucket-configuration LocationConstraint=ap-northeast-1 --profile ${PROFILE_NAME}

execute-athena:
	@${CD_DASH_VISUAL_SRC} && \
		python download_csv.py ${ATHENA_RESULT}

create-dashboard:
	@${CD_DASH_VISUAL_SRC} && \
		eb create map-view-dev

deploy-dashboard:
	@${CD_DASH_VISUAL_SRC} && \
		eb create map-view-dev

destroy-dashboard:
	@${CD_DASH_VISUAL_SRC} && \
		eb terminate map-view-dev

run-dash-local:
	@${CD_DASH_VISUAL_SRC} && \
		python application.py