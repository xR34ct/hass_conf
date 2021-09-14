import appdaemon.plugins.hass.hassapi as hass
import time

class SetVolume(hass.Hass):

  def initialize(self):
    self.listen_state(self.volchanged, "input_number.spotify_volume")
    
  def volchanged(self, entity, attribute, old, new, kwargs):
    self.log("Volume Set")
    VOL = float(self.get_state("input_number.spotify_volume"))/100
    self.call_service("media_player/volume_set", entity_id = "media_player.spotify", volume_level = VOL)
        
class SyncVolume(hass.Hass):

  def initialize(self):
    self.listen_state(self.state_changed, "sensor.spotify_volume")
    self.listen_event(self.ha_event, "plugin_started")
    self.listen_event(self.appd_event, "appd_started")
    
  def state_changed(self, entity, attribute, old, new, kwargs):
    self.run_in(self.volchanged, 1)
    
  def ha_event(self, event_name, data, kwargs):
    self.log("Home Assistant restart detected")
    self.run_in(self.volchanged, 10)
    
  def appd_event(self, event_name, data, kwargs):
    self.log("AppDaemon restart detected")
    self.run_in(self.volchanged, 10)
    
  def volchanged(self, kwargs):
    VOL = float(self.get_state("sensor.spotify_volume"))*100
    self.log("Volume Changed")
    #self.log(VOL)
    self.call_service("input_number/set_value", entity_id = "input_number.spotify_volume", value = VOL)
    
class SetShuffle(hass.Hass):

  def initialize(self):
    self.listen_state(self.shuffle, "input_boolean.spotify_shuffle")
    
  def shuffle(self, entity, attribute, old, new, kwargs):
    self.log("Shuffle Set")
    if new == "on":
        SHUFFLE = "true"
    else:
        SHUFFLE = "false"
    self.call_service("media_player/shuffle_set", entity_id = "media_player.spotify", shuffle = SHUFFLE)
    
class SyncShuffle(hass.Hass):
  
  def initialize(self):
    self.listen_state(self.state_changed, "sensor.spotify_shuffle")
    self.listen_event(self.ha_event, "plugin_started")
    self.listen_event(self.appd_event, "appd_started")
    
  def state_changed(self, entity, attribute, old, new, kwargs):
    self.run_in(self.shuffle, 1)
    
  def ha_event(self, event_name, data, kwargs):
    self.log("Home Assistant restart detected")
    self.run_in(self.shuffle, 10)
    
  def appd_event(self, event_name, data, kwargs):
    self.log("AppDaemon restart detected")
    self.run_in(self.shuffle, 10)
    
  def shuffle(self, kwargs):
    self.log("Shuffle Changed")
    if self.get_state("sensor.spotify_shuffle") == "True":
        self.call_service("input_boolean/turn_on", entity_id = "input_boolean.spotify_shuffle")
    else:
        self.call_service("input_boolean/turn_off", entity_id = "input_boolean.spotify_shuffle")

class Source(hass.Hass):
  
  def initialize(self):
    self.listen_state(self.state_changed, "sensor.spotify_source")
    self.listen_event(self.ha_event, "plugin_started")
    self.listen_event(self.appd_event, "appd_started")
    
  def state_changed(self, entity, attribute, old, new, kwargs):
    self.run_in(self.source, 1)
    
  def ha_event(self, event_name, data, kwargs):
    self.log("Home Assistant restart detected")
    self.run_in(self.source, 10)
    
  def appd_event(self, event_name, data, kwargs):
    self.log("AppDaemon restart detected")
    self.run_in(self.source, 10)
    
  def source(self, kwargs):
    self.log("Source Changed")
    OPTION = self.get_state("sensor.spotify_source")
    self.call_service("input_select/select_option", entity_id = "input_select.spotify_source", option = OPTION)
    
class StopPlay(hass.Hass):

  def initialize(self):
    #self.log("Started")
    self.listen_state(self.came_home, "device_tracker.apollo", new = "home")
    self.listen_state(self.left, "device_tracker.apollo", new = "not_home")
    
  def left(self, entity, attribute, old, new, kwargs):
    if self.get_state("sensor.spotify_source") == "HADES" or self.get_state("sensor.spotify_source") == "Ares":
    #    self.log("Hades or Ares is source")
        if self.get_state("media_player.spotify") == "playing":
    #        self.log("Playing so pausing")
            self.call_service("media_player/media_pause", entity_id = "media_player.spotify")
        
  def came_home(self, entity, attribute, old, new, kwargs):
    if self.get_state("media_player.spotify") == "playing" and self.get_state("device_tracker.hades") == "home":# and self.get_state("input_select.spotify_source") == "Zeus":
    #    self.log("Hades is online and Zeus is playing so tranfering")
        self.call_service("media_player/select_source", entity_id = "media_player.spotify", source = "HADES")
