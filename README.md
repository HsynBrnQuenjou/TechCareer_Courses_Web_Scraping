# TechCareer_Courses_Web_Scraping
# 📚 TechCareer Courses Web Scraping

Bu proje, [TechCareer.net](https://www.techcareer.net/courses) sitesindeki tüm kursları otomatik olarak tarayarak Excel dosyası olarak kaydeden bir Python scriptidir. Kurs bilgileri; kurs adı, seviyesi, süresi, sertifika durumu ve detay sayfasının linkini içerir.

## 🚀 Özellikler

- Tüm sayfalardaki kurs verilerini toplar (pagination destekli)
- Kurs adı, seviye, süre ve sertifika bilgilerini çeker
- Her kursun detay sayfasına yönlendiren linki oluşturur
- Sonuçları `techcareer_kurslar.xlsx` olarak kaydeder
- Eğer dosya yazılamazsa yedek `.xlsx` dosyasına kayıt yapar
- Hataları ayrıntılı olarak loglar

## 📦 Gereksinimler

- Python 3.7+
- Google Chrome tarayıcısı
- ChromeDriver (Chrome sürümünüzle uyumlu)

### Python Paketleri

```bash
pip install selenium pandas openpyxl
````

> `openpyxl`, `.xlsx` formatında Excel yazabilmek için gereklidir.

## 🔧 Kurulum

1. [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/)'ı indirip proje dizinine yerleştirin.
2. `chromedriver.exe` yolunu aşağıdaki satırda güncelleyin (gerekiyorsa):

```python
service = Service("chromedriver.exe")  # Gerekirse tam yol verin
```

## 🧠 Kullanım

```bash
python techcareer_scraper.py
```

Script çalıştırıldığında:

* Tarayıcı açılır
* Tüm kurs verileri toplanır
* `techcareer_kurslar.xlsx` dosyası oluşturulur

## 🗂️ Çıktı Örneği

| Kurs Adı                   | Seviyesi  | Süresi   | Sertifika | Link                                                                                                                           |
| -------------------------- | --------- | -------- | --------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Linux Bash Script Eğitimi | Orta | 7 Saat | Var       | [https://www.techcareer.net/courses/linux-bash-script-egitimi](https://www.techcareer.net/courses/linux-bash-script-egitimi) |

## ⚠️ Hatalar ve Uyarılar

* Eğer Excel dosyası açıksa `PermissionError` alınabilir. Lütfen dosyayı kapatın.
* Eğer "next page" butonu çalışmazsa sayfa yapısı değişmiş olabilir.
* WebDriver hatalarında, ChromeDriver sürümünüzü kontrol edin.
* 
---

---

✅ Bu script sayesinde TechCareer'deki tüm kurslara hızlıca ulaşabilir ve analiz edebilirsiniz.

---

## 📌 Excel Düzenleme İpucu

Excel'deki veri görünümünü otomatik olarak düzgün hale getirmek için:

1. `Sheet1` sekmesine sağ tıklayın → **Kod Görüntüle** seçeneğine tıklayın.
2. Sol üstte açılan kod penceresinde `(General)` yazan yeri **Worksheet** olarak değiştirin.
3. Aşağıdaki kod satırını ekleyin:

```vba
Columns.AutoFit
```

4. `Ctrl + S` ile kaydedin ve dosyayı kapatın.
5. Şimdi Excel dosyanız açıldığında sütunlar otomatik olarak içeriklere göre hizalanmış olacaktır.

---

## İletişim

Herhangi bir sorun ya da öneri için bana ulaşabilirsiniz.

---

## 👨‍💻 Geliştirici

**Baran Hüseyin Kençü**
Otomasyon ve veri işleme tutkusu ile geliştirildi. 💻❤️
