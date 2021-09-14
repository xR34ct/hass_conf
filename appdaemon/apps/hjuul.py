import appdaemon.plugins.hass.hassapi as hass
import time


class Hjuul(hass.Hass):
  
  def initialize(self):
    self.listen_state(self.hjuul_on, "input_boolean.hjuul", new="on")
    self.listen_state(self.hjuul_off, "input_boolean.hjuul", new="off")
    
  def hjuul_on(self, entity, attribute, old, new, kwargs):
    self.log("Time for Hjuul")
    sleep_timer = 1.5
    for i in range(10):
      self.call_service("light/turn_on", entity_id = 'light.extended_color_light_1', color_name = 'red', transition = '1')
      time.sleep(sleep_timer)
      self.call_service("light/turn_on", entity_id = 'light.extended_color_light_1', color_name = 'green', transition = '1')
      time.sleep(sleep_timer)
    self.call_service("input_boolean/turn_off", entity_id = 'input_boolean.hjuul')

  def hjuul_off(self, entity, attribute, old, new, kwargs):
    self.log("No more Hjuul")
    self.call_service("light/turn_off", entity_id = 'light.extended_color_light_1')