import appdaemon.plugins.hass.hassapi as hass

vm_list = ["asterisk", "full spectrum", "mcclellan", "minecraft",
          "rostock max", "skynet", "fab lab south pi", "fab lab north pi"]

class VMTracker(hass.Hass):

  def initialize(self):
    self.listen_state(self.presence_change, "device_tracker")

  def presence_change(self, entity, attribute, old, new, kwargs):
    vm = self.friendly_name(entity)
    if vm in vm_list:
      if old != new: 
        if new == "not_home" and old == "home":
          msgString = vm + " is offline"
          self.call_service("notify/slack_statusbots", message = msgString)
        elif new == "home" and old == "not_home":
          msgString = vm + " is online"
          self.call_service("notify/slack_statusbots", message = msgString)
