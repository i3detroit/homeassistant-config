import appdaemon.plugins.hass.hassapi as hass

northArchTop = "cmnd/i3/inside/elab/accent/arch-north/"
southArchTop = "cmnd/i3/inside/elab/accent/arch-south/"

commands = {
    "FFF807": ["POWER", "OFF"],
    "FFB04F": ["POWER", "ON"],
    "FF906F": ["Dimmer", "+"],
    "FFB847": ["Dimmer", "-"],
    "FF30CF": ["Scheme", "3"],
    "FFB24D": ["Scheme", "4"],
    "FF00FF": ["Scheme", "4"],
    "FF58A7": ["Scheme", "2"],
    "FF9867": ["Color", "FF0000"],
    "FFD827": ["Color", "00FF00"],
    "FF8877": ["Color", "0000FF"],
    "FFA857": ["Color", "FFFFFF"],
    "FFE817": ["Color", "e85133"],
    "FF48B7": ["Color", "18f960"],
    "FF6897": ["Color", "5555ff"],
    "FF02FD": ["Color", "ff7700"],
    "FF32CD": ["Color", "00FFFF"],
    "FF20DF": ["Color", "7700ff"],
    "FF50AF": ["Color", "ff9944"],
    "FF7887": ["Color", "00cccc"],
    "FF708F": ["Color", "AA00ff"],
    "FF38C7": ["Color", "FFFF00"],
    "FF28D7": ["Color", "009999"],
    "FFF00F": ["Color", "FF00FF"],
}


class IRRemote(hass.Hass):
    def initialize(self):
        self.listen_state(self.command_received, entity="sensor.elab_arch_north_ir_receiver")
        self.listen_state(self.command_received, entity="sensor.elab_arch_south_ir_receiver")

    def command_received(self, entity, attribute, old, new, kwargs):
        if new in commands.keys():
            top = commands[new][0]
            pl = commands[new][1]
            self.call_service("mqtt/publish", topic=northArchTop + top, payload=pl)
            self.call_service("mqtt/publish", topic=southArchTop + top, payload=pl)
