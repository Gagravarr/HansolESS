# Licensed under the Apache License, Version 2.0

from dataclasses import dataclass

@dataclass
class VIP:
   "Voltage (V), Current (I) and Power (P), for the different components"
   component: str
   voltage: float = None
   current: float = None
   power: float = None
   _attrs = ("voltage","current","power")

   def is_complete(self):
      return self.voltage != None and self.current != None and self.power != None
   def items(self):
      return [(k,getattr(self,k)) for k in VIP._attrs]
   def __repr__(self):
      return "%s " % (self.component) + \
             ",".join(["%s=%0.1f" % (k,v) for k,v in self.items()])

@dataclass
class Battery:
   "Battery state"
   charge_pct: float = None
   charging: bool = False

   def __init__(self, charge_pct, charging):
      self.charging = charging
      self.set_charge(charge_pct)

   def set_charge(self, charge_pct):
      self.charge_pct = charge_pct
      self.charge_01 = charge_pct / 100.0

@dataclass
class Power:
   "Power use and sources"
   load: float = None
   pv: float = None
   inv: float = None
   bat: float = None
   grid: float = None

@dataclass
class System:
   power: Power = None
   power_30s: Power = None
   battery: Battery = None
   vips: list = None
