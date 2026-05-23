# LettuceGrow Nook – Home Assistant Blueprint & Package

Automated day/night cycle management for a LettuceGrow Nook hydroponic system with override actions (test pump, snooze, cleaning, spraying) and a full dashboard.

---

## Components

| File | Purpose |
|------|---------|
| `lettucegrow_nook.yaml` | Blueprint – core automation for day/night light & pump cycling |
| `lettucegrow_package.yaml` | Package – helpers, scripts, and override expiry automation |
| `lettucegrow_dashboard.yaml` | Dashboard – status, energy, actions, schedule adjustment |

---

## Install Instructions

### 1. Import the Blueprint

In Home Assistant, go to **Settings → Automations & Scenes → Blueprints → Import Blueprint** and paste:

```
https://github.com/kidhasmoxy/ha-blueprints/blob/main/lettucegrow_nook.yaml
```

### 2. Install the Companion Package

1. Copy `lettucegrow_package.yaml` into your Home Assistant `packages/` directory.  
   (Typically at `/config/packages/lettucegrow_package.yaml`)

2. Ensure your `configuration.yaml` includes packages:
   ```yaml
   homeassistant:
     packages: !include_dir_named packages/
   ```

3. Restart Home Assistant (or reload YAML if only input helpers changed).

4. **Verify helpers were created:**
   - Go to **Settings → Devices & Services → Helpers**
   - Confirm you see: `LettuceGrow Light Entity`, `LettuceGrow Pump Entity`, `LettuceGrow Mode`, `LettuceGrow Day Start`, `LettuceGrow Day End`, etc.

5. **Confirm entity IDs** in `input_text` helpers (Settings → Helpers → edit each):
   - `input_text.lettucegrow_light_entity` → `switch.hydroponic_plug_switch`
   - `input_text.lettucegrow_pump_entity` → `switch.hydroponic_plug_switch_2`

   These should auto-populate from the `initial` values, but verify after first boot.

### 3. Create the Automation from the Blueprint

1. Go to **Settings → Automations & Scenes → Create Automation → Use Blueprint**
2. Select **"LettuceGrow Nook – Day/Night Light & Pump Controller"**
3. Configure:
   - **Day cycle start time helper:** `input_datetime.lettucegrow_day_start`
   - **Day cycle end time helper:** `input_datetime.lettucegrow_day_end`
   - **Grow light switch:** `switch.hydroponic_plug_switch`
   - **Water pump switch:** `switch.hydroponic_plug_switch_2`
   - **Override mode helper:** `input_select.lettucegrow_mode`
   - Pump timing: leave defaults (10 min run, 60 min day interval, 180 min night interval) or adjust
4. Save the automation

### 4. Install the Dashboard

1. Go to **Settings → Dashboards → Add Dashboard**
2. Name it "LettuceGrow" and select **"Manual"** mode
3. Open the dashboard, click the three dots menu → **Raw Configuration Editor**
4. Paste the entire contents of `lettucegrow_dashboard.yaml`
5. Save

### 5. (Optional) Configure Energy Dashboard

If you want the energy section to work with HA's built-in Energy dashboard:

1. Go to **Settings → Dashboards → Energy**
2. Add `sensor.hydroponic_plug_summation_delivered` and `sensor.hydroponic_plug_summation_delivered_2` as individual device consumption sensors

---

## How It Works

### Normal Operation

| Cycle | Light | Pump |
|-------|-------|------|
| **Day** (default 6:00–22:00) | ON continuously | 10 min ON, 50 min OFF, repeat |
| **Night** (default 22:00–6:00) | OFF | 10 min ON, 170 min OFF, repeat |

### Override Modes

| Mode | Triggered by | Behavior |
|------|-------------|----------|
| **Snooze** | Dashboard button | Light OFF, pump OFF for set duration (1–180 min) |
| **Test Pump** | Dashboard button | Pump runs for set duration (1–15 min), then returns to normal |
| **Cleaning** | Dashboard button | Pump runs 2 hours continuously, then returns to normal |
| **Spraying** | Dashboard button | Lights OFF for 6 hours, then returns to normal |

All overrides pause the main automation. When the override timer expires, the system automatically returns to normal operation.

### Resilience

The automation self-corrects on:
- Home Assistant restart
- Automation reload
- Every 5 minutes (periodic check)
- Schedule changes from dashboard
- Override mode returning to "normal"

---

## Entity Reference

| Purpose | Entity ID |
|---------|-----------|
| Grow light switch | `switch.hydroponic_plug_switch` |
| Water pump switch | `switch.hydroponic_plug_switch_2` |
| Light power (W) | `sensor.hydroponic_plug_power` |
| Pump power (W) | `sensor.hydroponic_plug_power_2` |
| Light energy (kWh) | `sensor.hydroponic_plug_summation_delivered` |
| Pump energy (kWh) | `sensor.hydroponic_plug_summation_delivered_2` |

### Helpers Created by Package

| Helper | Type | Purpose |
|--------|------|---------|
| `input_text.lettucegrow_light_entity` | text | Light switch entity ID |
| `input_text.lettucegrow_pump_entity` | text | Pump switch entity ID |
| `input_select.lettucegrow_mode` | select | Current operating mode |
| `input_datetime.lettucegrow_day_start` | time | Day cycle start time |
| `input_datetime.lettucegrow_day_end` | time | Day cycle end time |
| `input_number.lettucegrow_test_pump_minutes` | number | Test pump duration |
| `input_number.lettucegrow_snooze_minutes` | number | Snooze duration |
| `timer.lettucegrow_override` | timer | Override countdown |

### Scripts Created by Package

| Script | Action |
|--------|--------|
| `script.lettucegrow_test_pump` | Run pump for configured minutes |
| `script.lettucegrow_snooze` | Pause system for configured minutes |
| `script.lettucegrow_cleaning_cycle` | 2-hour continuous pump run |
| `script.lettucegrow_spraying_cycle` | 6-hour lights-off period |
| `script.lettucegrow_cancel_override` | Cancel any active override immediately |
