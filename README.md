## ⏱️ Zamanlayıcı Sistemi (zamanlayici-sistemi)

Bilgisayarınızda tıpkı eski internet kafelerdeki gibi çalışan, çocuklar için özel olarak tasarlanmış bir ekran süresi yönetim ve zamanlayıcı uygulamasıdır. 

Ebeveynlerin çocuklarının bilgisayar başında geçirdiği süreyi kontrol altında tutmasını sağlar. İstediğiniz süreyi ayarlar ve bırakırsınız; uygulama sağ alt köşede (sistem tepsisinde) geriye doğru saymaya başlar. Süre dolduğunda bilgisayarı otomatik olarak güvenli bir şekilde kapatır.

## ✨ Özellikler

* **İnternet Kafe Mantığı:** Basit ve anlaşılır süre tabanlı çalışma sistemi.
* **Arka Plan Modu (System Tray):** Ekranı kaplamaz, sağ altta sessizce çalışır ve anlık kalan süreyi gösterir.
* **Esnek Kontrol:** İstediğiniz an süreyi duraklatabilir veya tamamen iptal edebilirsiniz.
* **Otomatik Kapatma (Auto-Shutdown):** Süre sıfırlandığında bilgisayarı otomatik olarak kapatır.
* **Hafif ve Hızlı:** Bilgisayarı yormayan, tamamen Python ile geliştirilmiş yapı.

## 🚀 Kurulum ve Çalıştırma

Projeyi yerel bilgisayarınızda çalıştırmak için [Buraya](https://github.com/Taner-kt/zamanlayici-sistemi/releases/download/v1.0.0/timer.exe) tıklayarak indirebilirsiniz!

### Kod Kullanarak Çalıştırma

* Bilgisayarınızda **Python 3.8+** sürümünün yüklü olduğundan emin olun.
* `pip install pystray pillow pyinstaller` kodu ile harici kütüphaneleri ekleyin.
* `python -m PyInstaller --noconsole --onefile --icon=logo.ico --add-data "logo.ico;." app.py` ile .exe oluşturabilirsiniz.
