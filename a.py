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

print("=== Ultra Lite Arch + LabWC Görsel & Sistem Düzeltmesi ===")

USER_HOME = "/home/chaosx"

# 1. PAKET LİSTESİ
PACKAGES = [
    "labwc", "waybar", "wofi", "foot", "pcmanfm-qt", "mako", "grim", "slurp", "wl-clipboard",
    "gnome-themes-extra", "papirus-icon-theme", "ttf-liberation", "ttf-dejavu",
    "librewolf", "mpv", "imv", "firejail", "apparmor", "iptables",
    "networkmanager", "cifs-utils", "qemu-desktop", "virt-manager", "dnsmasq",
    "swaybg", "xdg-user-dirs"
]

print("[+] Paketler doğrulanıyor...")
run(f"pacman -S --needed --noconfirm {' '.join(PACKAGES)}")

# 2. STANDART KULLANICI KLASÖRLERİ
run("sudo -u chaosx xdg-user-dirs-update")
run(f"mkdir -p {USER_HOME}/Masaüstü {USER_HOME}/Desktop {USER_HOME}/İndirilenler {USER_HOME}/Applications {USER_HOME}/securityai {USER_HOME}/.config/firejail {USER_HOME}/.config/wallpapers")

# 3. MAT KOYU DUVAR KAĞIDI OLUŞTURMA (Temiz Python Dosya Yazımı)
ppm_path = f"{USER_HOME}/.config/wallpapers/dark.ppm"
header = b"P6\n1920 1080\n255\n"
pixel = bytes([24, 26, 31])
with open(ppm_path, "wb") as f:
    f.write(header + pixel * (1920 * 1080))

# 4. LABWC AUTOSTART
write_file(f"{USER_HOME}/.config/labwc/autostart", f"""
swaybg -i {USER_HOME}/.config/wallpapers/dark.ppm -m fill &
waybar &
mako &
gsettings set org.gnome.desktop.interface gtk-theme 'Arc-Dark'
gsettings set org.gnome.desktop.interface icon-theme 'Papirus-Dark'
""")

# 5. LABWC SAĞ TIK MENÜSÜ
write_file(f"{USER_HOME}/.config/labwc/menu.xml", """<?xml version="1.0" encoding="UTF-8"?>
<labwc_menu>
  <menu id="root-menu" label="Ana Menü">
    <item label="Uçbirim (Terminal)"><action name="Execute" command="foot"/></item>
    <item label="Dosya Yöneticisi"><action name="Execute" command="pcmanfm-qt"/></item>
    <item label="LibreWolf Tarayıcı"><action name="Execute" command="librewolf"/></item>
    <separator/>
    <item label="Başlat Menüsü"><action name="Execute" command="wofi --show drun"/></item>
    <separator/>
    <item label="Yeniden Yapılandır"><action name="Reconfigure"/></item>
    <item label="Çıkış"><action name="Exit"/></item>
  </menu>
</labwc_menu>
""")

# 6. WOFI BAŞLAT MENÜSÜ STİLİ (Sol Alt Köşe)
write_file(f"{USER_HOME}/.config/wofi/config", """
mode=drun
width=320
height=450
location=bottom_left
xoffset=5
yoffset=-38
prompt=Uygulama Ara...
filter_rate=100
allow_markup=true
no_actions=true
halign=fill
orientation=vertical
content_halign=fill
insensitive=true
""")

write_file(f"{USER_HOME}/.config/wofi/style.css", """
window {
    margin: 0px;
    border: 2px solid #5294e2;
    background-color: #1e2229;
    border-radius: 8px;
    font-family: sans-serif;
    font-size: 13px;
}
#input {
    margin: 8px;
    border: 1px solid #383c4a;
    color: #ffffff;
    background-color: #282c34;
    border-radius: 4px;
}
#inner-box {
    margin: 5px;
    background-color: transparent;
}
#outer-box {
    margin: 5px;
    background-color: transparent;
}
#scroll {
    margin: 0px;
}
#text {
    margin: 4px;
    color: #d3dae3;
}
#entry:selected {
    background-color: #5294e2;
    border-radius: 4px;
}
#entry:selected #text {
    color: #ffffff;
}
""")

# 7. WAYBAR ALT PANEL
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

# 8. İZİNLER
run(f"chown -R chaosx:chaosx {USER_HOME}")

print("\n=== TÜM GÖRSEL DÜZELTMELER BAŞARIYLA UYGULANDI! ===")
