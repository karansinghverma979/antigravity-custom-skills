# 🔧 Blaze Troubleshooting & Diagnostics Runbook

## Diagnostic Decision Tree

### Issue 1: `motobook` from Blaze says `Connection Refused` or `Port 22 Blocked`
1. **Diagnosis**: Windows OpenSSH firewall rule or service is inactive.
2. **Resolution on Motobook**:
   - Run `setup-ssh` in PowerShell.
   - It will elevate in Windows Terminal and enforce `-Profile Any` on the firewall rule `OpenSSH-Server-In-TCP`.

### Issue 2: `blaze` from Motobook says `Could not detect Blaze on port 8022`
1. **Diagnosis**: Termux SSH daemon is not running on the phone.
2. **Resolution on Blaze**:
   - Open Termux on Blaze. The startup telemetry will auto-launch `sshd`.
   - Or manually type `sshd`.

### Issue 3: Permission Denied (Publickey)
1. **Diagnosis**: Administrator ACL mismatch on Windows.
2. **Resolution**:
   - `administrators_authorized_keys` must have strict ACLs.
   - Run: `icacls.exe C:\ProgramData\ssh\administrators_authorized_keys /inheritance:r /grant "SYSTEM:(F)" /grant "BUILTIN\Administrators:(F)"`

### Issue 4: Windows Terminal Elevation Error `0x80070002`
1. **Diagnosis**: Raw string argument splitting by `wt.exe`.
2. **Resolution**:
   - Always encode script to Base64 and invoke with `-EncodedCommand`.
