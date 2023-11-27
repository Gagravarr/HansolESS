# Licensed under the Apache License, Version 2.0
#
# Exports data extracted from a Hansol Technics AIO ESS to
#  various systems

from urllib.request import urlopen


def console_write(s):
   for t,p in (("Current",s.power),("30 Second Average",s.power_30s)):
      print("Power - %s" % t)
      for k in vars(p):
         v = getattr(p,k)
         dk = k.ljust(10)
         dv = ("%0.1f"%v).rjust(7) if v else ""
         print( " - %s %s" % (dk,dv))
      print("")

   print("Battery")
   print(" - Charge %%       %2d%%" % (s.battery.charge_pct))
   print(" - Charging     %s" % (str(s.battery.charging)).rjust(5))
   print("")

   print("Component Electrical Data")
   for vip in s.vips:
      v = lambda f: ("%0.1f" % f).rjust(6)
      print(" - %s" % vip.component)
      print("  * Voltage (V)    %s" % v(vip.voltage))
      print("  * Current (A)    %s" % v(vip.current))
      print("  * Power   (W)    %s" % v(vip.power))
   print("")


def json_write(system):
   import json
   data = {
       "Power": vars(system.power), 
       "Power_30s_Avg": vars(system.power_30s),
       "VIPs":  list(vars(v) for v in system.vips),  
       "Battery": vars(system.battery) 
   }
   print(  json.dumps(data, indent=2) )


def mqtt_write(host, port, topic_all, topic_power, topic_battery,
               topic_electrical, system):
   import paho.mqtt.client as mqtt
   import json

   d_power = vars(system.power)
   d_battery = vars(system.battery),
   d_electrical = { v.component:vars(v) for v in system.vips }
   data = {"power":d_power, "battery":d_battery, "electrical":d_electrical}

   client = mqtt.Client("HansolESS-Monitoring")
   client.connect(host, port, 5)

   if topic_all:
      client.publish(topic_all, json.dumps(data))
   if topic_power:
      client.publish(topic_power, json.dumps(d_power))
   if topic_battery:
      client.publish(topic_battery, json.dumps(d_battery))
   if topic_electrical:
      client.publish(topic_electrical, json.dumps(d_electrical))

   client.disconnect()


def influx_write(base_url, db, username, password, system):
   if not base_url.endswith("/"):
      base_url += "/"
   url = base_url + "write?db=%s" % (db)

   lines = []
   _influx_power(system.power, lines)
   _influx_vips(system.vips, lines)
   _influx_bat(system.battery, lines)

   data = "\n".join(lines)
   with urlopen(url, data.encode("utf-8")) as f:
      resp = f.read()
      if resp:
         print("Unexpected InfluxDB response:")
         print(resp)

def _influx_power(power, lines):
   for thing in vars(power):
      lines.append("power,kind=%s power=%0.1f" % (thing,getattr(power,thing)))
def _influx_vips(vips, lines):
   for vip in vips:
      f = ",".join("%s=%s" % (k,v) for k,v in vip.items())
      lines.append("electrical,kind=%s %s" % (vip.component, f))
def _influx_bat(battery, lines):
   lines.append("battery,kind=battery charge=%0.1f,charge_pct=%0d" %
                (battery.charge_01, battery.charge_pct))


def prompg_write(base_url, job, username, password, system):
   from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
   from prometheus_client.exposition import basic_auth_handler

   def auth_handler(url, method, timeout, headers, data):
      return basic_auth_handler(url, method, timeout, headers, data, username, password)
   registry = CollectorRegistry()

   gp = Gauge("power_watts", "Power", ["component"], registry=registry)
   for thing in vars(system.power):
      gp.labels(component=thing).set( getattr(system.power, thing) )

   gev = Gauge("electrical_volts", "Voltage", ["component"], registry=registry)
   gei = Gauge("electrical_amps",  "Current", ["component"], registry=registry)
   gep = Gauge("electrical_watts", "Power", ["component"], registry=registry)
   for vip in system.vips:
      component = vip.component.replace('-','_')
      gev.labels(component=component).set(vip.voltage)
      gei.labels(component=component).set(vip.current)
      gep.labels(component=component).set(vip.power)

   gb = Gauge('battery_ratio', 'Battery Charge', registry=registry)
   gb.set(system.battery.charge_01)

   push_to_gateway(base_url, job=job, registry=registry, handler=auth_handler)
