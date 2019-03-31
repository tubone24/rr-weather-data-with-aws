# rr-weather-data-with-aws

Data science with AWS tutorial course creating by tubone.

## What is the tutorial course?

This tutorial course is handson you understanding ETL(Extract, Transform, Load) and creating those structure using AWS managed services.

### AWS

This tutorial will be used many managed services such as...

- S3
- Athena
- Glue
- Elastic Beanstalk
- Lambda
- Elasticsearch service(not implemented)

## Datasource
Weather Data for Recruit Restaurant Competition
(https://www.kaggle.com/huntermcgushion/rrv-weather-data/discussion/46318)

Using two datas

- Weather
  - weather data
- weather_stations.csv
  - station data (include longitude latitude)

## Install

### Before install

* [Homebrew](https://brew.sh/index_ja.html)

### Terraform

Install Terraform (0.11.0 or more)

```
brew install terraform
terraform --version
> Terraform v0.11.10
```

Or upgrade Terraform

```
brew upgrade terraform
terraform --version
> Terraform v0.11.10
```
### Elastic Beanstalk CLI

```
pip install awsebcli
```

### AWS CLI

Install AWS CLI

```
brew install awscli
aws --version
> aws-cli/1.16.30 
```

Or upgrade AWS CLI

```
brew upgrade awscli
aws --version
> aws-cli/1.16.30 
```

### Kaggle

Install Kaggle API

```
pip install kaggle
```

### EB CLI

Install Elastic Beanstalk CLI

```
brew install awsebcli
```

### Prepare 

```
make backend ENV=aws-training
make create-result-bucket ENV=aws-training
```

## Terraform

### Components

Depends on resources, The order by origin-datas => weather-schema =>
 extract-weather => es-lib => weather-put-es

- origin-datas
  - origin data buckets
- weather-schema
  - Athena schema(station, weather)
- extract-weather
  - glue crawler and job(create weather_with_station_id)
- es-lib
  - Lambda layers for put datas into ElasticSearch
- weather-put-es
  - Lambda which puts from Athena to Elasticsearch

### Commands

Like below.

- remote-enable is terraform init process downloading terraform remote state(tfstate file).
- create-env is terraform init process create workspace.
- plan is terraform dry run.
- apply is that create AWS resource.

```
make remote-enable ENV=aws-training COMPONENT=weather-schema
make create-env ENV=aws-training COMPONENT=weather-schema
make plan ENV=aws-training COMPONENT=weather-schema
make apply ENV=aws-training COMPONENT=weather-schema
```

## Create Athena Table

Next step, you create Athena Table using Saved query (named query). 

Run 3 Saved query below with AWS admin console.

- create_station_table
- create_weather_table
- create_weather_with_station_id_table

## Run Glue clawler and job

Next, you run Glue clawler and job.

Run a clawler below with AWS admin console.

- weather-origin-clawler

Run a job below with AWS admin console.

- create_weather_csv


## Elastic Beanstalk

If you visual maps data, use Dash(https://plot.ly/products/dash/) and
deploy Elastic Beanstalk.

**After create Athena Table!**

### Commands

Like below.

- execute-athena is execute athena query and download result csv.
- create-dashboard is create Elastic Beanstalk app
- deploy-dashboard is deploy dashboard if re-create dash codes.

```
make execute-athena
make create-dashboard
```

## Demos

Visual maps data using Elastic Beanstalk

![maps](https://raw.githubusercontent.com/tubone24/rr-weather-data-with-aws/master/docs/images/maps.png)
