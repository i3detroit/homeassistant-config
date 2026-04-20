#!/bin/bash
set -euo pipefail

devices="
small_bathroom_exhaust_fan.yaml
thermostat-A-NE.yaml"


for dev in $devices ; do
	esphome run --no-logs "$dev"
done
