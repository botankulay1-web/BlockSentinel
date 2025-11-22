import time

# --- 1. SİSTEM BİLEŞENLERİ VE DURUM DEĞİŞKENLERİ ---
# Varsayılan değerler
CAN_STATUS = "SAĞLAM"
DARBE_SIDDETI = "DÜŞÜK"

# Kritik Modül Durumları (Fail-Safe: Kontaktör Kapalı, Kilit Kapalı)
KONTAKTOR_DURUMU = "KAPALI"  # Yüksek voltaj anahtarı
KILIT_DURUMU = "KİLİTLİ"    # Kapı kilit durumu

# --- 2. FONKSİYONLAR ---

def sensor_tetikle(darbe="DÜŞÜK", can_hata=False):
    """Kaza durumunu ve CAN Bus arızasını ayarlar."""
    global DARBE_SIDDETI, CAN_STATUS
    DARBE_SIDDETI = darbe
    
    if can_hata:
        CAN_STATUS = "KOPUK (ANOMALİ)"
    else:
        CAN_STATUS = "SAĞLAM"
    
    print("\n--- KAZA SİNYALİ GÖNDERİLİYOR ---")
    print(f"   [Sensör]: Darbe Şiddeti -> {DARBE_SIDDETI}")
    print(f"   [CAN Hattı]: Durum -> {CAN_STATUS}")
    time.sleep(0.5)

def iletisim_kopyala(komut):
    """CAN Bus üzerinden komut iletimini simüle eder."""
    if CAN_STATUS == "SAĞLAM":
        print(f"   [CAN Bus]: Komut Başarılı -> '{komut}'")
        return True
    else:
        print(f"   [CAN Bus]: Komut BAŞARISIZ! Hattı KOPUK.")
        return False

def bms_ecu_tepki(komut):
    """BMS'nin (Batarya Yönetimi) komuta tepkisini simüle eder."""
    global KONTAKTOR_DURUMU
    
    if komut:
        # Komut başarılı ulaştıysa (SAĞLAM iletişim)
        if komut == "ACİL_KES":
            KONTAKTOR_DURUMU = "AÇIK (Güvenli)"
            print("   [BMS ECU]: ACİL KES komutu alındı. Kontaktör AÇILDI.")
            return True
    
    # Komut ulaşmadıysa veya yanlışsa (KOPUK iletişim)
    print("   [BMS ECU]: ACİL KES komutu ALINAMADI. Kontaktör KAPALI kalıyor (Fail-Safe).")
    return False

def kilit_ecu_tepki(komut):
    """Kapı Kilit ECU'sunun komuta tepkisini simüle eder."""
    global KILIT_DURUMU
    
    if komut:
        # Komut başarılı ulaştıysa (SAĞLAM iletişim)
        if komut == "ACİL_AÇ":
            KILIT_DURUMU = "AÇIK (Tahliye Mümkün)"
            print("   [Kilit ECU]: ACİL AÇ komutu alındı. Kapılar AÇILDI.")
            return True

    # Komut ulaşmadıysa veya yanlışsa (KOPUK iletişim)
    print("   [Kilit ECU]: ACİL AÇ komutu ALINAMADI. Kapılar KİLİTLİ kalıyor (Fail-Safe).")
    return False

def simule_et(senaryo_adi, can_arizasi=False):
    """Tüm simülasyon akışını yönetir."""
    print(f"\n=======================================================")
    print(f"🚀 SENARYO BAŞLADI: {senaryo_adi}")
    print(f"=======================================================")
    
    # Kaza durumunu ayarla
    sensor_tetikle("YÜKSEK", can_hata=can_arizasi)
    time.sleep(1)

    # --- 3. KRİTİK KOMUTLARIN GÖNDERİLMESİ ---
    
    # 1. BMS Komutu
    print("\n[ADIM 1]: Batarya Kontaktör Kesme Komutu")
    bms_komut_basarili = iletisim_kopyala("ACİL_KES")
    
    if bms_komut_basarili:
        bms_ecu_tepki("ACİL_KES")
    else:
        bms_ecu_tepki(None) # Komut yoksa None gönder
    time.sleep(1)

    # 2. Kapı Kilidi Komutu
    print("\n[ADIM 2]: Kapı Kilidi Açma Komutu")
    kilit_komut_basarili = iletisim_kopyala("ACİL_AÇ")
    
    if kilit_komut_basarili:
        kilit_ecu_tepki("ACİL_AÇ")
    else:
        kilit_ecu_tepki(None) # Komut yoksa None gönder
    time.sleep(1)

    # --- 4. SONUÇ RAPORU ---
    print("\n-------------------------------------------------------")
    print("             SİMÜLASYON SONUÇ RAPORU")
    print("-------------------------------------------------------")
    print(f"➡️ CAN Bus Hattı Durumu: {CAN_STATUS}")
    print(f"➡️ Batarya Kontaktör Durumu: {KONTAKTOR_DURUMU}")
    print(f"➡️ Kapı Kilit Durumu: {KILIT_DURUMU}")
    
    if KONTAKTOR_DURUMU == "KAPALI" or KILIT_DURUMU == "KİLİTLİ":
        print("\n⚠️ KRİTİK HATA ZİNCİRİ: CAN Kopması nedeniyle güvenlik sistemleri DEVRE DIŞI kaldı!")
        if KONTAKTOR_DURUMU == "KAPALI":
             print("   - YÜKSEK RİSK: Batarya devrede, termal kaçak (yangın) riski var.")
        if KILIT_DURUMU == "KİLİTLİ":
             print("   - YÜKSEK RİSK: Tahliye (Kurtarma) Engellendi.")
    else:
        print("\n✅ SİSTEM GÜVENLİĞİ: Tüm acil durum protokolleri başarıyla uygulandı.")
    print("-------------------------------------------------------")

# --- 5. ANA ÇALIŞTIRMA BLOĞU ---

# Simülasyon 1: NORMAL Senaryo (CAN Sağlam)
simule_et("NORMAL ÇALIŞMA: CAN Hattı SAĞLAM", can_arizasi=False)

# Simülasyon 2: ANOMALİ Senaryo (CAN Kopuk)
simule_et("ANOMALİ: CAN Hattı KOPUK (BUS-OFF)", can_arizasi=True)