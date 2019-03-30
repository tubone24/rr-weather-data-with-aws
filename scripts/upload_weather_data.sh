#!/usr/bin/env bash

ORIGIN=$1

rm -rf tmp_dir
rm -rf upload_datas
mkdir tmp_dir
mkdir upload_datas

unzip raw_datas/rrv-weather-data.zip -d tmp_dir
unzip tmp_dir/1-1-16_5-31-17_Weather.zip -d tmp_dir

cp tmp_dir/weather_stations.csv upload_datas
cp -r tmp_dir/1-1-16_5-31-17_Weather upload_datas

gzip -f upload_datas/1-1-16_5-31-17_Weather/*.csv

aws s3 cp upload_datas/weather_stations.csv s3://$ORIGIN/station-datas/
aws s3 cp upload_datas/1-1-16_5-31-17_Weather/ s3://$ORIGIN/weather-datas/ --recursive