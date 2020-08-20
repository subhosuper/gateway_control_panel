from pymongo import MongoClient
from influxdb import InfluxDBClient

def tag_value():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['gateway_control']
    collection = db['tags']

    influx_client = InfluxDBClient('localhost',8086,'root','root','gateway_control')


    query = collection.find()
    list_query = list(query)
    list_query_count = len(list_query)
    list_of_tags = []
    influx_value_list = []

    for tag_name in range(0,list_query_count):
        result = list_query[tag_name]['tags']
        influx_query = "select last("+result+") from tags_data"
        list_of_tags.append(result)
        result_query = influx_client.query(influx_query)
        result_query_string = list(result_query)
        result_query_string_final = result_query_string[0][0]['last']
        influx_value_list.append(result)
        influx_value_list.append(result_query_string_final)
    return influx_value_list