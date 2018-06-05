import appdaemon.appapi as appapi

class LightLWT(appapi.AppDaemon):

  def initialize(self):
    self.listen_state(self.lwt_triggered, entity="light", new="unavailable", duration="60")

  def lwt_triggered(self, entity, attribute, old, new, kwargs):
    light = self.friendly_name(entity)
    msgString = light + " is offline (LWT)"
    self.call_service("notify/slack_statusbots", message = msgString)

