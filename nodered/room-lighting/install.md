# Complete Hubitat Room Lighting Installation Guide

## Prerequisites

1. **Node-RED** installed and running (version 3.0.0 or higher)
2. **Home Assistant** with Node-RED addon or standalone Node-RED instance
3. **Required Node-RED packages:**
   - `@flowfuse/node-red-dashboard` (for the configuration UI)
   - `node-red-contrib-home-assistant-websocket` (for Home Assistant integration)
   - `node-red-contrib-cron-plus` (for time-based triggers) - optional

## Installation Steps

### Step 1: Install Required Packages

In your Node-RED instance, go to **Menu → Manage Palette → Install** and install:

```
@flowfuse/node-red-dashboard
node-red-contrib-home-assistant-websocket
node-red-contrib-cron-plus
```

Or via command line:
```bash
npm install @flowfuse/node-red-dashboard node-red-contrib-home-assistant-websocket node-red-contrib-cron-plus
```

### Step 2: Import the Complete Hubitat Room Lighting Flow

1. In Node-RED, go to **Menu → Import**
2. Copy the contents of `hubitat-room-lighting-complete.json`
3. Paste into the import dialog and click **Import**
4. This creates a complete "Hubitat Room Lighting" tab with all features

### Step 3: Configure Home Assistant Connection

1. In Node-RED, find any Home Assistant node (they will show as disconnected)
2. Double-click to edit and configure your Home Assistant server:
   - **Base URL**: Your Home Assistant URL (e.g., `http://homeassistant.local:8123`)
   - **Access Token**: Generate a long-lived access token in Home Assistant
     - Go to Profile → Security → Long-lived access tokens → Create token

### Step 4: Access the Complete Configuration Dashboard

1. The dashboard will be available at: `http://your-node-red-ip:1880/ui`
2. You should see a **Room Lighting** tab with the complete Hubitat-style interface
3. The system automatically creates storage files in your Node-RED directory

### Step 5: Configure Your First Room

1. **Create New Room**:
   - Click **New Room** button
   - Enter room name (e.g., "Living Room")
   - Check **Room Enabled**

2. **Configure Devices** (Devices tab):
   - Click **Add Device**
   - Enter entity ID (e.g., `light.living_room_main`)
   - Select device type (Light, Switch, Cover, Button, Scene)
   - Set brightness, color temp, RGB color for lights
   - Check **Activate** and **Turn Off** as needed

3. **Setup Activation Triggers** (Activation tab):
   - **Motion Sensors**: Check enable, add sensor entities, set timeout
   - **Contact Sensors**: Add door/window sensors with open/close triggers
   - **Switches**: Add wall switches for manual activation
   - **Illuminance**: Add light sensors with threshold values
   - **Time**: Configure time-based schedules
   - **Modes**: Set Home Assistant mode triggers

4. **Configure Turn Off** (Turn Off tab):
   - Enable motion timeout, contact sensors, switches, or time schedules

5. **Advanced Options** (Options tab):
   - Set fade times, activation delays
   - Choose turn-off method (standard, preset, dim, scene)
   - Enable override protection
   - Configure scene usage

6. **Set Conditions** (Conditions tab):
   - Add mode restrictions
   - Set time-based restrictions
   - Configure illuminance conditions

7. **Save Configuration**:
   - Click **Save** to persist all settings
   - Configuration is immediately active!

## Troubleshooting

### Dashboard Not Loading
- Ensure `@flowfuse/node-red-dashboard` is properly installed
- Check Node-RED logs for errors
- Restart Node-RED after installing packages

### Home Assistant Connection Issues
- Verify your Home Assistant URL and access token
- Check that Home Assistant is accessible from Node-RED
- Ensure the websocket connection is working

### Devices Not Showing
- Verify Home Assistant connection is working
- Check that entities exist in Home Assistant
- Look for errors in Node-RED debug panel

### Flow Import Errors
- Import flows one at a time
- Check for missing dependencies
- Ensure Node-RED version compatibility

## Configuration Tips

1. **Start Simple**: Begin with just motion sensors and basic lights
2. **Test Incrementally**: Add one trigger type at a time
3. **Use Debug Nodes**: Enable debug output to troubleshoot issues
4. **Check Entity IDs**: Ensure all entity IDs match your Home Assistant setup

## Support

For issues and questions:
1. Check the Node-RED logs for error messages
2. Verify all prerequisites are met
3. Test with simple configurations first
4. Consult the Home Assistant and Node-RED documentation
