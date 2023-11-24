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

p.add_argument('--mqtt-host',metavar='MQTT_HOST',default='localhost',
   help='Hostname / IP Address of the MQTT Server')
p.add_argument('--mqtt-port',metavar='MQTT_PORT',default=1883,
   help='Port of the MQTT Server')
p.add_argument('--mqtt-topic-all',metavar='MQTT_TOPIC_ALL',default='power',
   help='MQTT Topic to publish all data to, use an empty string to disable')
p.add_argument('--mqtt-topic-power',metavar='MQTT_TOPIC_POWER',
   help='MQTT Topic to publish power-related data to')
p.add_argument('--mqtt-topic-battery',metavar='MQTT_TOPIC_BATTERY',
   help='MQTT Topic to publish battery-related data to')
p.add_argument('--mqtt-topic-electrical',metavar='MQTT_TOPIC_ELEC',
   help='MQTT Topic to publish electrical-related data to')

p.add_argument('--influx-url',metavar='INFLUX_URL',
   default='http://localhost:8086/',
   help='URL of the InfluxDB server')
p.add_argument('--influx-db',metavar='INFLUX_DB',default='power',
   help='Database to use on the InfluxDB server, must already exist')
p.add_argument('--influx-user',metavar='INFLUX_USER',
   help='InfluxDB server username')
p.add_argument('--influx-pass',metavar='INFLUX_PASS',
   help='InfluxDB server password')

p.add_argument('--prom-pg-url',metavar='PROM_PG_URL',
   default='http://localhost:9091/',
   help='URL of the Prometheus Push-Gateway server')
p.add_argument('--prom-job',metavar='PROM_JOB',default='power',
   help='Job to write to on the Prometheus Push-Gateway')
p.add_argument('--prom-user',metavar='PROM_USER',
   help='Prometheus server username')
p.add_argument('--prom-pass',metavar='PROM_PASS',
   help='Prometheus server password')

# TODO prometheus


# Find out what they want us to do
args = p.parse_args()

# Have the data fetched and extracted
system = extract_remote(args.host, args.port)

# Run the outputs/exports
for output in args.output:
   if output == "console":
      console_write(system)
   elif output == "json":
      json_write(system)
   elif output == "mqtt":
      mqtt_write(args.mqtt_host, args.mqtt_port, args.mqtt_topic_all, 
                 args.mqtt_topic_power, args.mqtt_topic_battery, 
                 args.mqtt_topic_electrical, system)
   elif output == "influx":
      influx_write(args.influx_url, args.influx_db,
                   args.influx_user, args.influx_pass, system)
   elif output == "prometheus":
      # TODO prometheus
      raise Exception("TODO: Prometheus")
   else:
      raise Exception("Unsupported output type: %s" % output)
