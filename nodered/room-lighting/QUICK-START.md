# Quick Start Guide

## 🚀 Get Room Lighting Running in 5 Minutes

### 1. Install Dependencies
In Node-RED: **Menu → Manage Palette → Install**
- `@flowfuse/node-red-dashboard`
- `node-red-contrib-home-assistant-websocket`

### 2. Import the Flow
1. **Menu → Import** in Node-RED
2. Copy/paste contents of `room-lighting-complete.json`
3. Click **Import**

### 3. Configure Home Assistant Connection
1. Double-click any Home Assistant node (red triangle)
2. Add your HA server URL and access token
3. Deploy the flow

### 4. Access Dashboard
Go to: `http://your-node-red-ip:1880/ui`

### 5. Create Your First Room
1. Scroll to **Configuration** section
2. Click **New**
3. Enter room name (e.g., "Living Room")
4. Click **Add Device**, enter light entity (e.g., `light.living_room`)
5. Enter motion sensor (e.g., `binary_sensor.living_room_motion`)
6. Click **Save**
7. Select your room from dropdown at top

### 6. Test It!
- Click **Activate** button to test
- Walk in front of motion sensor
- Lights should turn on/off automatically

## 📝 Example Configuration

**Device Entity ID:** `light.living_room_main`
**Motion Sensor:** `binary_sensor.living_room_motion`
**Timeout:** `300` seconds (5 minutes)

## 🔧 Customize
- Add more devices with **Add Device**
- Add more motion sensors
- Adjust timeout values
- Create multiple room configurations

## ❓ Need Help?
- Check Node-RED debug panel for errors
- Verify entity IDs exist in Home Assistant
- Ensure motion sensor reports 'on'/'off' states

That's it! Your Room Lighting system is now running and will automatically control lights based on motion detection, just like Hubitat's Room Lighting app.
