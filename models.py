# Licensed under the Apache License, Version 2.0

class VIP:
   "Voltage (V), Current (I) and Power (P), for the different components"
   attrs = ("voltage","current","power")

   def __init__(self, component, voltage=None, current=None, power=None):
      self.component = component
      self.voltage = voltage
      self.current = current
      self.power = power

   def is_complete(self):
      return self.voltage != None and self.current != None and self.power != None
   def items(self):
      return [(k,getattr(self,k)) for k in VIP.attrs]
   def __repr__(self):
      return "%s " % (self.component) + \
             ",".join(["%s=%0.1f" % (k,v) for k,v in self.items()])

class Battery:
   "Battery state"
   def __init__(self, charge_pct, charging):
      self.charge_pct = charge_pct
      self.charge_01 = charge_pct / 100.0
      self.charging = charging

class Power:
   "Power use and sources"
   pass

class System:
   def __init__(self, power=None, battery=None, vips=None):
      self.power = power
      self.battery = battery
      self.vips = vips
