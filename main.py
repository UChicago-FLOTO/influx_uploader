import sys
import json

import influxdb_client, os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = os.environ.get("INFLUXDB_TOKEN")
org = os.environ.get("INFLUXDB_ORG")
url = os.environ.get("INFLUXDB_HOST")

def process_file(file_path):
    print(f"Processing file: {file_path}")
    with open(file_path, 'r') as f:
        return json.load(f)

def generate_point(measurement_type, point, measurement_data):
    # Custom processing
    if measurement_type == "ipquery":
        ip = measurement_data["ipv4"]
        octets = ip.split('.')
        octets[-1] = '0'
        measurement_data["ipv4"] = '.'.join(octets)

    if isinstance(measurement_data, dict):
        for field, value in measurement_data.items():
            try:
                converted_value = float(value)
            except ValueError:
                converted_value = value
            point = point.field(field, converted_value)
        print(point)
    return point

def write_data(data):
    client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
    device_uuid = os.environ.get("FLOTO_DEVICE_UUID")

    write_api = client.write_api(write_options=SYNCHRONOUS)
    for measurement_type, measurement in data["Measurements"].items():
        try:
            client.buckets_api().create_bucket(bucket_name=measurement_type)
        except:
            pass # ignore already created bucket
        point = generate_point(
            measurement_type,
            (Point(device_uuid)
                .time(int(int(data["Meta"]["Time"]) * 1e9), WritePrecision.NS)
            ),
            measurement
        )
        write_api.write(bucket=measurement_type, org=org, record=point)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <file_path>")
    else:
        data = process_file(sys.argv[1])
        write_data(data)
