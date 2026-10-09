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

print("=== Arch Linux Eksiksiz & Kararlı XFCE Masaüstü Kurulumu ===")

USER_HOME = "/home/chaosx"

# 1. TAM VE KARARLI MASAÜSTÜ PAKETLERİ
PACKAGES = [
    # Masaüstü Ortamı & Panel
    "xfce4", "xfce4-goodies", "lightdm", "lightdm-gtk-greeter",
    # Ağ, Ses & Fontlar
    "network-manager-applet", "pulseaudio", "pavucontrol", "ttf-dejavu", "ttf-liberation", "papirus-icon-theme",
    # Uygulamalar (Tarayıcı, Medya, Arşiv, Güvenlik)
    "librewolf", "mpv", "eog", "file-roller", "firejail", "apparmor", "iptables",
    # Sanallaştırma & Araçlar
    "cifs-utils", "qemu-desktop", "virt-manager", "dnsmasq", "xdg-user-dirs"
]

print("[+] Temiz masaüstü paketleri yükleniyor...")
run(f"pacman -S --needed --noconfirm {' '.join(PACKAGES)}")

# 2. XDG KLASÖRLERİ & MASAÜSTÜ SİMGELERİ
run("sudo -u chaosx xdg-user-dirs-update")
DESKTOP_DIR = f"{USER_HOME}/Desktop"
run(f"mkdir -p {DESKTOP_DIR}")

# Masaüstü Kısayolları
write_file(f"{DESKTOP_DIR}/librewolf.desktop", """[Desktop Entry]
Version=1.0
Type=Application
Name=LibreWolf
Exec=librewolf
Icon=librewolf
Terminal=false
""", mode=0o755)

write_file(f"{DESKTOP_DIR}/pcmanfm.desktop", """[Desktop Entry]
Version=1.0
Type=Application
Name=Dosya Yöneticisi
Exec=thunar
Icon=org.xfce.thunar
Terminal=false
""", mode=0o755)

# 3. OTOMATİK GİRİŞ (LightDM Autologin)
write_file("/etc/lightdm/lightdm.conf", """
[Seat:*]
autologin-user=chaosx
autologin-user-timeout=0
user-session=xfce
""")

run("systemctl enable lightdm -f")

# 4. İZİNLER
run(f"chown -R chaosx:chaosx {USER_HOME}")

print("\n=== EKSİKSİZ MASAÜSTÜ KURULDU! REBOOT ATABİLİRSİNİZ. ===")
