import socket
import struct
import threading
import tkinter as tk

class YerIstasyonu:
    def __init__(self, root):
        self.root = root
        self.root.title("STNM - Roket Yer Kontrol İstasyonu")
        self.root.geometry("450x450")
        self.root.configure(bg="#1e1e2e")

        # Bilgi Etiketleri
        self.lbl_baslik = tk.Label(root, text="CANLI TELEMETRİ HATTI", fg="#89b4fa", bg="#1e1e2e", font=("Arial", 14, "bold"))
        self.lbl_baslik.pack(pady=10)

        self.lbl_paket = tk.Label(root, text="Paket No: --", fg="#cdd6f4", bg="#1e1e2e", font=("Arial", 11))
        self.lbl_paket.pack()

        self.lbl_irtifa = tk.Label(root, text="İrtifa: 0.0 m", fg="#a6e3a1", bg="#1e1e2e", font=("Arial", 16, "bold"))
        self.lbl_irtifa.pack(pady=5)

        self.lbl_hiz = tk.Label(root, text="Hız: 0.0 m/s", fg="#cdd6f4", bg="#1e1e2e", font=("Arial", 11))
        self.lbl_hiz.pack()

        self.lbl_durum = tk.Label(root, text="Durum: Bekleniyor...", fg="#f9e2af", bg="#1e1e2e", font=("Arial", 12, "bold"))
        self.lbl_durum.pack(pady=5)

        self.lbl_cs = tk.Label(root, text="Checksum: --", fg="#cdd6f4", bg="#1e1e2e", font=("Arial", 10))
        self.lbl_cs.pack()

        # Basit Canlı İrtifa Grafiği (Canvas)
        self.canvas = tk.Canvas(root, width=380, height=180, bg="#11111b", highlightthickness=0)
        self.canvas.pack(pady=15)
        self.points = []

        # Arka planda UDP dinleyici başlat
        threading.Thread(target=self.udp_dinle, daemon=True).start()

    def udp_dinle(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("127.0.0.1", 5005))

        durum_metinleri = {1: "TIRMANIŞTA", 2: "PARAŞÜT AÇILDI", 3: "GÖREV TAMAM (İNDİ)"}

        while True:
            veri, _ = sock.recvfrom(1024)
            if len(veri) == 16:  # 15 bayt veri + 1 bayt checksum
                baslik, p_no, irt, hz, pil, st, alinan_cs = struct.unpack("<BIffBBB", veri)

                hesaplanan_cs = 0
                for b in veri[:-1]:
                    hesaplanan_cs ^= b

                cs_durum = "DOĞRULANDI (OK)" if hesaplanan_cs == alinan_cs else "HATALI PAKET!"
                cs_renk = "#a6e3a1" if hesaplanan_cs == alinan_cs else "#f38ba8"

                self.root.after(0, self.ekrani_guncelle, p_no, irt, hz, durum_metinleri.get(st, "Bilinmiyor"), cs_durum, cs_renk)

    def ekrani_guncelle(self, p_no, irt, hz, durum, cs_durum, cs_renk):
        self.lbl_paket.config(text=f"Paket No: {p_no}")
        self.lbl_irtifa.config(text=f"İrtifa: {irt:.1f} m")
        self.lbl_hiz.config(text=f"Hız: {hz:.1f} m/s")
        self.lbl_durum.config(text=f"Durum: {durum}")
        self.lbl_cs.config(text=f"Paket Bütünlüğü: {cs_durum}", fg=cs_renk)

        # Grafiğe çizgi ekle
        self.points.append(irt)
        if len(self.points) > 35:
            self.points.pop(0)

        self.canvas.delete("all")
        for i in range(len(self.points) - 1):
            x1 = i * 10 + 15
            y1 = 170 - (self.points[i] / 2000.0 * 150)
            x2 = (i + 1) * 10 + 15
            y2 = 170 - (self.points[i+1] / 2000.0 * 150)
            self.canvas.create_line(x1, y1, x2, y2, fill="#a6e3a1", width=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = YerIstasyonu(root)
    root.mainloop()