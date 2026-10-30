import socket
import struct
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

irtifa = 0.0
hiz = 150.0
durum = 1  # 1: Tırmanış, 2: Paraşüt Açıldı, 3: Yere İndi
paket_no = 0

print("Roket Aviyonik Simülatörü Başlatıldı. Veri fırlatılıyor...")

while True:
    paket_no += 1
    
    # Roket uçuş dinamiği simülasyonu
    if durum == 1:
        irtifa += hiz * 0.5
        hiz -= 3.5
        if hiz <= 0:
            durum = 2  # Tepe noktası, paraşüt tetiklendi
            hiz = -15.0
    elif durum == 2:
        irtifa += hiz * 0.5
        if irtifa <= 0:
            irtifa = 0
            durum = 3  # Yere indi

    # Byte Paketi: [Header(1B), PaketNo(4B), Irtifa(4B), Hiz(4B), Pil(1B), Durum(1B)]
    ham_veri = struct.pack("<BIffBB", 0xAA, paket_no, irtifa, hiz, 95, durum)
    
    # Basit Checksum (XOR) hesaplama
    checksum = 0
    for b in ham_veri:
        checksum ^= b
    
    tam_paket = ham_veri + struct.pack("<B", checksum)
    sock.sendto(tam_paket, (UDP_IP, UDP_PORT))
    
    time.sleep(0.5)