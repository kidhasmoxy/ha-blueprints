# Mode Manager Blueprint

A comprehensive Home Assistant blueprint that replicates the functionality of Hubitat's Mode Manager. This blueprint provides automated mode management based on time, presence, button events, and switch states using an `input_select` entity to store the current mode.

## Features

- **Time-Based Mode Changes**: Automatic mode switching based on specific times or sunrise/sunset
- **Presence-Based Mode Changes**: Mode switching based on person/device tracker presence
- **Button-Based Mode Changes**: Mode control via button device events
- **Switch-Based Mode Changes**: Mode control via switch state changes
- **Skip Logic**: Prevent certain modes (like "Away") from being overridden by time-based triggers
- **Startup Mode Setting**: Optionally set mode based on time when Home Assistant starts
- **Flexible Configuration**: Supports custom mode names and multiple trigger types

## Prerequisites

### Required Entities

1. **Input Select Entity**: You must create an `input_select` entity to store your modes. Example configuration in `configuration.yaml`:

```yaml
input_select:
  house_mode:
    name: House Mode
    options:
      - Day
      - Evening
      - Night
      - Away
    initial: Day
    icon: mdi:home-variant
```

### Optional Entities

- **Person/Device Tracker entities** for presence detection
- **Button devices** that generate events (ZHA, deCONZ, Hue, etc.)
- **Switch/Light entities** for switch-based triggers

## Installation

1. Download the `mode_manager.yaml` blueprint file
2. Place it in your Home Assistant `blueprints/automation/` directory
3. Restart Home Assistant or reload automations
4. Go to **Settings** → **Automations & Scenes** → **Blueprints**
5. Find "Mode Manager (Hubitat Style)" and click **Create Automation**

## Configuration

### Mode Configuration

- **Mode Input Select Entity**: Select your `input_select` entity that will store the current mode

### Time-Based Mode Changes

Enable automatic mode changes based on time with clear trigger options:

- **Enable Time-Based Mode Changes**: Toggle to enable/disable all time-based triggers

#### Day Mode Configuration
- **Day Mode Name**: Name for your daytime mode (default: "Day")
- **Day Mode Trigger**: Choose between "Fixed Time" or "Sunrise (with optional offset)"
- **Day Mode - Fixed Time**: Specific time to trigger Day mode (only used if "Fixed Time" selected)
- **Day Mode - Sunrise Offset**: Minutes before (-) or after (+) sunrise (only used if "Sunrise" selected)

#### Evening Mode Configuration  
- **Evening Mode Name**: Name for your evening mode (default: "Evening")
- **Evening Mode Trigger**: Choose between "Fixed Time" or "Sunset (with optional offset)"
- **Evening Mode - Fixed Time**: Specific time to trigger Evening mode (only used if "Fixed Time" selected)
- **Evening Mode - Sunset Offset**: Minutes before (-) or after (+) sunset (only used if "Sunset" selected)

#### Night Mode Configuration
- **Night Mode Name**: Name for your night mode (default: "Night")
- **Night Mode - Fixed Time**: Specific time to trigger Night mode (always uses fixed time)

#### Additional Settings
- **Skip Time Changes**: Comma-separated list of modes that should not be changed by time triggers (e.g., "Away,Vacation")
- **Set Mode on System Startup**: Automatically set appropriate mode when Home Assistant starts

### Presence-Based Mode Changes

Configure mode changes based on presence with flexible logic:

- **Enable Presence-Based Mode Changes**: Toggle to enable presence detection
- **Device Trackers / Person Entities**: Select person or device_tracker entities for presence detection
- **Away Mode Trigger Logic**: Choose when to trigger Away mode:
  - "When ALL selected people/devices are away" (default - traditional behavior)
  - "When ANY selected person/device leaves" (immediate away mode)
- **Away Mode Name**: Mode to set when away condition is met
- **Return Trigger Logic**: Choose when to trigger return from Away mode:
  - "When ANY selected person/device returns home" (default - immediate return)
  - "When ALL selected people/devices are home" (wait for everyone)
- **Return from Away Behavior**: Choose between time-based mode or specific mode when returning
- **Return Mode**: Specific mode to set when returning (if not using time-based)

### Button-Based Mode Changes

Set up mode control via button events:

- **Enable Button-Based Mode Changes**: Toggle to enable button triggers
- **Button Devices**: Select button devices that generate events
- **Button Events**: Configure specific button events for each mode (e.g., "button_1_single", "button_2_double")

### Switch-Based Mode Changes

Configure mode changes via switch states:

- **Enable Switch-Based Mode Changes**: Toggle to enable switch triggers
- **Switch Devices**: Select switch entities for mode control
- **Day Mode Switch (On)**: Switch that triggers Day mode when turned on
- **Night Mode Switch (Off)**: Switch that triggers Night mode when turned off

## Usage Examples

### Basic Time-Based Setup

1. Create an input_select with options: Day, Evening, Night, Away
2. Enable time-based mode changes
3. Configure Day Mode:
   - Name: "Day"
   - Trigger: "Fixed Time" 
   - Fixed Time: 07:00:00
4. Configure Evening Mode:
   - Name: "Evening"
   - Trigger: "Fixed Time"
   - Fixed Time: 18:00:00
5. Configure Night Mode:
   - Name: "Night"
   - Fixed Time: 22:00:00
6. Set skip modes to "Away" so time changes don't override Away mode

### Sunrise/Sunset Setup

For a more natural lighting schedule:

1. Configure Day Mode:
   - Name: "Day"
   - Trigger: "Sunrise (with optional offset)"
   - Sunrise Offset: 30 (triggers 30 minutes after sunrise)
2. Configure Evening Mode:
   - Name: "Evening" 
   - Trigger: "Sunset (with optional offset)"
   - Sunset Offset: -15 (triggers 15 minutes before sunset)
3. Night Mode still uses fixed time: 22:00:00

### Presence + Time Setup

1. Configure time-based modes as above
2. Enable presence-based changes
3. Select your person entities or device trackers
4. Configure Away logic:
   - Away Mode Trigger Logic: "When ALL selected people/devices are away"
   - Away Mode Name: "Away"
5. Configure Return logic:
   - Return Trigger Logic: "When ANY selected person/device returns home"
   - Return from Away Behavior: "Use time-based mode (recommended)"

### Alternative Presence Scenarios

**Immediate Away Mode** (for security/energy savings):
- Away Mode Trigger Logic: "When ANY selected person/device leaves"
- Useful for immediately turning off lights/HVAC when first person leaves

**Wait for Everyone Home**:
- Return Trigger Logic: "When ALL selected people/devices are home"  
- Useful for family situations where you want to wait until everyone is back

### Button Control

1. Enable button-based changes
2. Select your button devices
3. Configure button events:
   - Day Mode: "button_1_single"
   - Evening Mode: "button_2_single"
   - Night Mode: "button_3_single"
   - Away Mode: "button_1_double"

### Bedroom Switch Example

1. Enable switch-based changes
2. Set "Night Mode Switch (Off)" to your bedroom light
3. When you turn off the bedroom light, it automatically switches to Night mode

## Advanced Configuration

### Custom Mode Names

You can use any mode names in your input_select. The blueprint will use whatever names you configure in the mode fields.

### Multiple Triggers

You can enable multiple trigger types simultaneously. For example:
- Time-based changes during normal operation
- Presence detection for Away mode
- Button override for manual control
- Switch triggers for specific scenarios

### Skip Logic

The "Skip Time Changes" feature prevents certain modes from being automatically changed by time triggers. This is useful for:
- Away mode (shouldn't change to Evening just because it's 6 PM)
- Vacation mode
- Sleep mode
- Any temporary modes you don't want interrupted

## Troubleshooting

### Common Issues

1. **Mode not changing**: 
   - Check that your input_select entity is correctly selected
   - Verify the mode names match exactly (case-sensitive)
   - Check automation traces for errors

2. **Button events not working**:
   - Verify your button device generates the expected events
   - Check Developer Tools → Events to see what events your buttons generate
   - Ensure event names match exactly

3. **Presence not working**:
   - Confirm your person/device_tracker entities are updating correctly
   - Check that all selected presence entities are in "not_home" state for Away mode to trigger

4. **Time changes not working**:
   - Verify times are in 24-hour format (HH:MM:SS)
   - Check that current mode is not in the skip list
   - Ensure "Enable Time-Based Mode Changes" is turned on

### Debugging

1. Go to **Settings** → **Automations & Scenes**
2. Find your Mode Manager automation
3. Click on it and select **Traces** to see execution history
4. Check the automation's state and recent triggers

## Integration with Other Automations

Your mode can be used in other automations as a condition:

```yaml
condition:
  - condition: state
    entity_id: input_select.house_mode
    state: "Evening"
```

Or as a trigger:

```yaml
trigger:
  - platform: state
    entity_id: input_select.house_mode
    to: "Night"
```

## Customization

The blueprint is designed to be flexible. You can:

- Use any mode names you prefer
- Enable only the trigger types you need
- Combine multiple trigger methods
- Customize times and offsets
- Add your own conditions in other automations

## Support

This blueprint replicates the core functionality of Hubitat's Mode Manager. If you encounter issues or need additional features, please check:

1. Home Assistant logs for errors
2. Automation traces for execution details
3. Entity states in Developer Tools

## Version History

- **v1.0**: Initial release with full Hubitat Mode Manager functionality
  - Time-based triggers (fixed time and sunrise/sunset)
  - Presence-based triggers
  - Button event triggers
  - Switch state triggers
  - Skip logic for protected modes
  - Startup mode setting
