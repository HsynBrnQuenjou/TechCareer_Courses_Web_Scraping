from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException, \
    StaleElementReferenceException
import pandas as pd
import time
import os

# ChromeDriver yolu
service = Service("chromedriver.exe")
driver = None

try:
    driver = webdriver.Chrome(service=service)

    # Sayfayı aç
    print("Web sayfasını açılıyor: https://www.techcareer.net/courses")
    driver.get("https://www.techcareer.net/courses")
    time.sleep(5)  # Sayfanın yüklenmesi için başlangıç bekleme süresi

    veriler = []
    page_number = 1

    while True:
        print(f"\nKurs verileri toplanıyor... Sayfa {page_number}")

        # Sayfanın tamamen yüklenmesini beklemek için kurs öğelerinin görünür olmasını bekleyelim.
        # Bu, her sayfa yüklendiğinde içeriğin hazır olduğundan emin olmamızı sağlar.
        try:
            WebDriverWait(driver, 20).until(  # Artırılmış bekleme süresi
                EC.presence_of_all_elements_located((By.XPATH, "//div[@data-test='course-item']"))
            )
            # Eğer sayfadaki kurslar değiştiyse ve bir öncekini yakalamak istiyorsak
            # örneğin, ilk kursun metninin bir önceki iterasyondaki ilk kurstan farklı olmasını bekleyebiliriz.
            # Ancak bu daha karmaşık ve bazen aşırıya kaçabilir. Mevcut yöntem genellikle yeterlidir.

        except TimeoutException:
            print(f"Sayfa {page_number} için kurs öğeleri yüklenemedi veya çok uzun sürdü. Bu sayfayı atlıyorum.")
            break

            # Tüm kurs kutularını bul
        kurs_divleri = driver.find_elements(By.XPATH, "//div[@data-test='course-item']")

        if not kurs_divleri:
            print(f"Sayfa {page_number}'de kurs bulunamadı. Muhtemelen son sayfaya ulaşıldı veya içerik kalmadı.")
            break

        for div in kurs_divleri:
            try:
                kurs_adi_element = div.find_element(By.CSS_SELECTOR, "h3[data-test='course-item-title']")
                kurs_adi = kurs_adi_element.text.strip()

                kurs_link_slug = kurs_adi.lower().replace(" ", "-").replace("(", "").replace(")", "").replace("&",
                                                                                                              "and").strip(
                    "-")
                kurs_link = f"https://www.techcareer.net/courses/{kurs_link_slug}"

                kurs_seviyesi = "Bilgi yok"
                try:
                    seviye_element = div.find_element(By.CSS_SELECTOR, "span[data-test='course-item-level']")
                    kurs_seviyesi = seviye_element.text.strip()
                except NoSuchElementException:
                    pass

                kurs_suresi = "Bilgi yok"
                try:
                    süre_element = div.find_element(By.CSS_SELECTOR, "span[data-test='course-item-total-time']")
                    kurs_suresi = süre_element.text.strip()
                except NoSuchElementException:
                    pass

                sertifika = "Bilgi yok"
                try:
                    sertifika_element = div.find_element(By.CSS_SELECTOR, "span[data-test='course-item-certificate']")
                    sertifika = sertifika_element.text.strip()
                except NoSuchElementException:
                    pass

                veriler.append({
                    "Kurs Adı": kurs_adi,
                    "Seviyesi": kurs_seviyesi,
                    "Süresi": kurs_suresi,
                    "Sertifika": sertifika,
                    "Link": kurs_link
                })

                print(f"✅ {kurs_adi} - Seviye: {kurs_seviyesi}, Süre: {kurs_suresi}, Sertifika: {sertifika}")

            except NoSuchElementException as e:
                print(f"Element bulunamadı, bu kurs atlanıyor: {e}")
                continue
            except Exception as e:
                print(f"Kurs verisi işlenirken hata oluştu: {e}")
                continue

        # --- Pagination Logic ---
        try:
            # Sayfadaki mevcut aktif sayfa numarası elementini alalım
            # Eğer bu elementi alamıyorsak, sayfa yapısı değişmiş veya yüklenmemiş olabilir.
            try:
                current_page_number_element = driver.find_element(By.CSS_SELECTOR,
                                                                  "a.MuiPaginationItem-page[aria-current='page']")
                current_page_text = current_page_number_element.text.strip()
            except NoSuchElementException:
                print("Aktif sayfa numarası elementi bulunamadı. Pagination sonlanıyor.")
                break

            # Sonraki sayfa butonunu aria-label ile buluyoruz
            # Bekleme süresini biraz artırdık ve butona odaklanmasını bekliyoruz.
            next_button = WebDriverWait(driver, 15).until(  # Artırılmış bekleme süresi
                EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Go to next page']"))
            )

            # Butonun devre dışı olup olmadığını kontrol et (son sayfa kontrolü)
            if "Mui-disabled" in next_button.get_attribute("class"):
                print("Sonraki sayfa butonu devre dışı (son sayfa). Tüm sayfalar toplandı.")
                break

                # Sonraki sayfaya tıklamadan önce URL'yi kontrol edelim
            # Eğer URL'de bir 'page=' parametresi varsa, bu parametrenin yeni değeriyle yüklenmesini bekleyebiliriz.
            # Örneğin, href="https://www.techcareer.net/courses?page=2"
            next_page_href = next_button.get_attribute("href")

            next_button.click()
            print(f"Sonraki sayfaya ({page_number + 1}) geçiliyor...")

            # URL'nin yeni sayfa numarasını içerecek şekilde değişmesini bekleyelim.
            # Bu, sayfanın tamamen yüklendiğinden emin olmak için daha güvenilir bir yoldur.
            expected_url_part = f"page={page_number + 1}"
            WebDriverWait(driver, 20).until(  # URL'nin değişmesi için daha uzun bekleme
                EC.url_contains(expected_url_part)
            )

            page_number += 1
            # Artık time.sleep() çok daha az gerekli, çünkü EC.url_contains zaten bekledi
            # Yine de küçük bir bekleme (0.5 saniye) bazen tarayıcının render etmesi için faydalı olabilir.
            time.sleep(1)

        except TimeoutException:
            print("Sonraki sayfa butonu bulunamadı veya tıklanamadı (Timeout). Tüm sayfalar toplandı.")
            break
        except NoSuchElementException:
            print("Sonraki sayfa butonu bulunamadı. Tüm sayfalar toplandı.")
            break
        except Exception as e:
            print(f"Pagination sırasında beklenmeyen bir hata oluştu: {e}")
            break

    # Excel'e yaz
    df = pd.DataFrame(veriler)
    excel_filename = "techcareer_kurslar.xlsx"

    try:
        df.to_excel(excel_filename, index=False)
        print(f"\n✅ {len(veriler)} kurs başarıyla Excel'e kaydedildi: '{os.path.abspath(excel_filename)}'")
    except PermissionError:
        print(f"❌ Hata: '{excel_filename}' dosyasına erişim engellendi.")
        print("Lütfen aşağıdaki nedenlerden birini kontrol edin:")
        print("1. Dosya başka bir programda (örn: Microsoft Excel) açık olabilir. Lütfen kapatın.")
        print(
            "2. Script'in bu dizine yazma izni olmayabilir. Farklı bir dizine kaydetmeyi deneyin veya izinleri kontrol edin.")
        print("3. Antivirüs yazılımınız dosyaya erişimi engelliyor olabilir.")
        try:
            alternative_filename = "techcareer_kurslar_yedek.xlsx"
            df.to_excel(alternative_filename, index=False)
            print(f"✅ Dosya '{excel_filename}' kaydedilemedi, ancak '{alternative_filename}' olarak kaydedildi.")
        except Exception as e:
            print(f"Yedek dosyayı kaydederken de hata oluştu: {e}")
    except Exception as e:
        print(f"Excel'e yazarken beklenmeyen bir hata oluştu: {e}")

except WebDriverException as e:
    print(f"❌ WebDriver başlatılırken veya kullanılırken bir hata oluştu: {e}")
    print("Lütfen ChromeDriver'ın doğru yolda olduğundan ve Chrome tarayıcınızla uyumlu olduğundan emin olun.")
    print("Ayrıca, Chrome tarayıcınızın güncel olduğundan emin olun.")
except Exception as e:
    print(f"Genel bir hata oluştu: {e}")
finally:
    # Tarayıcıyı kapat
    if driver:
        driver.quit()
        print("Tarayıcı kapatıldı.")