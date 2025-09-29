# Advanced Room Lighting Blueprint (Hubitat Style)

This Home Assistant blueprint replicates the comprehensive functionality of Hubitat's Room Lighting app, providing sophisticated room automation with motion detection, contact sensors, buttons, and advanced lighting control.

## Features Implemented

### 🏠 Home Assistant Area Integration
- **Area Selection**: Choose from your configured Home Assistant Areas
- **Automatic Naming**: Room name automatically populated from area name
- **Dual Device Selectors**: Each device type has both area-filtered and all-area options
- **Smart Combination**: Blueprint automatically combines selections from both selectors
- **Name Override**: Option to override area name with custom room name
- **Flexible Setup**: Use area filtering for convenience or manual selection for precision
- **Best of Both Worlds**: Get area filtering benefits while maintaining full control

### ✅ Core Hubitat Room Lighting Features
- **Multiple Activation Methods**: Motion sensors, contact sensors, buttons/switches
- **Per-Mode Settings**: Different brightness and color temperature for Away/Day/Evening/Night modes
- **Advanced Turn-Off Logic**: Configurable timeouts per mode, require all sensors clear
- **Illuminance Control**: Prevent activation during bright conditions
- **Fade Times**: Smooth transitions for all light changes
- **Activation Delays**: Configurable delays before activation
- **Partial Activation Control**: Options for handling partially on/off states
- **Weekend/Weekday Differences**: Different timeouts for weekends
- **Override Prevention**: Prevent motion from turning off manually adjusted lights

### ✅ Advanced Home Assistant Features
- **Color Temperature Control**: Automatic adjustment based on mode
- **Occupancy Tracking**: Internal state tracking with events
- **Conditional Activation**: Disable when TV is on or someone is sleeping
- **Debug Logging**: Comprehensive logging for troubleshooting
- **Event System**: Fires events for integration with other automations
- **Template-Based Logic**: Sophisticated condition checking

## Prerequisites

### Required Helper Entity
Create this input_select in your `configuration.yaml` or via the UI:

```yaml
input_select:
  home_mode:
    name: Home Mode
    options:
      - Away
      - Day
      - Evening
      - Night
    initial: Day
```

### Recommended Integrations
- **Motion Sensors**: Z-Wave JS, Zigbee2MQTT, ZHA
- **Contact Sensors**: Z-Wave JS, Zigbee2MQTT, ZHA
- **Button Devices**: Z-Wave JS, Zigbee2MQTT, ZHA, Philips Hue
- **Illuminance Sensors**: Any integration providing lux values

## Installation

1. Copy `room_lighting_advanced.yaml` to your Home Assistant `blueprints/automation/` directory
2. Restart Home Assistant or reload automations
3. Go to Settings → Automations & Scenes → Blueprints
4. Find "Advanced Room Lighting (Hubitat Style)" and create a new automation

## Configuration Guide

### Basic Setup
1. **Area Selection**: Select a Home Assistant Area to automatically populate the room name and enable area filtering
2. **Room Name Override**: Optionally override the area name with a custom room name
3. **Device Selection**: For each device type, you'll see two options:
   - **Area Filtered**: Shows only devices from the selected area (recommended)
   - **All Areas**: Shows devices from any area (for cross-room setups)
4. **Smart Combination**: The blueprint automatically combines your selections from both options

**Device Types Available**:
- **Lights to Control**: Lights, switches, and dimmers
- **Motion Sensors**: Motion detection devices
- **Contact Sensors**: Door/window sensors (optional)
- **Button Devices**: Buttons or switches for manual control (optional)
- **Additional Sensors**: Illuminance, TV/media player, and sleep sensors

**Usage Tip**: Most users will only need the area-filtered selectors. Use the "All Areas" selectors only when you need devices from other rooms (e.g., hallway motion sensor for bedroom lights).

### Activation Settings
- **Enable Motion Activation**: Turn on for motion-based lighting
- **Enable Contact Activation**: Turn on to activate when doors/windows open
- **Enable Button Activation**: Turn on for button/switch control
- **Illuminance Control**: Prevent activation during bright conditions

### Per-Mode Light Settings
Configure different brightness levels for each mode:
- **Away Mode**: Lower brightness for security/energy savings (default: 30%)
- **Day Mode**: Comfortable daytime brightness (default: 75%)
- **Evening Mode**: Bright evening lighting (default: 85%)
- **Night Mode**: Dim lighting for nighttime (default: 20%)

### Color Temperature (Optional)
Enable automatic color temperature adjustment:
- **Away**: 3000K (warm)
- **Day**: 4000K (neutral)
- **Evening**: 3000K (warm)
- **Night**: 2200K (very warm)

### Turn-Off Settings
Configure different timeouts for each mode:
- **Away Mode**: Quick timeout (default: 2 minutes)
- **Day Mode**: Standard timeout (default: 10 minutes)
- **Evening Mode**: Longer timeout (default: 15 minutes)
- **Night Mode**: Medium timeout (default: 5 minutes)

### Advanced Options
- **Require All Motion Clear**: All motion sensors must be inactive before turning off
- **Require Contact Closed**: Contact sensors must be closed before turning off
- **Prevent Motion Override**: Don't turn off lights after manual changes
- **Weekend Settings**: Use different timeouts on weekends
- **TV/Sleep Conditions**: Disable activation when TV is on or someone is sleeping

## Usage Examples

### Basic Motion Lighting with Area
```yaml
# Minimal configuration using Home Assistant Area
area_selector: living_room  # Select your Living Room area
# room_name will automatically be "Living Room" from the area
# Device selectors will be filtered to show only Living Room devices
enable_motion_activation: true
```

### Basic Motion Lighting (Manual)
```yaml
# Minimal configuration for simple motion lighting without area
room_name: "Living Room"
lights_to_control:
  entity_id: 
    - light.living_room_ceiling
    - light.living_room_lamp
motion_sensors:
  entity_id:
    - binary_sensor.living_room_motion
enable_motion_activation: true
```

### Advanced Multi-Sensor Setup with Area
```yaml
# Full-featured room using Home Assistant Area
area_selector: master_bedroom  # Select Master Bedroom area
room_name: "Master Bedroom"  # Optional override
# All device selectors will be filtered to Master Bedroom area
illuminance_sensor: sensor.bedroom_illuminance
enable_illuminance_control: true
illuminance_threshold: 30
disable_when_sleeping: true
sleep_sensor: input_boolean.bedroom_sleep_mode
enable_color_temp: true
require_all_motion_clear: true
enable_weekend_settings: true
weekend_timeout_multiplier: 2.0
```

## Events and Integration

The blueprint fires events that can be used by other automations:

### Events Fired
- `room_lighting_activated`: When lights are turned on
- `room_lighting_deactivated`: When lights are turned off

### Event Data
```yaml
# Activation event
event_type: room_lighting_activated
data:
  room: "Living Room"
  trigger: "motion"  # or "contact", "button"
  mode: "evening"
  brightness: 85

# Deactivation event
event_type: room_lighting_deactivated
data:
  room: "Living Room"
  trigger: "motion_timeout"
  timeout_minutes: 15
```

### Using Events in Other Automations
```yaml
# Example: Announce when room lighting activates
automation:
  - alias: "Announce Room Lighting"
    trigger:
      - platform: event
        event_type: room_lighting_activated
    action:
      - service: tts.speak
        data:
          message: "{{ trigger.event.data.room }} lights activated"
```

## Troubleshooting

### Enable Debug Logging
Set `enable_debug_logging: true` to see detailed logs in Home Assistant's log file.

### Common Issues
1. **Lights don't turn on**: Check illuminance threshold and TV/sleep conditions
2. **Lights don't turn off**: Verify motion sensor states and timeout settings
3. **Wrong brightness**: Check current mode in `input_select.home_mode`
4. **Color temperature not working**: Ensure lights support color temperature

### Log Messages
Look for messages starting with your room name in the Home Assistant logs:
```
Living Room: Motion detected, activating lights (Mode: evening, Brightness: 85%)
Living Room: Motion timeout (15 min), turning off lights
Living Room: Mode changed to night, adjusting lights
```

## Comparison to Hubitat Room Lighting

### Fully Replicated Features ✅
- Multiple activation methods (motion, contact, buttons)
- Per-mode brightness settings
- Advanced turn-off conditions
- Illuminance-based activation
- Fade times and delays
- Partial activation handling
- Weekend/weekday differences

### Enhanced Features 🚀
- Color temperature automation
- Event system for integration
- Template-based condition logic
- Advanced debug logging
- TV and sleep mode integration

### Limitations vs Hubitat 📝
- No built-in scene transitions (use separate automations)
- No direct Zigbee group messaging (uses HA services)
- Simplified UI compared to Hubitat's custom interface
- No built-in activator device (use events instead)

## Advanced Customization

### Multiple Room Setup
Create separate automations for each room using this blueprint. Each can have different settings while sharing the same `input_select.home_mode`.

### Integration with Other Systems
Use the events fired by this blueprint to integrate with:
- Security systems
- Energy monitoring
- Voice announcements
- Dashboard updates
- Other room automations

### Custom Mode Automation
Create automations to automatically change `input_select.home_mode` based on:
- Time of day
- Presence detection
- Sleep sensors
- Security system state

This blueprint provides a comprehensive room lighting solution that matches and in some cases exceeds the functionality of Hubitat's Room Lighting app, while taking full advantage of Home Assistant's powerful automation engine and integration capabilities.
