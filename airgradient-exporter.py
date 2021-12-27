#!/usr/bin/env python3

from sanic import Sanic
from sanic.response import text
import asyncio
import re
import json
import datetime

listen_port = 2474

app = Sanic("airgradient-exporter")

sensor_data = {}

@app.route('/', methods=['GET'])
async def default_get_handler(request):
  return text("Air Gradient Exporter\n")

@app.route('/metrics', methods=['GET'])
async def dump_metrics(request):
  data_expire_seconds = 60
  sr = ''
  
  cur_time = int(datetime.datetime.utcnow().timestamp())
  wifi = { x: sensor_data[x]['wifi'] for x in sensor_data if 'wifi' in sensor_data[x] and sensor_data[x]['timestamp'] > (cur_time - data_expire_seconds) }
  pm02 = { x: sensor_data[x]['pm02'] for x in sensor_data if 'pm02' in sensor_data[x] and sensor_data[x]['timestamp'] > (cur_time - data_expire_seconds) }
  rco2 = { x: sensor_data[x]['rco2'] for x in sensor_data if 'rco2' in sensor_data[x] and sensor_data[x]['timestamp'] > (cur_time - data_expire_seconds) }
  atmp = { x: sensor_data[x]['atmp'] for x in sensor_data if 'atmp' in sensor_data[x] and sensor_data[x]['timestamp'] > (cur_time - data_expire_seconds) }
  rhum = { x: sensor_data[x]['rhum'] for x in sensor_data if 'rhum' in sensor_data[x] and sensor_data[x]['timestamp'] > (cur_time - data_expire_seconds) }
  
  sr = sr + "# HELP wifi_rssi\n"
  sr = sr + "# TYPE wifi_rssi gauge\n"
  for sensor in wifi:
    sr = sr + 'wifi_rssi{sensor_id=\"' + sensor + '\"} ' + str(wifi[sensor]) + "\n"
  
  sr = sr + "# HELP pm02\n"
  sr = sr + "# TYPE pm02 gauge\n"
  for sensor in wifi:
    sr = sr + 'pm02{sensor_id=\"' + sensor + '\"} ' + str(pm02[sensor]) + "\n"
  
  sr = sr + "# HELP rco2\n"
  sr = sr + "# TYPE rco2 gauge\n"
  for sensor in wifi:
    sr = sr + 'rco2{sensor_id=\"' + sensor + '\"} ' + str(rco2[sensor]) + "\n"
  
  sr = sr + "# HELP atmp\n"
  sr = sr + "# TYPE atmp gauge\n"
  for sensor in wifi:
    sr = sr + 'atmp{sensor_id=\"' + sensor + '\"} ' + str(atmp[sensor]) + "\n"
  
  sr = sr + "# HELP rhum\n"
  sr = sr + "# TYPE rhum gauge\n"
  for sensor in wifi:
    sr = sr + 'rhum{sensor_id=\"' + sensor + '\"} ' + str(rhum[sensor]) + "\n"

  return text(sr)

@app.route('/<path:path>', methods=['POST'])
async def log_sensors(request, path=''):
  global sensor_data
  res = re.match('sensors/airgradient:(?P<sensorid>[^\/]+)/measures', path)
  sensorid = None
  if res:
    sensorid = res.group('sensorid')
  if not sensorid:
    raise SanicException('No sensor ID', status_code=404)
  sensor_data[sensorid] = request.json
  sensor_data[sensorid]['timestamp'] = int(datetime.datetime.utcnow().timestamp())
  return text('Received data')

if __name__ == '__main__':
  asyncio.run(app.run(host='0.0.0.0', port=listen_port))
