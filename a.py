#!/usr/bin/env python3
import os
import subprocess

TARGET = "/mnt" if os.path.exists("/mnt/etc") else ""

def run(cmd):
    print(f"--> [Çalıştırılıyor]: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def write_file(path, content, mode=0o644):
    full_path = os.path.join(TARGET, path.lstrip("/"))
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    os.chmod(full_path, mode)

print("=== Ultra Lite Arch + LabWC Kurulum Betiği Başlatılıyor ===")

# 1. PAKET LİSTESİ VE KURULUM
PACKAGES = [
    # Temel Masaüstü & Wayland Katmanı
    "labwc", "waybar", "wofi", "foot", "pcmanfm-qt", "mako", "grim", "slurp", "wl-clipboard",
    # Temalar & İkonlar
    "arc-gtk-theme", "papirus-icon-theme", "ttf-liberation", "ttf-dejavu",
    # Uygulamalar & Görüntüleyiciler
    "librewolf", "mpv", "imv", "firejail", "apparmor", "iptables",
    # Ağ & Sistem Araçları
    "networkmanager", "cifs-utils", "qemu-desktop", "virt-manager", "dnsmasq"
]

print("[+] Paketler yükleniyor...")
run(f"pacman -S --needed --noconfirm {' '.join(PACKAGES)}")

# 2. ŞİFREMİZ/OTOMATİK GİRİŞ (TTY1 -> LabWC)
write_file("/etc/systemd/system/getty@tty1.service.d/override.conf", """
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin chaosx --noclear %I $TERM
""")

# .bash_profile üzerinden TTY1'de otomatik LabWC başlatma
write_file("/home/chaosx/.bash_profile", """
if [ -z "$DISPLAY" ] && [ "$XDG_VTNR" -eq 1 ]; then
  exec labwc
fi
""")

# 3. NETWORKMANAGER & DISABLED IPV6
write_file("/etc/NetworkManager/conf.d/00-disable-ipv6.conf", """
[main]
dns=default

[connection]
ipv6.method=disabled
""")

conn_file = "/etc/NetworkManager/system-connections/Kablolu Ag.nmconnection"
write_file(conn_file, """
[connection]
id=Kablolu Ag
uuid=98765432-1111-2222-3333-444455556666
type=ethernet
autoconnect=true

[ethernet]

[ipv4]
method=auto

[ipv6]
method=disabled
""", mode=0o600)

# 4. GÖRSEL TEMA VE XP-TARZI WAYBAR PANEL YAPILANDIRMASI
write_file("/home/chaosx/.config/labwc/autostart", """
waybar &
mako &
gsettings set org.gnome.desktop.interface gtk-theme 'Arc-Dark'
gsettings set org.gnome.desktop.interface icon-theme 'Papirus-Dark'
""")

# Waybar Konfigürasyonu (Alt Panel)
write_file("/home/chaosx/.config/waybar/config", """
{
    "layer": "top",
    "position": "bottom",
    "height": 30,
    "modules-left": ["custom/menu", "wlr/taskbar"],
    "modules-center": [],
    "modules-right": ["cpu", "memory", "network", "pulseaudio", "clock"],
    
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
    "network": { "format": "Ağ: {ifname}" },
    "pulseaudio": { "format": "Ses: {volume}%" },
    "clock": { "format": "{:%H:%M | %d.%m.%Y}" }
}
""")

# Waybar Stil (Arc-Dark Mat Siyah Teması)
write_file("/home/chaosx/.config/waybar/style.css", """
* {
    border: none;
    font-family: Liberation Sans, sans-serif;
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
    padding: 0 10px;
}
#taskbar button {
    padding: 0 8px;
    color: #d3dae3;
}
#taskbar button.active {
    background-color: #383c4a;
    border-bottom: 2px solid #5294e2;
}
#cpu, #memory, #network, #pulseaudio, #clock {
    padding: 0 10px;
    background-color: #282c34;
    margin-left: 2px;
}
""")

# 5. UYGULAMA İZOLASYONLARI VE DIŞ KLASÖRLER
run("mkdir -p /home/chaosx/Applications /home/chaosx/securityai /home/chaosx/.config/firejail")

# AppImage Update Kontrolünü Kapatma
write_file("/home/chaosx/.config/firejail/firejail.config", "no-appimage-update yes\n")

# İzinlerin ayarlanması
run("chown -R chaosx:chaosx /home/chaosx")

print("\n=== KURULUM TAMAMLANDI! ===")
