import appdaemon.plugins.hass.hassapi as hass


class Motion(hass.Hass):

  def initialize(self):
    self.handle = None
  
    if "sensor" in self.args:
      self.listen_state(self.motion_on, self.args["sensor"], new="1")
      self.listen_state(self.motion_off, self.args["sensor"], new="0", duration=self.args["delay"])
    else:
      self.log("No sensor specified, doing nothing")

    if "entity_id" in self.args:
      self.listen_state(self.off, self.args["entity_id"])
      self.listen_state(self.off, self.args["entity_id"])
    else:
      self.log("No light specified, doing nothing") 

  def off(self, entity, attribute, old, new, kwargs):
    if self.get_state(self.args["entity_id"]) == "off":
      self.log("reset handle, because {} was turned off".format(self.args["entity_id"]))
      self.cancel_timer(self.handle)
      self.handle = None
    
  def motion_on(self, entity, attribute, old, new, kwargs):
    if self.get_state("device_tracker.zeus") == "home":
        if self.args["entity_id"] == "light.living_room":
            if self.get_state("sensor.plex_sensor") != "Playing":
                self.log("Good Ares is not playing plex")
                if int(self.get_state("sensor.living_room_light")) <= 7500:
                    self.light_on(self, self.args["entity_id"])
        else:
            self.light_on(self, self.args["entity_id"])
    else:
        self.call_service("notify/pushbullet", target= "channel/anethass", title = "Home Assistant", message = "Movement at home")
        self.log("Notification sent for motion at home")
  
  def light_on(self, entity, attribute):
        self.log(self.args["entity_id"] + " turned on because motion was detected and Zeus is home")
        self.turn_on(self.args["entity_id"], brightness_pct = int(self.args["brightness_pct"]))
        self.cancel_timer(self.handle)
        self.handle = None

  def motion_off(self, entity, attribute, old, new, kwargs):
    if self.get_state(self.args["entity_id"]) == "on":
      self.log("Set brightness to " + str(self.args["dim_brightness_pct"]) + " and turn off light in " + str(self.args["dim_delay"]) + " seconds")
      self.call_service("light/turn_on", entity_id = (self.args["entity_id"]), brightness_pct = int(self.args["dim_brightness_pct"]))
      self.cancel_timer(self.handle)
      self.handle = self.run_in(self.light_off, int(self.args["dim_delay"]))
   
  def light_off(self, kwargs):
    self.log(self.args["entity_id"] + " turn off")
    self.turn_off(self.args["entity_id"])
            
