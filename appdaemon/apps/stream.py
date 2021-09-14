import appdaemon.plugins.hass.hassapi as hass
import datetime

#
# Hello World App
#
# Args:
#

class stream_temp(hass.Hass):

  def initialize(self):
    self.log("Stream Temp has started")
    time = datetime.time(0,0,0)
    self.run_minutely(self.stream_temp_c, time)
#    runtime = datetime.datetime.now()
#    addseconds = (round((runtime.minute*60 + runtime.second)/300)+1)*900
#    runtime = runtime.replace(minute=0, second=0, microsecond=0) + datetime.timedelta(seconds=addseconds)
#    self.run_every(self.stream_temp_c,runtime,900)

  def stream_temp_c(self, kwargs):
#    self.log("Test")
    current_temp = self.get_state(entity="sensor.living_room_sensor_temperature")
    file = "/etc/avdagic.net/stream_temp.txt"
    f = open(file,"w+")
    f.write("Current temperature in apartment: " + current_temp)
    f.close

    #self.log("Hello from AppDaemon")
    #self.log("You are now ready to run Apps!")
