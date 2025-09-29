# Node-RED Room Lighting for Home Assistant

A comprehensive room lighting automation system that replicates the functionality of Hubitat's Room Lighting app. This Node-RED implementation provides a powerful, flexible way to automate lighting based on motion sensors, contact sensors, switches, illuminance levels, and more.

## Features

### Core Functionality
- **Multiple Room Configurations**: Create and manage multiple room lighting setups
- **Device Management**: Support for lights, switches, covers, and buttons
- **Flexible Activation**: Motion, contact, switch, illuminance, time, and manual triggers
- **Smart Turn-Off**: Configurable turn-off conditions with override protection
- **Real-time Configuration**: Web-based UI for easy setup and management

### Device Support
- **Lights**: Full control of brightness, color temperature, RGB colors, and effects
- **Switches**: Simple on/off control
- **Covers**: Position control for blinds, curtains, and shades
- **Buttons**: Trigger actions on button press

### Activation Triggers
- **Motion Sensors**: Activate lights when motion is detected
- **Contact Sensors**: Trigger on door/window open or close
- **Switches**: Manual switch activation
- **Illuminance**: Light level-based activation (below/above threshold)
- **Time-based**: Schedule-based activation
- **Manual**: Dashboard buttons for testing

### Turn-Off Options
- **Motion Timeout**: Turn off after motion inactive for specified time
- **Contact Sensors**: Turn off when doors/windows close
- **Override Protection**: Prevent turn-off after manual adjustments
- **Alternative Methods**: Turn off, dim, or use preset settings
- **Conditional Logic**: Wait for multiple conditions

## Installation

See [install.md](install.md) for detailed installation instructions.

### Quick Start
1. Install required Node-RED packages:
   - `@flowfuse/node-red-dashboard`
   - `node-red-contrib-home-assistant-websocket`
2. Import the flow files into Node-RED
3. Configure Home Assistant connection
4. Access dashboard at `http://your-node-red-ip:1880/ui`

## Usage

### Creating a Room Lighting Configuration

1. **Access Configuration UI**
   - Navigate to the "Room Config" tab in the dashboard
   - Click "New" to create a new configuration

2. **Basic Setup**
   - Enter a descriptive name for your room lighting
   - Optionally select a room for automatic device discovery

3. **Configure Devices**
   - Go to "Device Management" tab
   - Add devices you want to automate
   - Configure activation settings (brightness, color, etc.)
   - Set which devices activate and which turn off

4. **Set Up Triggers**
   - Go to "Triggers" tab
   - Configure activation triggers (motion, contact, etc.)
   - Set up turn-off conditions and timeouts
   - Configure advanced options

5. **Save and Test**
   - Save your configuration
   - Use manual activate/turn-off buttons to test
   - Monitor the system and adjust as needed

### Device Configuration Table

The device table allows you to:
- **Select Devices**: Choose from available Home Assistant entities
- **Set Device Type**: Light, switch, cover, or button
- **Configure Activation**: Set brightness, color temperature, RGB colors
- **Control Participation**: Choose which devices activate/turn off
- **Capture Settings**: Capture current device state
- **Test Devices**: Test individual device settings

### Activation Triggers

#### Motion Sensors
- Add multiple motion sensors
- Configurable timeout for turn-off
- Support for motion inactive delays

#### Contact Sensors
- Door and window sensors
- Configurable trigger state (open/closed)
- Multiple sensors supported

#### Illuminance Sensors
- Light level-based activation
- Configurable threshold and operator
- Multiple sensors for redundancy

#### Switches and Buttons
- Manual activation triggers
- Support for wall switches and button devices
- Integration with existing switch infrastructure

### Advanced Features

#### Override Protection
Prevents automatic turn-off when lights have been manually adjusted, useful for:
- Makeup mirrors requiring specific brightness
- Reading lights adjusted for comfort
- Any scenario where manual adjustment should be preserved

#### Conditional Logic
- Wait for multiple conditions before turn-off
- Prevent activation based on other sensor states
- Time-based restrictions and mode-based operation

#### Alternative Turn-Off Methods
- **Standard Turn-Off**: Simply turn devices off
- **Preset Settings**: Set devices to specific "off" states
- **Dimming**: Gradually dim lights instead of turning off

## Architecture

### Flow Structure
- **Main Engine** (`flows.json`): Core automation logic and device control
- **Configuration UI** (`config-ui.json`): Basic configuration management
- **Device Management** (`device-management.json`): Device setup and testing
- **Trigger Configuration** (`trigger-config.json`): Activation and turn-off setup

### Data Storage
- Configurations stored in Node-RED global context
- Persistent across Node-RED restarts
- JSON-based configuration format

### Home Assistant Integration
- Uses websocket connection for real-time updates
- Service calls for device control
- State monitoring for override detection

## Configuration Examples

### Basic Motion Lighting
```json
{
  "name": "Living Room Lights",
  "devices": [
    {
      "entity_id": "light.living_room_main",
      "type": "light",
      "activate": true,
      "turnOff": true,
      "settings": {
        "brightness": 255,
        "color_temp": 370
      }
    }
  ],
  "activationMeans": {
    "motion": {
      "enabled": true,
      "sensors": ["binary_sensor.living_room_motion"],
      "timeout": 300
    }
  }
}
```

### Multi-Sensor Setup
```json
{
  "name": "Kitchen Automation",
  "activationMeans": {
    "motion": {
      "enabled": true,
      "sensors": ["binary_sensor.kitchen_motion"]
    },
    "illuminance": {
      "enabled": true,
      "sensors": ["sensor.kitchen_illuminance"],
      "threshold": 50,
      "operator": "below"
    }
  },
  "turnOffMeans": {
    "motion": {
      "enabled": true,
      "timeout": 600
    },
    "contact": {
      "enabled": true,
      "sensors": ["binary_sensor.kitchen_door"],
      "state": "closed"
    }
  }
}
```

## Troubleshooting

### Common Issues

**Dashboard Not Loading**
- Check that `@flowfuse/node-red-dashboard` is installed
- Verify Node-RED is running and accessible
- Clear browser cache and reload

**Devices Not Responding**
- Verify Home Assistant connection
- Check entity IDs match your HA setup
- Test individual devices in Home Assistant

**Triggers Not Working**
- Check sensor entity IDs
- Verify sensors are reporting state changes
- Enable debug output to monitor trigger events

**Configuration Not Saving**
- Check Node-RED logs for errors
- Verify global context is working
- Try restarting Node-RED

### Debug Tips

1. **Enable Debug Output**: Add debug nodes to monitor message flow
2. **Check Logs**: Monitor Node-RED logs for error messages
3. **Test Incrementally**: Start with simple configurations
4. **Verify Entities**: Ensure all entity IDs exist in Home Assistant

## Contributing

This project is part of the Home Assistant community blueprints. Contributions are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by Hubitat's Room Lighting app
- Built for the Home Assistant community
- Uses Node-RED for flexible automation logic
- Powered by flowfuse/node-red-dashboard for the UI

## Support

For support and questions:
- Check the troubleshooting section above
- Review the installation guide
- Consult Home Assistant and Node-RED documentation
- Report issues on the project repository
