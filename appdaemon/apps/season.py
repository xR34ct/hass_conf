import appdaemon.plugins.hass.hassapi as hass
from datetime import date

class Season(hass.Hass):

  def initialize(self):
    self.log("Started wait for new season")
    self.listen_state(self.changed, "sensor.season_checker")
    
  def changed(self, entity, attribute, old, new, kwargs):
    self.log("Season changed")
    if self.get_state("sensor.season_checker") == "Spring":
        NEW_DATE = date.fromordinal(int(date.toordinal(date.today())) - 8).strftime("%Y-%m-%d")
        self.log(NEW_DATE)
    
    else:
        NEW_DATE = date.fromordinal(int(date.toordinal(date.today())) - 6).strftime("%Y-%m-%d")
        self.log(NEW_DATE)
    
    self.call_service("input_datetime/set_datetime", entity_id = "input_datetime.season_date", date = NEW_DATE)
    
    self.call_service("notify/pushbullet", target= "channel/anethass", title = "Home Assistant", message = "Seasons have changed")