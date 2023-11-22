#!/usr/bin/python3
# Licensed under the Apache License, Version 2.0
#
# Extracts data from a Hansol Technics AIO ESS

from argparse import ArgumentParser

p = ArgumentParser(
      prog='command.py', add_help=False,
      description='Extracts data from a Hansol Technics AIO ESS'
)

p.add_argument("--help", action="help")

p.add_argument('-h','--host',metavar='HOST',required=True,
   help='Hostname / IP Address of the ESS')
p.add_argument('-p','--port',metavar='PORT',default=21710,
   help='Port of the ESS interface, default 21710')

p.add_argument('--mqtt-host',metavar='MQTT_HOST',
   help='Hostname / IP Address of the MQTT Server')
p.add_argument('--mqtt-port',metavar='MQTT_PORT',default=1883,
   help='Port of the MQTT Server, default 1883')
p.add_argument('--mqtt-topic',metavar='MQTT_TOPIC',default='power',
   help='MQTT Topic to publish data to, default "power"')

args = p.parse_args()
print(args)

# TODO Rest
