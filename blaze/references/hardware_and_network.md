# 📡 Blaze Hardware, Network & Automation Reference

## Device Specifications
- **PC Persona**: `Motobook`
  - OS: Windows 11 Pro 64-bit
  - Shell: PowerShell 7 (`pwsh.exe`)
  - SSH Server Port: `22`
  - User Account: `karan`
  - Public Key: `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPCNjdCpyt8IFlrtDnJNjZq6bWAMg6PUtfX/GYEaL3zF karan@Motobook`

- **Phone Persona**: `Blaze`
  - Device: Lava Blaze 5G
  - Display: IPS High-Contrast Screen
  - OS: Android 14 / Linux 4.19 aarch64
  - Shell: Zsh with Powerlevel10k & MesloLGS NF Bold font
  - SSH Server Port: `8022`
  - User Account: `u0_a46`
  - Public Key: `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIB+dDpYExt6orFFlwv0YaSUVDs5zuLpNL7wTLaR1diuw blaze@termux`

## Network Topology & Discovery
- **Hotspot SSID**: `Lava Blaze 5G 290` (Subnet: `10.242.186.0/24`)
- **Discovery Strategy**:
  - Windows: Asynchronous TCP socket probe across active ARP table neighbors on port 8022.
  - Termux: Dynamic probe of `~/.ssh_last_client` and default gateway (`ip route`).
- **Resilience**: `ServerAliveInterval 3`, `ServerAliveCountMax 2` (detects dropped links in ~6s).
