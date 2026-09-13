---
name: blaze
description: >-
  Bi-directional device bridge, mobile automation runbook, and network protocol specification
  connecting Workstation (PC) and Mobile (Android Termux) over SSH, ADB, and Termux:API.
  Use whenever triggering mobile file transfers, clipboard sync, notifications, TTS audio, camera capture, or /blaze.
---

# 📱 Blaze: Mobile-Workstation Interop & Automation Engine

Use this skill to orchestrate, automate, and diagnose bi-directional workflows between the primary Workstation (PC) and Mobile device (Android Termux).

---

## 🏛️ System Architecture & Connectivity Topology

```
┌────────────────────────────────────────────────────────┐
│               💻 WORKSTATION (PC Node)                 │
│  PowerShell Profile (10 blaze-* Commands) + FZF Picker │
│  OpenSSH Server (Port 22) | Directory: ~/Downloads     │
└──────────────────────────┬─────────────────────────────┘
                           │ Zero-Password Ed25519 Trust
                           │ Dynamic IP Discovery (<200ms)
                           │ Dual-Transport: SSH (8022) + ADB (5555)
                           ▼ Subnet / Wi-Fi Hotspot
┌────────────────────────────────────────────────────────┐
│               📱 MOBILE (Android Termux Node)          │
│  Termux Zsh + OpenSSH (Port 8022)                      │
│  Termux:API + Scrcpy Display/Opus + Android Intents    │
│  Storage: ~/storage/shared/ (/sdcard)                  │
└────────────────────────────────────────────────────────┘
```

---

## 📐 Universal UI & Transport Engineering Standards

All `blaze-*` commands adhere to these 6 architectural invariants:

1. **Inline FZF Fuzzy Picker**: Renders strictly inline beneath the prompt without clearing terminal screen or causing layout artifacts.
2. **Defensive Error Traps & Safe Timeouts**: Network operations wrapped with `run_ssh()` (8s connect timeout, 11s execution timeout) with clean red/yellow diagnostic box cards.
3. **Dual-Transport Foreground Intent Engine**: Bypass Android 10+ background activity launch restrictions via `adb shell am start` with automatic fallback to `termux-open`.
4. **Direct Native Downloads**: Pulled files land directly in native `~/Downloads`.
5. **Standardized Menu Structure**: Every interactive hub includes a `📖 Help & CLI Reference` option positioned before `0. Exit`.
6. **Android Dialog Return Code Protocol**: Map `code: -1` as `BUTTON_POSITIVE` and `code: -2` as `BUTTON_NEGATIVE`.

---

## 🎮 Operational Commands Suite

Scripts live in `./scripts/` (or `~/Void/Blaze/scripts/`) and are exposed via `blaze_profile.ps1`:

| Command | Function | Key Mechanism |
| :--- | :--- | :--- |
| `blaze` | Core Connection & Auto-Discovery | 3-Tier dynamic IP discovery, interactive Termux Zsh shell with disconnect recovery. |
| `blaze-status` | System Telemetry & Health HUD | Real-time battery %, charging status, Wi-Fi SSID, IP address, and memory. |
| `blaze-location` | Geolocation & Coordinates | High-precision GPS coordinates, reverse geocoding to city/address, and map links. |
| `blaze-phone` | Telephony & Communications | Recent call logs, SMS message inbox/search, and interactive SMS sender. |
| `blaze-clip` | Bi-Directional Clipboard Sync | Copy PC clipboard to phone or pull phone clipboard to PC seamlessly. |
| `blaze-notifs` | Push Notifications & Toast HUD | Send interactive system notifications, ring alarms, and trigger vibration alerts. |
| `blaze-wifi` | Network Topology & Wi-Fi Engine | Scan active Wi-Fi networks, report link speed, frequency, RSSI signal strength. |
| `blaze-file` | Bi-Directional File Transfer | Interactive fuzzy file picker to push/pull documents, APKs, screenshots, and media. |
| `blaze-media` | Screen Streaming, Cam & Audio | Scrcpy ultra-low latency screen mirroring, microphone recording, camera photo capture. |
| `blaze-speak` | Text-to-Speech (TTS) Engine | Vocalizes text prompts on phone speaker with configurable pitch, speed, and language. |

---

## 📚 Technical References
- [Hardware & Network Protocol Specifications](./references/hardware_and_network.md)
- [Troubleshooting & Diagnostic Runbook](./references/troubleshooting_runbook.md)
