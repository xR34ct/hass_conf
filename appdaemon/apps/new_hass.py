import appdaemon.plugins.hass.hassapi as hass


class HassUpdate(hass.Hass):

  def initialize(self):
     self.log("Started update monitoring")
     self.listen_state(self.message, "updater.updater")
  def message (self, entity, attribute, old, new, kwargs):
     self.call_service("notify/pushbullet", target = "channel/anethass", title = "Home Assistant", message = "There is an update to Homeassistant")
     self.log("Notification sent for new update")