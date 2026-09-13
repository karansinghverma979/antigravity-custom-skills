# 📡 Mobile-PC Bridge Hardware & Network Protocol Reference

## Architecture Specifications

### 1. Workstation Node (PC)
- **OS**: Windows 11 / Linux / macOS
- **Shell**: PowerShell 7 (`pwsh.exe`) / Zsh / Bash
- **SSH Daemon**: OpenSSH Server (Port 22)
- **Authentication**: Public-Key Cryptography (Ed25519)
- **Downloads Directory**: `~/Downloads`

### 2. Mobile Node (Android Termux)
- **OS**: Android 12+ / Linux aarch64
- **Environment**: Termux + Termux:API + OpenSSH
- **SSH Daemon**: Port `8022` (`sshd`)
- **Background Persistence**: `termux-wake-lock`
- **Storage Mapping**:
  - Shared Storage: `~/storage/shared/` (`/sdcard`)
  - Downloads: `~/storage/downloads/` (`/sdcard/Download`)

## Dynamic Network Discovery & Resilience
- **Discovery Routine**:
  1. Gateway IP resolution via local routing table (`ip route` / `arp -a`).
  2. Subnet socket sweep on SSH port (`8022`).
  3. Cached IP verification from previous successful handshake.
- **Heartbeat & Keepalive**:
  - `ServerAliveInterval 3`
  - `ServerAliveCountMax 2` (detects dropped connection in ~6s without hanging terminal).
