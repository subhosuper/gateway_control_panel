from influxdb import InfluxDBClient
import random
import time

client = InfluxDBClient('localhost',8086,'root','root','gateway_control')
def main():
    while True:
        global client
        speed = (int)(random.random()*100)
        velocity = (int)(random.random()*100)
        heat = (int)(random.random()*100)
        json_body = [{"measurement": "tags_data","fields": {"speed": speed, "velocity": velocity, "heat": heat}}]
        client.write_points(json_body)
        time.sleep(10)

if __name__ == "__main__":
    main()
