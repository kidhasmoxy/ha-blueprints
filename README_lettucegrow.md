# LettuceGrow Nook – Home Assistant Package

Automated day/night cycle management for a LettuceGrow Nook hydroponic system. Everything is self-contained in a single package file — no blueprint required.

Features: configurable light/pump schedules, override modes (snooze, cleaning, spraying, test pump), restart resilience, safety shutoff, and a full dashboard with energy tracking.

---

## Components

| File | Purpose |
|------|---------|
| `lettucegrow_package.yaml` | **Package** – all automations, helpers, scripts, timers, and sensors |
| `lettucegrow_dashboard.yaml` | **Dashboard** – status, actions, energy, schedule settings |
| `lettucegrow_nook.yaml` | *(Deprecated)* Old blueprint — kept as reference only |

---

## Install Instructions

### 1. Install the Package

1. Copy `lettucegrow_package.yaml` into your Home Assistant `packages/` directory  
   (typically `/config/packages/lettucegrow_package.yaml`).

2. Ensure your `configuration.yaml` includes packages:
   ```yaml
   homeassistant:
     packages: !include_dir_named packages/
   ```

3. **Restart Home Assistant** (a full restart is required for new helpers and automations).

4. **Verify helpers were created:**
   - Go to **Settings → Devices & Services → Helpers**
   - Confirm you see: `LettuceGrow Light Entity`, `LettuceGrow Pump Entity`, `LettuceGrow Mode`, `LettuceGrow Day Start`, `LettuceGrow Day End`, etc.

5. **Confirm entity IDs** in the input_text helpers (Settings → Helpers → edit each):
   - `input_text.lettucegrow_light_entity` → your light switch entity ID
   - `input_text.lettucegrow_pump_entity` → your pump switch entity ID

   These auto-populate from the `initial` values in the package, but verify after first boot.

### 2. Install the Dashboard

1. Go to **Settings → Dashboards → Add Dashboard**
2. Name it "LettuceGrow" and select **"Manual"** mode
3. Open the dashboard, click the three dots menu → **Raw Configuration Editor**
4. Paste the entire contents of `lettucegrow_dashboard.yaml`
5. **Update the entity IDs** in the `anchors:` block at the top to match your devices
6. Save

> **Note:** HA's visual dashboard editor will resolve YAML anchors to plain entity IDs when you save from the UI. If you make UI edits, re-apply anchors in the Raw Configuration Editor afterward.

---

## How It Works

### Architecture

The package uses an **event-driven** design with no loops or delays:

1. **Light Controller** — triggers at day/night start times, HA restart, mode changes, and schedule changes. Evaluates whether it's daytime and turns the light on or off accordingly.
2. **Pump Cycle Start** — triggers every minute via `time_pattern`, checks if enough time has elapsed since the last run (start-to-start interval), then turns the pump on and starts a timer.
3. **Pump Cycle End** — fires when the pump run timer finishes and turns the pump off.
4. **Pump Safety** — catches the pump left on too long (duration + 5 min buffer) and forces it off.
5. **Override Expiry** — fires when the override timer finishes and resets mode to normal.

### Normal Operation

| Cycle | Light | Pump |
|-------|-------|------|
| **Day** (default 6:00–22:00) | ON continuously | 10 min ON every 60 min |
| **Night** (default 22:00–6:00) | OFF | 10 min ON every 180 min |

All timing is configurable from the dashboard (Settings tab).

### Override Modes

| Mode | Triggered by | Behavior |
|------|-------------|----------|
| **Test Pump** | Dashboard / script | Pump runs for configured duration (1–15 min), then returns to normal |
| **Snooze** | Dashboard / script | Light OFF, pump OFF for configured duration (1–180 min) |
| **Cleaning** | Dashboard / script | Pump runs 2 hours continuously, then returns to normal |
| **Spraying** | Dashboard / script | Lights OFF for configured hours (pump keeps cycling), then returns to normal |

All overrides set the mode and start a timer. When the timer expires, the system automatically returns to normal operation. You can cancel any override early from the dashboard.

### Resilience

The system self-corrects on:
- **Home Assistant restart** — light controller and pump scheduler both fire on HA start
- **Timer restore** — pump run and override timers have `restore: true`, surviving restarts
- **Manual switch changes** — safety automation catches unexpected pump-on states; light controller re-evaluates on mode/schedule changes
- **Schedule changes** — light controller triggers immediately when day start/end times are modified

---

## Entity Reference

### Device Entities (configure in dashboard anchors + input_text helpers)

| Purpose | Default Entity ID |
|---------|-------------------|
| Grow light switch | `switch.hydroponic_plug_switch` |
| Water pump switch | `switch.hydroponic_plug_switch_2` |
| Light power (W) | `sensor.hydroponic_plug_power` |
| Pump power (W) | `sensor.hydroponic_plug_power_2` |
| Light energy (kWh) | `sensor.hydroponic_plug_summation_delivered` |
| Pump energy (kWh) | `sensor.hydroponic_plug_summation_delivered_2` |

### Input Helpers

| Helper | Type | Purpose |
|--------|------|---------|
| `input_text.lettucegrow_light_entity` | text | Light switch entity ID |
| `input_text.lettucegrow_pump_entity` | text | Pump switch entity ID |
| `input_select.lettucegrow_mode` | select | Operating mode (normal/snooze/cleaning/spraying) |
| `input_datetime.lettucegrow_day_start` | time | Day cycle start (default 06:00) |
| `input_datetime.lettucegrow_day_end` | time | Night cycle start (default 22:00) |
| `input_datetime.lettucegrow_last_pump_run` | datetime | Timestamp of last pump start |
| `input_number.lettucegrow_pump_duration` | number | Pump run time per cycle (default 10 min) |
| `input_number.lettucegrow_day_pump_interval` | number | Minutes between pump runs during day (default 60) |
| `input_number.lettucegrow_night_pump_interval` | number | Minutes between pump runs at night (default 180) |
| `input_number.lettucegrow_test_pump_minutes` | number | Test pump duration (default 5 min) |
| `input_number.lettucegrow_snooze_minutes` | number | Snooze duration (default 30 min) |
| `input_number.lettucegrow_spraying_hours` | number | Spraying lights-off duration (default 6 hrs) |

### Timers

| Timer | Purpose |
|-------|---------|
| `timer.lettucegrow_pump_run` | Pump on-duration countdown |
| `timer.lettucegrow_override` | Override mode expiry countdown |

### Template Sensors

| Sensor | Purpose |
|--------|---------|
| `binary_sensor.lettucegrow_is_daytime` | Whether current time is within day start/end |
| `sensor.lettucegrow_next_pump_run` | Timestamp of next scheduled pump run |
| `sensor.lettucegrow_pump_status` | Current pump state description |
| `sensor.lettucegrow_current_cycle` | Whether system is in Day or Night cycle |

### Automations

| Automation | Purpose |
|------------|---------|
| `automation.lettucegrow_light_controller` | Manage light based on schedule and mode |
| `automation.lettucegrow_pump_cycle_start` | Start pump when interval has elapsed |
| `automation.lettucegrow_pump_cycle_end` | Turn pump off when run timer finishes |
| `automation.lettucegrow_pump_safety_shutoff` | Force pump off if on too long |
| `automation.lettucegrow_override_expiry` | Return to normal when override timer ends |

### Scripts

| Script | Action |
|--------|--------|
| `script.lettucegrow_test_pump` | Run pump for configured minutes |
| `script.lettucegrow_snooze` | Pause system for configured minutes |
| `script.lettucegrow_cleaning_cycle` | 2-hour continuous pump run |
| `script.lettucegrow_spraying_cycle` | Lights off for configured hours (pump keeps cycling) |
| `script.lettucegrow_cancel_override` | Cancel any active override immediately |
