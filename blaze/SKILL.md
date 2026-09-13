---
name: blaze
description: Authoritative command center, network protocol specification, and automation runbook for the bi-directional ecosystem between Motobook (Windows 11) and Blaze (Lava Blaze 5G / Android Termux).
trigger: /blaze
---

# 📱 Blaze Ecosystem Master Skill & Automation Architecture

Use this skill whenever Karan invokes `/blaze` or requests any action, query, automation, file transfer, screen streaming, audio synthesis, camera capture, telephony, or diagnostic task involving **Blaze** (Lava Blaze 5G / Android 14 / Termux) and **Motobook** (Windows 11 PC).

> **Single Source of Truth**: This skill is the authoritative operational governor, UI/transport specification, and automation engine for the **Motobook ⇄ Blaze Ecosystem** located in [`~/Void/Blaze/`](file:///C:/Users/karan/Void/Blaze/).

---

## 🏛️ System Architecture & Connectivity Topology

```
┌────────────────────────────────────────────────────────┐
│             💻 MOTOBOOK (Windows 11 Node)              │
│  PowerShell Profile (10 blaze-* Commands) + Scoop CLI  │
│  OpenSSH Server (Port 22) | User: $USER                │
│  Direct Downloads: ~/Downloads/                        │
└──────────────────────────┬─────────────────────────────┘
                           │ Zero-Password Ed25519 Trust
                           │ Dynamic IP Discovery (<200ms)
                           │ Dual-Transport: SSH (8022) + ADB (5555)
                           ▼ Hotspot / Local Subnet (e.g., 10.154.149.x / 10.242.186.x)
┌────────────────────────────────────────────────────────┐
│              📱 BLAZE (Lava Blaze 5G Node)             │
│  Termux Zsh + OpenSSH (Port 8022) | User: u0_a46       │
│  Termux:API + Scrcpy Display/Opus + Android Intents    │
│  Storage Root: /sdcard (~/storage/shared/)             │
└────────────────────────────────────────────────────────┘
```

### 📂 Device Profiles & Network Topology
- **Motobook (PC)**:
  - OS: Windows 11 Pro | User: `karan`
  - OpenSSH Server: Port `22` (Service: `sshd`)
  - SSH Key: `~/.ssh/id_ed25519`
  - Public Key: `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPCNjdCpyt8IFlrtDnJNjZq6bWAMg6PUtfX/GYEaL3zF karan@Motobook`
- **Blaze (Phone)**:
  - Hardware: Lava Blaze 5G (Android 14) | User: `u0_a46` | MAC: `F6-DC-F9-03-FA-07`
  - OpenSSH Server: Port `8022` (`sshd` running in Termux)
  - Public Key: `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIB+dDpYExt6orFFlwv0YaSUVDs5zuLpNL7wTLaR1diuw blaze@termux`
  - Background Immunity: `termux-wake-lock` held automatically by default on boot
  - Termux Storage Root: `~/storage/shared/` (`/sdcard`)
  - Termux Downloads: `~/storage/downloads/` (`/sdcard/Download`)

---

## 📐 Universal UI & Transport Engineering Standards

All `blaze-*` commands must strictly adhere to these 6 architectural invariants:

1. **Inline FZF Fuzzy Picker Architecture**:
   - MUST execute as `subprocess.Popen(..., stdin=PIPE, stdout=PIPE, stderr=None, text=True, encoding="utf-8")`.
   - Arguments: `fzf --prompt="..." --height=40% --reverse --cycle`.
   - Renders strictly inline beneath the prompt without clearing terminal screen or causing layout artifacts.
2. **Defensive Error Traps & Safe Timeouts**:
   - Network operations wrapped with `run_ssh()` (8s connect timeout, 11s execution timeout).
   - Display standardized red/yellow diagnostic box card if Blaze is unreachable.
   - Global signal traps: catch `(KeyboardInterrupt, EOFError)` and wrap prompts in `safe_pause()` — **zero unhandled Python tracebacks**.
3. **Dual-Transport Foreground Intent Engine**:
   - To bypass Android 10+ background activity launch restrictions over SSH, file/URL launches execute via `adb shell am start -a android.intent.action.VIEW -d "<URI>"` with automatic fallback to `termux-open`.
4. **Direct Native Downloads**:
   - All pulled files from phone land directly in native Windows `~/Downloads`.
   - Legacy `Z:\` Rclone mounts and `~/Blaze/` directories are permanently deprecated and removed.
5. **Standardized Menu Structure**:
   - Every interactive hub includes a `📖 Help & CLI Reference` option positioned right before `0. Exit`.
6. **Android Dialog Return Code Protocol**:
   - For `termux-dialog`, map `code: -1` as `BUTTON_POSITIVE` (User clicked OK/Submit/Yes) and `code: -2` as `BUTTON_NEGATIVE` (Cancel/No).

---

## 🎮 Complete 10 Operational Commands Suite

All scripts live in [`~/Void/Blaze/scripts/`](file:///C:/Users/karan/Void/Blaze/scripts/) and are exposed via [`blaze_profile.ps1`](file:///C:/Users/karan/Void/Blaze/blaze_profile.ps1).

### 1. `blaze` (Core Connection & Auto-Discovery)
- **Command**: `blaze` or `blaze "<command>"`
- **File**: [`blaze_profile.ps1`](file:///C:/Users/karan/Void/Blaze/blaze_profile.ps1)
- **Function**: 3-Tier dynamic IP discovery (Gateway $\to$ MAC `F6-DC-F9-03-FA-07` $\to$ Cached IP), dynamic `~/.ssh/config` injection, interactive Termux Zsh shell with disconnect recovery.

### 2. `blaze-status` (System Telemetry & Health HUD)
- **Command**: `blaze-status` (or `blaze-status --json`)
- **File**: [`scripts/blaze_status.py`](file:///C:/Users/karan/Void/Blaze/scripts/blaze_status.py)
- **Function**: Sub-second bundled SSH query rendering battery %, temperature, charging status, Wi-Fi SSID/IP/frequency, storage usage, and uptime.

### 3. `blaze-location` (GPS & Reverse Geolocation Radar)
- **Command**: `blaze-location` (or `blaze-location --raw`, `--map`)
- **File**: [`scripts/blaze_location.py`](file:///C:/Users/karan/Void/Blaze/scripts/blaze_location.py)
- **Function**: Multi-provider location acquisition (`gps` $\to$ `network` $\to$ `passive`), OpenStreetMap reverse geocoding to human-readable address, Google Maps browser launcher.

### 4. `blaze-phone` (Telephony, SMS & Contacts Hub)
- **Command**: `blaze-phone` (or `blaze-phone call <num>`, `blaze-phone sms <num> <msg>`)
- **File**: [`scripts/blaze_phone.py`](file:///C:/Users/karan/Void/Blaze/scripts/blaze_phone.py)
- **Function**: Earpiece & Speakerphone call initiator, SMS conversation inbox (newest-first with inline search), Contact phonebook picker.

### 5. `blaze-clip` (Bidirectional Clipboard Sync)
- **Command**: `blaze-clip` (or `blaze-clip --push`, `--pull`, `--watch`)
- **File**: [`scripts/blaze_clip.py`](file:///C:/Users/karan/Void/Blaze/scripts/blaze_clip.py)
- **Function**: Termux API v2 protocol synchronization, side-by-side diff preview between Windows and Android clipboard, continuous sync daemon.

### 6. `blaze-notifs` (Notification Studio & Toast Engine)
- **Command**: `blaze-notifs` (or `blaze-notifs toast "<msg>"`, `blaze-notifs dialog`)
- **File**: [`scripts/blaze_notifs.py`](file:///C:/Users/karan/Void/Blaze/scripts/blaze_notifs.py)
- **Function**: Screen toasts (centered gravity, custom hex colors), Mobile Dialog Studio (Text, PIN password, multiline, numbers, confirm, radio, checkbox, bottom sheet, speech-to-text), Tag/ID prioritized notification dismissal, 1-click OTP extraction.

### 7. `blaze-wifi` (Wireless ADB & Scrcpy Control Center)
- **Command**: `blaze-wifi` (or `blaze-wifi --adb`, `blaze-wifi --scrcpy <preset>`)
- **File**: [`scripts/blaze_wifi.py`](file:///C:/Users/karan/Void/Blaze/scripts/blaze_wifi.py)
- **Function**: Hotspot AP vs Wi-Fi Client radar detection, 1-Click USB $\to$ Wireless switch wizard (`adb tcpip 5555`), Scrcpy presets (Stealth 60fps, Live, Audio-only, HD Webcam, Recording), extended 15s ADB timeouts with zombie process auto-recovery.

### 8. `blaze-file` (Remote File Explorer & Transfer Hub)
- **Command**: `blaze-file` (or `blaze-file push <file>`, `blaze-file pull <remote_path>`)
- **File**: [`scripts/blaze_file.py`](file:///C:/Users/karan/Void/Blaze/scripts/blaze_file.py)
- **Function**: Inline FZF remote storage explorer (`/sdcard/Download`, `Documents`, `DCIM`, `Motobook`, `Music`), local file drop wizard with MediaStore auto-indexing, direct pull to `~/Downloads/`, dual-transport foreground intents (`am start` + `termux-open`).

### 9. `blaze-media` (Hierarchical Audio Browser & Sound Engine)
- **Command**: `blaze-media` (or `blaze-media play <path>`, `blaze-media volume <0-15>`)
- **File**: [`scripts/blaze_media.py`](file:///C:/Users/karan/Void/Blaze/scripts/blaze_media.py)
- **Function**: Inline FZF audio explorer (`/sdcard/Music`, `Download`, `Motobook`), Scrcpy Opus audio streaming to PC speakers, playback radar, 6-channel volume master console, TTS & haptics.

### 10. `blaze-speak` (Studio HD Voice Synthesis & TTS Center)
- **Command**: `blaze-speak` (or `blaze-speak "<text>" -v jarvis`, `blaze-speak --clip`, `blaze-speak --alert`)
- **File**: [`scripts/blaze_speak.py`](file:///C:/Users/karan/Void/Blaze/scripts/blaze_speak.py)
- **Function**: 20 Studio HD Neural Edge-TTS + Google Assist voice personas, persistent default voice stored in `~/.config/blaze_default_voice.txt`, single-shot emergency siren, live spoken briefings, and interactive Voice Chat REPL.

---

## 🔧 Self-Learning & Troubleshooting Runbook

### 1. `blaze` SSH Unreachable on Port 8022
- **Symptoms**: `Connection timed out` or `Connection refused`.
- **Diagnostic Flow**:
  1. Check if phone is connected to the same Wi-Fi / Hotspot.
  2. Verify Termux is awake (`termux-wake-lock`).
  3. Ensure SSH daemon is active: run `sshd` inside Termux on Blaze.
  4. Test raw socket probe from Motobook:
     ```powershell
     Test-NetConnection -ComputerName 10.154.149.220 -Port 8022
     ```

### 2. ADB Wireless Connection Dropped / Zombie ADB
- **Symptoms**: `adb devices` shows `offline` or hangs >10 seconds.
- **Resolution**:
  1. Run automatic recovery:
     ```powershell
     taskkill /F /IM adb.exe
     adb start-server
     adb connect <phone-ip>:5555
     ```
  2. If Wi-Fi ADB lost port 5555, run the 1-Click USB Wizard in `blaze-wifi` (`adb tcpip 5555`).

### 3. File / URL Opening Fails Over SSH
- **Symptoms**: `termux-open` displays toast but nothing opens on phone screen.
- **Root Cause**: Android 10+ restricts background SSH processes from launching foreground activities without Termux overlay permissions.
- **Resolution**:
  - Always execute via ADB shell intent dispatcher:
    ```bash
    adb shell am start -a android.intent.action.VIEW -d "<URI_OR_PATH>"
    ```

### 4. Dialog Return Code `-1` Confusion
- **Root Cause**: `termux-dialog` uses Android DialogInterface constants where `-1` represents `BUTTON_POSITIVE` (User clicked OK/Submit).
- **Rule**: Never treat return code `-1` as an error.

---

## 🥊 Socratic `/grill-me` Initiative for Mobile Architecture

When designing new mobile automations, scripts, or workflow expansions for Blaze, spar with Karan using this structured checklist:

1. **Transport Selection**:
   - *Should this operation run via fast SSH (`port 8022`), ADB Shell (`port 5555`), or Direct Termux API?*
2. **Foreground vs Background Execution**:
   - *Does this task require immediate user interaction on the physical screen (needs ADB intent) or silent daemon execution?*
3. **Data Destination & Cleanup**:
   - *Are incoming files landing directly in `~/Downloads`? Is temporary storage in `/data/data/com.termux/files/usr/tmp/` cleaned up immediately?*
4. **Power & Wake Lock Strategy**:
   - *Does this operation require sustained network transfers during screen-off? (Ensure `termux-wake-lock` is engaged).*
