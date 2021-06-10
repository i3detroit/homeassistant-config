nums = range(1, 103)

for n in nums:
    config = f'''<<: !include common/sonoff_basic_light.yaml
<<: !include common/api.yaml

substitutions:
  device_name: "light_{n:03d}"
  pretty_name: "Light {n:03d}"
  ui_name: "Light {n:03d}"
  icon: "mdi:lightbulb"
'''
    with open(f"light_{n:03d}.yaml", "w") as f:
        f.write(config)