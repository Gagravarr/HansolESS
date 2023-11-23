#!/usr/bin/python3
# Licensed under the Apache License, Version 2.0
#
# Extracts data from a Hansol Technics AIO ESS

import argparse
from extract import extract_remote
from export import *

class ExplicitDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):
   def _get_help_string(self, action):
      if action.default is None or action.default is False:
         return action.help
      return super()._get_help_string(action)

p = argparse.ArgumentParser(
      prog='command.py', add_help=False,
      description='Extracts data from a Hansol Technics AIO ESS',
      formatter_class=ExplicitDefaultsHelpFormatter
)

p.add_argument("--help", action="help")

p.add_argument('-h','--host',metavar='HOST',required=True,
   help='Hostname / IP Address of the ESS')
p.add_argument('-p','--port',metavar='PORT',default=21710,
   help='Port of the ESS interface')

p.add_argument('-o','--output',metavar='OUTPUT',required=True,
   choices=("console","json","mqtt","influx","prometheus"),
   help='What systems/formats to output to', nargs='+')

p.add_argument('--mqtt-host',metavar='MQTT_HOST',
   help='Hostname / IP Address of the MQTT Server')
p.add_argument('--mqtt-port',metavar='MQTT_PORT',default=1883,
   help='Port of the MQTT Server')
p.add_argument('--mqtt-topic',metavar='MQTT_TOPIC',default='power',
   help='MQTT Topic to publish data to')

p.add_argument('--influx-url',metavar='INFLUX_URL',
   default='http://localhost:8086/',
   help='URL of the InfluxDB server')
p.add_argument('--influx-db',metavar='INFLUX_DB',default='power',
   help='Database to use on the InfluxDB server, must already exist')
p.add_argument('--influx-user',metavar='INFLUX_USER',
   help='InfluxDB server username')
p.add_argument('--influx-pass',metavar='INFLUX_PASS',
   help='InfluxDB server password')

# TODO prometheus

args = p.parse_args()
print(args)

# TODO Rest

system = extract_remote(args.host, args.port)
influx_write("10.5.2.1", 8086, "power", system)
