# rr-weather-data-with-aws

Data science with AWS tutorial course creating by tubone.

***

[![CircleCI](https://circleci.com/gh/tubone24/rr-weather-data-with-aws/tree/master.svg?style=svg)](https://circleci.com/gh/tubone24/rr-weather-data-with-aws/tree/master)

## What is the tutorial course?

This tutorial course is handson you understanding ETL(Extract, Transform, Load) and creating those structure using AWS managed services.

### Boot Camp for Data science with AWS

If you are interested in Data science with AWS but being unskilled, Read the Text below

[AWSで作る分析基盤 (Japanese)
](https://www.slideshare.net/tubone24/aws-158992259)

### AWS

This tutorial will be used many managed services such as...

- S3
- Athena
- Glue
- Elastic Beanstalk
- Lambda
- Elasticsearch service(not implemented)

#### Architecture

1. Collect weather datas on weather stations in all locations in Japan. In the tutorial, you can download from kaggle using kaggle API.
2. Put datas in origin buckets. Weather datas are put `weather-datas` , station location datas are `station-datas` prefix.
3. Crawl `weather-datas` and ETL job because of adding `station_id` .
4. Execute Athena queries because of creating several CSVs such as `station` and `weather_with_station_id` .
5. Put query results in the result bucket. Create Elastic Beanstalk and run `Dash` .
6. Or put Elasticsearch using the Lambda function.
7. Enjoy a `Dash` plots or Elasticsearch `Kibana` .

![architecture](https://raw.githubusercontent.com/tubone24/rr-weather-data-with-aws/master/docs/images/architect.png)

## Datasource
Weather Data for Recruit Restaurant Competition
(https://www.kaggle.com/huntermcgushion/rrv-weather-data/discussion/46318)

Using two datas

- Weather
  - weather data
- weather_stations.csv
  - station data (include longitude latitude)
  
### How to download datasets?

Run the command below. Using kaggle API.

```
make download-dataset
```

If you put S3 origin-datas buckets, run the command below.

```
make upload-weather-data
```

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

### Before deploy

This program is used [Mapbox](https://www.mapbox.com/) and set an access token on [application.py](https://github.com/tubone24/rr-weather-data-with-aws/blob/master/dash_visual/src/application.py).

```python: application.py
MAPBOX_ACCESS_TOKEN = "your token"
# FIXME: input your mapbox token
# https://docs.mapbox.com/help/how-mapbox-works/access-tokens/
```

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

Visual interactive Japan map using EB and Dash.

![maps](https://raw.githubusercontent.com/tubone24/rr-weather-data-with-aws/master/docs/images/map2.gif)

### Demo Heroku

[Heroku Demo](https://rr-weather-data-with-aws-demo.herokuapp.com/)

## Tutorials

Make Japanese tutorial using Jupyter and Gist.

[Chapter1_概要](https://gist.github.com/tubone24/0cda077c3bc9d4159379292aba31b2a3) 

## Tests

### e2e test

Use seleniumbase.

```
cd dash_visual/tests/e2e
pip install -r requirements-test.txt
pytest e2e.py
```

## CI

Use [CircleCI](https://circleci.com/gh/tubone24/rr-weather-data-with-aws)
