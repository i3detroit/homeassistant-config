# Directory Contents
## Generic config files
* `wifi.yaml` - wifi connection info, referencing secrets.yaml
* `secrets.yaml`
* `esp_home_components.yaml` - essential ESPHome components like ota, logger, api, etc

## Hardware configs
Templates for a variety of hardware. Mostly named `[hardware]_[function].yaml`. For example `sonoff_basic_light.yaml` gives you a light entity in Home Assistant, while `sonoff_basic_switch.yaml` gives you a switch. There's probably a way to do this better since the two files are almost identical, but meh.
