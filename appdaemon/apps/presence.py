import appdaemon.plugins.hass.hassapi as hass

class Presence_Detect(hass.Hass):
  
  def initialize(self):
    self.log("Testing")
    self.listen_state(self.presence_changed, "input_boolean.testing")
    
  def presence_changed(self, entity, attribute, old, new, kwargs):
    self.log(new)
    if self.get_state("device_tracker.apollo") == "home":
        self.log("Adnan came home")
    else:
        self.log("Adnan left")
