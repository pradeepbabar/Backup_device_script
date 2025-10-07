#!/usr/bin/env python3
"""
Backup Cisco running‑config over SSH.

Prerequisites:
    pip install netmiko
"""
from datetime import datetime
import os
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException

# ---- device inventory -------------------------------------------------------
DEVICE = {
    "device_type": "cisco_ios",     # adjust for NX‑OS: "cisco_nxos"
    "host": "192.0.2.10",
    "username": "admin",
    "password": "yourPassword",
    "secret":  "enablePassword",    # omit if not using 'enable'
    "fast_cli": True,               # optional speed‑up
}

# ---- main logic -------------------------------------------------------------
def backup_config(device: dict) -> None:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"{device['host']}_running_cfg_{timestamp}.txt"
    backup_dir = "backups"
    os.makedirs(backup_dir, exist_ok=True)

    try:
        with ConnectHandler(**device) as conn:
            if device.get("secret"):
                conn.enable()
            running_cfg = conn.send_command("show running-config", delay_factor=2)
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as err:
        print(f"[ERROR] {device['host']}: {err}")
        return

    path = os.path.join(backup_dir, fname)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(running_cfg)
    print(f"[OK] Saved backup to {path}")

if __name__ == "__main__":
    backup_config(DEVICE)
