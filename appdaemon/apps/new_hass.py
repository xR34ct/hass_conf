import appdaemon.plugins.hass.hassapi as hass


class HassUpdate(hass.Hass):

  def initialize(self):
     self.listen_state(self.message, "binary_sensor.test")
     self.log("Started update monitoring")
  def message (self, entity, attribute, old, new, kwargs):
     self.call_service("notify/pushbullet", title = "Home Assistant", message = "There is an update to Homeassistant")
     self.log("Notification sent for new update")