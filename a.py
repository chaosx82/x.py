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

print("=== Ultra Lite Arch + Masaüstü Simgeleri & Duvar Kağıdı Onarımı ===")

USER_HOME = "/home/chaosx"

# 1. PAKET LİSTESİ
PACKAGES = [
    "labwc", "waybar", "wofi", "foot", "pcmanfm-qt", "mako", "grim", "slurp", "wl-clipboard",
    "gnome-themes-extra", "papirus-icon-theme", "ttf-liberation", "ttf-dejavu", "ttf-font-awesome",
    "librewolf", "mpv", "imv", "eog", "file-roller", "firejail", "apparmor", "iptables",
    "networkmanager", "cifs-utils", "qemu-desktop", "virt-manager", "dnsmasq",
    "swaybg", "xdg-user-dirs", "pipewire", "pipewire-pulse", "wireplumber", "pavucontrol"
]

print("[+] Paketler doğrulanıyor...")
run(f"pacman -S --needed --noconfirm {' '.join(PACKAGES)}")

# 2. XDG MASAÜSTÜ KLASÖRLERİ (Hem Desktop hem Masaüstü Garantilendi)
run("sudo -u chaosx xdg-user-dirs-update")
DESKTOP_1 = f"{USER_HOME}/Desktop"
DESKTOP_2 = f"{USER_HOME}/Masaüstü"
run(f"mkdir -p {DESKTOP_1} {DESKTOP_2} {USER_HOME}/.config/wallpapers")

# Masaüstü Kısayolları (.desktop dosyaları)
desktop_entry_librewolf = """[Desktop Entry]
Version=1.0
Type=Application
Name=LibreWolf
Exec=librewolf
Icon=librewolf
Terminal=false
"""

desktop_entry_foot = """[Desktop Entry]
Version=1.0
Type=Application
Name=Uçbirim
Exec=foot
Icon=utilities-terminal
Terminal=false
"""

desktop_entry_pcmanfm = """[Desktop Entry]
Version=1.0
Type=Application
Name=Dosya Yöneticisi
Exec=pcmanfm-qt
Icon=system-file-manager
Terminal=false
"""

for target_dir in [DESKTOP_1, DESKTOP_2]:
    write_file(f"{target_dir}/librewolf.desktop", desktop_entry_librewolf, mode=0o755)
    write_file(f"{target_dir}/foot.desktop", desktop_entry_foot, mode=0o755)
    write_file(f"{target_dir}/pcmanfm-qt.desktop", desktop_entry_pcmanfm, mode=0o755)

# 3. GARANTİ MAT KOYU DUVAR KAĞIDI (PNG Formatında)
ppm_path = f"{USER_HOME}/.config/wallpapers/dark.ppm"
header = b"P6\n1920 1080\n255\n"
pixel = bytes([25, 30, 40])  # Koyu Mat Lacivert/Gri Tonu
with open(ppm_path, "wb") as f:
    f.write(header + pixel * (1920 * 1080))

# 4. LABWC AUTOSTART (Masaüstü Simgeleri + Swaybg Garanti Başlatma)
write_file(f"{USER_HOME}/.config/labwc/autostart", f"""
swaybg -i {USER_HOME}/.config/wallpapers/dark.ppm -m fill &
pcmanfm-qt --desktop --profile=lxqt &
waybar &
mako &
gsettings set org.gnome.desktop.interface gtk-theme 'Arc-Dark'
gsettings set org.gnome.desktop.interface icon-theme 'Papirus-Dark'
""")

# 5. LABWC MASAÜSTÜ MENÜSÜ
write_file(f"{USER_HOME}/.config/labwc/menu.xml", """<?xml version="1.0" encoding="UTF-8"?>
<labwc_menu>
  <menu id="root-menu" label="Ana Menü">
    <item label="Uçbirim (Terminal)"><action name="Execute" command="foot"/></item>
    <item label="Dosya Yöneticisi"><action name="Execute" command="pcmanfm-qt"/></item>
    <item label="LibreWolf Tarayıcı"><action name="Execute" command="librewolf"/></item>
    <item label="Ses Denetimi"><action name="Execute" command="pavucontrol"/></item>
    <separator/>
    <item label="Başlat Menüsü"><action name="Execute" command="wofi --show drun"/></item>
    <separator/>
    <item label="Yeniden Yapılandır"><action name="Reconfigure"/></item>
    <item label="Çıkış"><action name="Exit"/></item>
  </menu>
</labwc_menu>
""")

# 6. WOFI VE WAYBAR
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
window { margin: 0px; border: 2px solid #5294e2; background-color: #1e2229; border-radius: 8px; font-family: sans-serif; font-size: 13px; }
#input { margin: 8px; border: 1px solid #383c4a; color: #ffffff; background-color: #282c34; border-radius: 4px; }
#entry:selected { background-color: #5294e2; border-radius: 4px; }
#entry:selected #text { color: #ffffff; }
""")

write_file(f"{USER_HOME}/.config/waybar/config", """
{
    "layer": "top",
    "position": "bottom",
    "height": 32,
    "modules-left": ["custom/menu", "wlr/taskbar"],
    "modules-center": [],
    "modules-right": ["pulseaudio", "cpu", "memory", "clock"],
    
    "custom/menu": {
        "format": " ☰ Başlat ",
        "on-click": "wofi --show drun"
    },
    "wlr/taskbar": {
        "format": "{icon} {title}",
        "on-click": "activate"
    },
    "pulseaudio": {
        "format": "Ses: {volume}%",
        "on-click": "pavucontrol"
    },
    "cpu": { "format": "CPU: {usage}%" },
    "memory": { "format": "RAM: {percentage}%" },
    "clock": { "format": "{:%H:%M - %d.%m.%Y}" }
}
""")

write_file(f"{USER_HOME}/.config/waybar/style.css", """
* { border: none; font-family: FontAwesome, sans-serif; font-size: 13px; }
window#waybar { background-color: #1e2229; color: #ffffff; }
#custom-menu { background-color: #5294e2; color: #ffffff; font-weight: bold; padding: 0 12px; border-radius: 4px; margin: 3px; }
#taskbar button { padding: 0 10px; color: #d3dae3; }
#taskbar button.active { background-color: #383c4a; border-bottom: 2px solid #5294e2; }
#pulseaudio, #cpu, #memory, #clock { padding: 0 10px; background-color: #282c34; margin-left: 2px; }
""")

# 7. İZİNLER
run(f"chown -R chaosx:chaosx {USER_HOME}")

print("\n=== MASAÜSTÜ SİMGELERİ VE DUVAR KAĞIDI DÜZELTİLDİ! ===")
