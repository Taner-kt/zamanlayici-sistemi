import tkinter as tk
from tkinter import messagebox
import os
import sys
import threading
import pystray
from PIL import Image, ImageDraw
import ctypes

def kaynak_yolu(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class ZamanlayiciUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Bilgisayar zamanlayıcı")
        
        self.root.geometry("350x160") 
        self.root.resizable(False, False)
        
        self.root.configure(bg="#000000")

        # --- İKON YÜKLEME BÖLÜMÜ ---
        try:
            ikon_yolu = kaynak_yolu("logo.ico")
            self.root.iconbitmap(default=ikon_yolu)
        except Exception as e:
            print(f"Uyarı: İkon yüklenemedi. Lütfen 'logo.ico' dosyasının klasörde olduğundan emin olun. Hata: {e}")

        self.kalan_saniye = 0
        self.calisiyor = False
        self.duraklatildi = False
        self.sayac_penceresi = None
        self.sayac_gorunur = True 
        
        self.root.protocol("WM_DELETE_WINDOW", self.kapatma_yoneticisi)

        # --- Arayüz Tasarımı ---
        self.lbl_ana = tk.Label(root, text="Kapanma Süresi (Dakika):", font=("Segoe UI", 12, "bold"), fg="white", bg="black")
        self.lbl_ana.pack(pady=15)
        
        self.sure_girisi = tk.Entry(root, font=("Segoe UI", 14, "bold"), justify="center", bg="#2D2D2D", fg="white", insertbackground="white", relief="flat")
        self.sure_girisi.pack(pady=5)

        self.btn_calistir = tk.Button(root, text="Çalıştır", width=25, command=self.baslat, bg="#27AE60", fg="white", activebackground="#219150", relief="flat")
        self.btn_calistir.pack(pady=7)

        self.btn_duraklat = tk.Button(root, text="Durdur / Devam Ettir", width=25, command=self.duraklat_devam_ettir, bg="#F1C40F", fg="white", activebackground="#D4AC0D", relief="flat", disabledforeground="white")
        self.btn_sayac_goster_gizle = tk.Button(root, text="Sayacı Gizle", width=25, command=self.sayac_goster_gizle, bg="#3498DB", fg="white", activebackground="#2980B9", relief="flat", disabledforeground="white")
        self.btn_iptal = tk.Button(root, text="İptal Et", width=25, command=self.iptal_et, bg="#95A5A6", fg="white", activebackground="#7F8C8D", relief="flat", disabledforeground="white")
        self.btn_kapat = tk.Button(root, text="Hemen Kapat", width=25, command=self.hemen_kapat, bg="#E74C3C", fg="white", activebackground="#C0392B", relief="flat")

    def kapatma_yoneticisi(self):
        if self.calisiyor:
            self.tepsiye_gonder()
        else:
            self.root.destroy()
            os._exit(0) 

    def baslat(self):
        try:
            dakika = float(self.sure_girisi.get())
            if dakika <= 0:
                raise ValueError
                
            self.kalan_saniye = int(dakika * 60)
            self.calisiyor = True
            self.duraklatildi = False
            self.sayac_gorunur = True

            self.btn_calistir.config(state=tk.DISABLED)
            
            self.root.geometry("350x360")
            
            self.btn_duraklat.pack(pady=7)
            self.btn_sayac_goster_gizle.pack(pady=7)
            self.btn_iptal.pack(pady=7)
            self.btn_kapat.pack(pady=7)

            self.sayac_penceresi_olustur()
            self.geri_sayim()
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli ve 0'dan büyük bir dakika girin.")

    def iptal_et(self):
        self.calisiyor = False
        self.duraklatildi = False
        
        if self.sayac_penceresi:
            self.sayac_penceresi.destroy()
            self.sayac_penceresi = None
            
        self.sure_girisi.delete(0, tk.END)
        
        self.btn_calistir.config(state=tk.NORMAL)
        self.btn_duraklat.pack_forget()
        self.btn_sayac_goster_gizle.pack_forget()
        self.btn_iptal.pack_forget()
        self.btn_kapat.pack_forget()
        
        self.root.geometry("350x160")
        
        messagebox.showinfo("İptal", "Zamanlayıcı iptal edildi. Yeni bir süre girebilirsiniz.")

    def sayac_penceresi_olustur(self):
        if self.sayac_penceresi is not None:
            self.sayac_penceresi.destroy()

        self.sayac_penceresi = tk.Toplevel(self.root)
        self.sayac_penceresi.overrideredirect(True)
        self.sayac_penceresi.attributes("-topmost", True)
        self.sayac_penceresi.configure(bg="#000000")

        ekran_genisligi = self.root.winfo_screenwidth()
        ekran_yuksekligi = self.root.winfo_screenheight()
        
        pencere_genisligi = 190 
        pencere_yuksekligi = 55
        
        x = ekran_genisligi - pencere_genisligi - 20
        y = ekran_yuksekligi - pencere_yuksekligi - 60 
        self.sayac_penceresi.geometry(f"{pencere_genisligi}x{pencere_yuksekligi}+{x}+{y}")

        self.lbl_sayac = tk.Label(self.sayac_penceresi, text="", font=("Consolas", 22, "bold"), fg="#00FF00", bg="black")
        self.lbl_sayac.pack(expand=True, fill=tk.BOTH)
        self.guncelle_sayac_etiketi()

    def guncelle_sayac_etiketi(self):
        saat = self.kalan_saniye // 3600
        dk = (self.kalan_saniye % 3600) // 60
        sn = self.kalan_saniye % 60
        
        if saat > 0:
            zaman_metni = f"{saat:02d}:{dk:02d}:{sn:02d}"
        else:
            zaman_metni = f"{dk:02d}:{sn:02d}"

        if self.duraklatildi:
            self.lbl_sayac.config(text=f"⏸️ {zaman_metni}", fg="#FF0000")
        else:
            self.lbl_sayac.config(text=zaman_metni, fg="#00FF00")

    def geri_sayim(self):
        if self.calisiyor and not self.duraklatildi:
            if self.kalan_saniye > 0:
                self.guncelle_sayac_etiketi()
                self.kalan_saniye -= 1
                self.root.after(1000, self.geri_sayim)
            else:
                self.bilgisayari_kapat()

    def duraklat_devam_ettir(self):
        self.duraklatildi = not self.duraklatildi
        if not self.duraklatildi:
            self.guncelle_sayac_etiketi()
            self.geri_sayim()
        else:
            if self.sayac_penceresi:
                self.guncelle_sayac_etiketi()

    def sayac_goster_gizle(self):
        if self.sayac_penceresi is not None:
            if self.sayac_gorunur:
                self.sayac_penceresi.withdraw()
                self.sayac_gorunur = False
                self.btn_sayac_goster_gizle.config(text="Sayacı Göster")
            else:
                self.sayac_penceresi.deiconify()
                self.sayac_gorunur = True
                self.btn_sayac_goster_gizle.config(text="Sayacı Gizle")

    def hemen_kapat(self):
        cevap = messagebox.askyesno("Uyarı", "Bilgisayarı şu an kapatmak istediğinize emin misiniz?")
        if cevap:
            self.bilgisayari_kapat()

    def bilgisayari_kapat(self):
        if self.sayac_penceresi:
            self.sayac_penceresi.destroy()
        # os.system("shutdown /s /t 0")
        print("Bilgisayar kapanıyor...")

    def ikon_olustur(self):
        try:
            ikon_yolu = kaynak_yolu("logo.ico")
            image = Image.open(ikon_yolu).convert("RGBA")
            return image
        except Exception as e:
            print(f"Uyarı: Tepsi ikonu yüklenemedi: {e}")
            image = Image.new('RGB', (64, 64), color=(39, 174, 96))
            dc = ImageDraw.Draw(image)
            dc.rectangle((16, 16, 48, 48), fill=(255, 255, 255))
            return image

    def tepsiye_gonder(self):
        self.root.withdraw()
        
        menu = pystray.Menu(
            pystray.MenuItem("Göster", self.tepsiden_cikar, default=True),
            pystray.MenuItem("Tamamen Kapat", self.uygulamayi_kapat)
        )
        
        self.ikon = pystray.Icon("Zamanlayici", self.ikon_olustur(), "Bilgisayar Zamanlayıcı", menu)
        threading.Thread(target=self.ikon.run, daemon=True).start()

    def tepsiden_cikar(self, icon, item):
        icon.stop()
        self.root.after(0, self.root.deiconify)

    def uygulamayi_kapat(self, icon, item):
        icon.stop()
        self.root.after(0, self.root.destroy)
        os._exit(0) 

if __name__ == "__main__":
    # YENİ: Windows görev çubuğu ikon sorunu için AppUserModelID ayarlaması
    try:
        # Uygulamanıza özel benzersiz bir kimlik tanımlıyoruz
        myappid = 'benim.zamanlayici.uygulamam.v1'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass # Eğer sistem Windows değilse veya hata verirse atla

    # Uygulamanın zaten açık olup olmadığını kontrol ediyoruz
    mutex_adi = "BilgisayarZamanlayici_TekGirdi_Mutex"
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, mutex_adi)
    hata_kodu = ctypes.windll.kernel32.GetLastError()

    if hata_kodu == 183:
        temp_root = tk.Tk()
        temp_root.withdraw()
        messagebox.showwarning("Zaten Çalışıyor", "Uygulama zaten açık!\n\nLütfen görev çubuğunu veya sağ alt köşedeki gizli simgeleri (yukarı ok işareti) kontrol edin.")
        temp_root.destroy()
        sys.exit(0) 

    root = tk.Tk()
    app = ZamanlayiciUygulamasi(root)
    root.mainloop()
