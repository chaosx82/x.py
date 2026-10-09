#!/usr/bin/env python3
import os
import subprocess

def run(cmd):
    print(f"--> [Çalıştırılıyor]: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def write_file(path, content, mode=0o644):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    os.chmod(path, mode)

print("=== Ultra Lite Arch + LabWC Görsel & Sistem Yapılandırması ===")

USER_HOME = "/home/chaosx"

# 1. PAKET LİSTESİ VE KURULUM
PACKAGES = [
    "labwc", "waybar", "wofi", "foot", "pcmanfm-qt", "mako", "grim", "slurp", "wl-clipboard",
    "gnome-themes-extra", "papirus-icon-theme", "ttf-liberation", "ttf-dejavu",
    "librewolf", "mpv", "imv", "firejail", "apparmor", "iptables",
    "networkmanager", "cifs-utils", "qemu-desktop", "virt-manager", "dnsmasq"
]

print("[+] Paketler doğrulanıyor...")
run(f"pacman -S --needed --noconfirm {' '.join(PACKAGES)}")

# 2. AUTOLOGIN & TTY1
write_file("/etc/systemd/system/getty@tty1.service.d/override.conf", """
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin chaosx --noclear %I $TERM
""")

write_file(f"{USER_HOME}/.bash_profile", """
if [ -z "$DISPLAY" ] && [ "$XDG_VTNR" -eq 1 ]; then
  exec labwc
fi
""")

# 3. LABWC AUTOSTART & TEMA
write_file(f"{USER_HOME}/.config/labwc/autostart", """
waybar &
mako &
gsettings set org.gnome.desktop.interface gtk-theme 'Arc-Dark'
gsettings set org.gnome.desktop.interface icon-theme 'Papirus-Dark'
""")

# 4. SAĞ TIK MENÜSÜ (LABWC MENU.XML)
write_file(f"{USER_HOME}/.config/labwc/menu.xml", """<?xml version="1.0" encoding="UTF-8"?>
<labwc_menu>
  <menu id="root-menu" label="Ana Menü">
    <item label="Uçbirim (Terminal)"><action name="Execute" command="foot"/></item>
    <item label="Dosya Yöneticisi"><action name="Execute" command="pcmanfm-qt"/></item>
    <item label="LibreWolf Tarayıcı"><action name="Execute" command="librewolf"/></item>
    <separator/>
    <item label="Uygulama Menüsü (Wofi)"><action name="Execute" command="wofi --show drun"/></item>
    <separator/>
    <item label="Yeniden Yapılandır"><action name="Reconfigure"/></item>
    <item label="Çıkış"><action name="Exit"/></item>
  </menu>
</labwc_menu>
""")

# 5. WAYBAR ALT PANEL (XP/MAT SIYAH TEMA)
write_file(f"{USER_HOME}/.config/waybar/config", """
{
    "layer": "top",
    "position": "bottom",
    "height": 32,
    "modules-left": ["custom/menu", "wlr/taskbar"],
    "modules-center": [],
    "modules-right": ["cpu", "memory", "clock"],
    
    "custom/menu": {
        "format": "  Başlat ",
        "on-click": "wofi --show drun"
    },
    "wlr/taskbar": {
        "format": "{icon} {title}",
        "on-click": "activate"
    },
    "cpu": { "format": "CPU: {usage}%" },
    "memory": { "format": "RAM: {percentage}%" },
    "clock": { "format": "{:%H:%M - %d.%m.%Y}" }
}
""")

write_file(f"{USER_HOME}/.config/waybar/style.css", """
* {
    border: none;
    font-family: sans-serif;
    font-size: 13px;
}
window#waybar {
    background-color: #1e2229;
    color: #ffffff;
}
#custom-menu {
    background-color: #2d313b;
    color: #5294e2;
    font-weight: bold;
    padding: 0 12px;
}
#taskbar button {
    padding: 0 10px;
    color: #d3dae3;
}
#taskbar button.active {
    background-color: #383c4a;
    border-bottom: 2px solid #5294e2;
}
#cpu, #memory, #clock {
    padding: 0 10px;
    background-color: #282c34;
    margin-left: 2px;
}
""")

# 6. KLASÖR VE İZİNLER
run(f"mkdir -p {USER_HOME}/Applications {USER_HOME}/securityai {USER_HOME}/.config/firejail")
run(f"chown -R chaosx:chaosx {USER_HOME}")

print("\n=== TÜM AYARLAR BAŞARIYLA YAZILDI! ===")
