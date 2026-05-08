# ESPHome

## Naming conventions

* Always use dashes, not underscores, in `device_name` to prevent mDNS issues
* Match the YAML filename to `device_name`
* Don't duplicate the name across entities (sensors, controls, etc) only keep it at the device's `pretty_name`

## Generic config files
* `wifi.yaml`: wifi connection info, referencing secrets.yaml
* `secrets.yaml`: not in git repo
* `esp_home_components.yaml`: essential ESPHome components like ota, logger, api, etc

## Hardware configs

Templates for a variety of hardware. Mostly named `[hardware]_[function].yaml`. For example `sonoff_basic_light.yaml` gives you a light entity in Home Assistant, while `sonoff_basic_switch.yaml` gives you a switch. There's probably a way to do this better since the two files are almost identical, but meh.

Note that when adding devices that act as a trigger for other devices, like "virtual" switches, you will need to check "Allow the device to perform Home Assistant actions." under device options.
