# Mode Manager Blueprint

A comprehensive Home Assistant blueprint that replicates the functionality of Hubitat's Mode Manager. This blueprint provides automated mode management based on time, presence, button events, and switch states using an `input_select` entity to store the current mode.

## Features

- **Dynamic Mode Detection**: Automatically adapts to any input_select entity with any number of modes
- **Time-Based Mode Changes**: Automatic mode switching based on specific times or sunrise/sunset
- **Presence-Based Mode Changes**: Mode switching based on person/device tracker presence
- **Button-Based Mode Changes**: Mode control via button device events (up to 4 button mappings)
- **Switch-Based Mode Changes**: Mode control via switch state changes (up to 2 switch mappings)
- **Skip Logic**: Prevent selected modes from being overridden by time-based triggers
- **Startup Mode Setting**: Optionally set mode based on time when Home Assistant starts
- **Flexible Configuration**: Works with any mode names and any number of modes in your input_select

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
      - Vacation
      - Party
    initial: Day
    icon: mdi:home-variant
```

**Note**: The blueprint dynamically adapts to whatever modes you define in your input_select. You can have as few as 2 modes or as many as you need. Common examples:
- **Simple**: Day, Night, Away
- **Standard**: Day, Evening, Night, Away  
- **Extended**: Morning, Day, Evening, Night, Away, Vacation, Party, Sleep

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

- **Mode Input Select Entity**: Select your `input_select` entity that will store the current mode. You'll need to manually enter the exact mode names from this entity in the configuration fields below.

### Time-Based Mode Changes

Enable automatic mode changes based on time with clear trigger options:

- **Enable Time-Based Mode Changes**: Toggle to enable/disable all time-based triggers

#### Day Mode Configuration
- **Day Mode**: Enter the exact mode name from your input_select for daytime (e.g., "Day", "Morning")
- **Day Mode Trigger**: Choose how to trigger Day mode:
  - "Fixed Time" - Use only the fixed time
  - "Sunrise (with optional offset)" - Use only sunrise with offset
  - "Earlier of Fixed Time or Sunrise" - Trigger at whichever comes first
  - "Later of Fixed Time or Sunrise" - Trigger at whichever comes last
- **Day Mode - Fixed Time**: Specific time to trigger Day mode
- **Day Mode - Sunrise Offset**: Minutes before (-) or after (+) sunrise
- **Day Mode - Schedule Type**: Choose how to control when Day mode is triggered:
  - "All Days" - Trigger every day
  - "Select Specific Days" - Choose specific days of the week
  - "Use Schedule Helper" - Use a Home Assistant schedule entity
- **Day Mode - Days of Week**: Select specific days (only used if "Select Specific Days" chosen)
- **Day Mode - Schedule Helper**: Select a schedule entity (only used if "Use Schedule Helper" chosen)

#### Evening Mode Configuration  
- **Evening Mode**: Enter the exact mode name from your input_select for evening (e.g., "Evening", "Dusk")
- **Evening Mode Trigger**: Choose how to trigger Evening mode:
  - "Fixed Time" - Use only the fixed time
  - "Sunset (with optional offset)" - Use only sunset with offset
  - "Earlier of Fixed Time or Sunset" - Trigger at whichever comes first
  - "Later of Fixed Time or Sunset" - Trigger at whichever comes last
- **Evening Mode - Fixed Time**: Specific time to trigger Evening mode
- **Evening Mode - Sunset Offset**: Minutes before (-) or after (+) sunset
- **Evening Mode - Schedule Type**: Choose how to control when Evening mode is triggered:
  - "All Days" - Trigger every day
  - "Select Specific Days" - Choose specific days of the week
  - "Use Schedule Helper" - Use a Home Assistant schedule entity
- **Evening Mode - Days of Week**: Select specific days (only used if "Select Specific Days" chosen)
- **Evening Mode - Schedule Helper**: Select a schedule entity (only used if "Use Schedule Helper" chosen)

#### Night Mode Configuration
- **Night Mode**: Enter the exact mode name from your input_select for night (e.g., "Night", "Sleep")
- **Night Mode - Fixed Time**: Specific time to trigger Night mode (always uses fixed time)
- **Night Mode - Schedule Type**: Choose how to control when Night mode is triggered:
  - "All Days" - Trigger every day
  - "Select Specific Days" - Choose specific days of the week
  - "Use Schedule Helper" - Use a Home Assistant schedule entity
- **Night Mode - Days of Week**: Select specific days (only used if "Select Specific Days" chosen)
- **Night Mode - Schedule Helper**: Select a schedule entity (only used if "Use Schedule Helper" chosen)

#### Additional Settings
- **Skip Time Changes for These Modes**: Comma-separated list of modes that should not be changed by time triggers (e.g., "Away,Vacation,Party")
- **Set Mode on System Startup**: Automatically set appropriate mode when Home Assistant starts

### Presence-Based Mode Changes

Configure mode changes based on presence with flexible logic:

- **Enable Presence-Based Mode Changes**: Toggle to enable presence detection
- **Device Trackers / Person Entities**: Select person or device_tracker entities for presence detection
- **Away Mode Trigger Logic**: Choose when to trigger Away mode:
  - "When ALL selected people/devices are away" (default - traditional behavior)
  - "When ANY selected person/device leaves" (immediate away mode)
- **Away Mode**: Enter the exact mode name from your input_select to set when away condition is met (e.g., "Away", "Vacation")
- **Return Trigger Logic**: Choose when to trigger return from Away mode:
  - "When ANY selected person/device returns home" (default - immediate return)
  - "When ALL selected people/devices are home" (wait for everyone)
- **Return from Away Behavior**: Choose between time-based mode or specific mode when returning
- **Return Mode**: Enter the exact mode name to set when returning (if not using time-based, e.g., "Day")

### Guest Mode

Prevent automatic away mode changes when guests are present:

- **Enable Guest Mode**: Toggle to enable guest mode functionality
- **Guest Mode Sensor**: Select a binary sensor, input_boolean, or switch that indicates when guests are present
  - When this sensor is "on", the system will NOT automatically switch to away mode
  - Useful for situations where family members leave but guests remain at home
  - Common sensors: guest mode input_boolean, guest room occupancy sensor, or manual guest switch

### Button-Based Mode Changes

Set up mode control via button events (up to 4 button mappings):

- **Enable Button-Based Mode Changes**: Toggle to enable button triggers
- **Button Devices**: Select button devices that generate events
- **Button Mode 1-4**: Enter the exact mode names from your input_select for each button mapping (leave empty to disable)
- **Button Event 1-4**: Configure specific button events for each mode (e.g., "button_1_single", "button_2_double")

### Switch-Based Mode Changes

Configure mode changes via switch states (up to 2 switch mappings):

- **Enable Switch-Based Mode Changes**: Toggle to enable switch triggers
- **Switch Devices**: Select switch entities for mode control
- **Switch Mode 1-2**: Enter the exact mode names from your input_select for each switch mapping (leave empty to disable)
- **Switch Entity 1-2**: Select specific switch entities for each mapping
- **Switch State 1-2**: Choose "On" or "Off" state that triggers the mode change

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

### Advanced Time Setup with Earlier/Later Logic

For more sophisticated scheduling:

1. **Day Mode - Earlier of 7 AM or Sunrise + 10 minutes**:
   - Name: "Day"
   - Trigger: "Earlier of Fixed Time or Sunrise"
   - Fixed Time: 07:00:00
   - Sunrise Offset: 10
   - Result: Switches to Day mode at 7 AM in winter, but earlier in summer when sunrise + 10 min is before 7 AM

2. **Evening Mode - Later of 6 PM or Sunset**:
   - Name: "Evening"
   - Trigger: "Later of Fixed Time or Sunset"
   - Fixed Time: 18:00:00
   - Sunset Offset: 0
   - Result: Never switches to Evening before 6 PM, but waits for sunset if it's later

### Weekday/Weekend Schedules

Different schedules for different days:

1. **Weekday Schedule**:
   - Day Mode: Days = Monday, Tuesday, Wednesday, Thursday, Friday
   - Fixed Time: 06:30:00 (early for work)

2. **Weekend Schedule**:
   - Day Mode: Days = Saturday, Sunday  
   - Fixed Time: 08:00:00 (sleep in on weekends)

3. **Night Mode**:
   - Sunday-Thursday: 22:00:00 (early bedtime for work nights)
   - Friday-Saturday: 23:30:00 (later bedtime for weekends)

### Using Schedule Helpers (Recommended for Complex Schedules)

Create schedule helpers in Home Assistant for maximum flexibility:

#### Step 1: Create Schedule Helpers

In Home Assistant, go to **Settings** → **Devices & Services** → **Helpers** and create:

```yaml
# Example schedule configurations
schedule.workday_schedule:
  name: "Workday Schedule"
  # Configure: Mon-Fri, all day

schedule.weekend_schedule:
  name: "Weekend Schedule" 
  # Configure: Sat-Sun, all day

schedule.vacation_schedule:
  name: "Vacation Schedule"
  # Configure: Specific vacation dates
```

#### Step 2: Create Multiple Mode Manager Instances

**Workday Mode Manager**:
- Day Mode: Schedule Type = "Use Schedule Helper", Schedule = `schedule.workday_schedule`
- Fixed Time: 06:30:00
- Trigger: "Earlier of Fixed Time or Sunrise"

**Weekend Mode Manager**:
- Day Mode: Schedule Type = "Use Schedule Helper", Schedule = `schedule.weekend_schedule`  
- Fixed Time: 09:00:00
- Trigger: "Later of Fixed Time or Sunrise"

**Vacation Mode Manager**:
- Day Mode: Schedule Type = "Use Schedule Helper", Schedule = `schedule.vacation_schedule`
- Fixed Time: 10:00:00 (sleep in on vacation!)

#### Benefits of Schedule Helpers:
- **Visual calendar interface** for setting dates
- **Holiday integration** with Home Assistant calendar
- **Easy temporary changes** without reconfiguring automations
- **Complex patterns** like "every other Friday" or "first Monday of month"
- **Vacation mode** with specific date ranges

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

### Guest Mode Setup

Perfect for when you have guests staying over:

#### Step 1: Create Guest Mode Helper
In Home Assistant, create an input_boolean:
```yaml
input_boolean:
  guest_mode:
    name: "Guest Mode"
    icon: mdi:account-multiple
```

#### Step 2: Configure Mode Manager
- Enable Guest Mode: ✅ On
- Guest Mode Sensor: `input_boolean.guest_mode`

#### Step 3: Usage Scenarios
**Normal Operation**:
- Family leaves → Mode changes to "Away" ✅
- Family returns → Mode changes back ✅

**With Guests** (guest_mode = on):
- Family leaves → Mode stays "Day/Evening/Night" (no away mode) ✅
- Guests can enjoy normal lighting/climate
- Family returns → Normal operation continues ✅

**Manual Control**:
- Turn on guest mode before leaving guests alone
- Turn off guest mode when guests leave
- Can be automated with guest room occupancy sensors

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
