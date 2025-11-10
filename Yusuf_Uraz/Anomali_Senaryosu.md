Anomali Senaryosu: Enerji Hırsızlığı için Veri Manipülasyonu

Amacı ve Kapsamı

Bu anomali, bir saldırganın, şarj istasyonu (Charge Point - CP) ile Merkezi Yönetim Sistemi (Central System Management Software - CSMS) arasındaki iletişime sızarak, şarj oturumu sırasında tüketilen gerçek enerji miktarını içeren OCPP mesajlarını manipüle etmesini gösterir. Amaç, faturalandırma sistemine kasıtlı olarak daha düşük bir enerji tüketim verisi göndererek haksız kazanç sağlamaktır. Kapsam, OCPP “MeterValues” mesajlarının bütünlüğü ve faturalandırma sürecinin doğruluğudur.

Özet
Saldırgan, şarj istasyonunun internete bağlandığı yerel ağda bir "Araya Girme" (Man-in-the-Middle - MitM) saldırısı başlatır. Şarj istasyonunun periyodik olarak merkeze gönderdiği enerji tüketim verilerini “MeterValues.req” yakalar, içindeki tüketim değerini düşürür ve değiştirilmiş mesajı merkeze iletir. Sonuç olarak, kullanıcı tükettiği enerjiden daha azı için faturalandırılır ve şarj operatörü (CPO) zarara uğrar.

Hedef Varlıklar

 OCPP “MeterValues.req” mesajı
 Merkezi sistemdeki (CSMS) faturalandırma kaydı
 Şarj istasyonu ile merkezi sistem arasındaki iletişim kanalı

İlgili Zafiyetle

Şifresiz İletişim: İstasyon ve merkez arasında TLS (Transport Layer Security) kullanılmaması.
Veri Bütünlüğü Kontrolü Eksikliği: İletilen OCPP mesajlarının içeriğinin değiştirilip değiştirilmediğini doğrulayacak bir mekanizmanın (örn: dijital imza) olmaması.
Zayıf Ağ Güvenliği: Şarj istasyonunun bulunduğu yerel ağın (örn: halka açık Wi-Fi) güvensiz olması.

Tehdit Kategorisi

Tampering (Veri Değiştirme / Kurcalama): Aktif bir saldırı ile iletilen verinin içeriği değiştirilmektedir.
Information Disclosure (Bilgi Sızdırma): Saldırgan, kullanıcının ne kadar enerji tükettiği gibi hassas verileri de görmüş olur.

Saldırı Adımları

Konumlanma: Saldırgan, hedef şarj istasyonunun bulunduğu yerel ağa (örn: bir AVM'nin Wi-Fi ağına) bağlanır.
 Araya Girme (MitM): Saldırgan, `ettercap` veya `bettercap` gibi araçlar kullanarak bir ARP spoofing saldırısı başlatır ve şarj istasyonunun tüm internet trafiğini kendi bilgisayarı üzerinden geçmeye zorlar. Artık istasyon ile merkez (CSMS) arasındaki tüm iletişimi okuyabilir ve değiştirebilir.
Oturum Başlatma: Normal bir kullanıcı aracını şarja takar ve şarj oturumu başlar.
Veri Yakalama: Şarj istasyonu, OCPP protokolü gereği belirli aralıklarla (örn: her 5 dakikada bir) tüketilen toplam enerji miktarını bildiren bir “MeterValues.req” mesajı gönderir. Saldırgan bu mesajı yakalar.
 Örnek Orijinal Mesaj: `{"measurand": "Energy.Active.Import.Register", "value": "22500"}` (22.5 kWh tüketildi)
 Veri Manipülasyonu: Saldırgan, bu mesajın içindeki `value` değerini önceden belirlediği bir oranda (%25 daha az gibi) düşürür.
 Örnek Manipüle Edilmiş Mesaj:`{"measurand": "Energy.Active.Import.Register", "value": "16875"}` (Tüketim 16.875 kWh olarak değiştirildi)
 Değiştirilmiş Veriyi İletme:Saldırgan, manipüle ettiği bu mesajı sanki istasyondan geliyormuş gibi merkezi sisteme (CSMS) iletir.
 Süreci Tekrarlama:Saldırgan, şarj oturumu boyunca gelen tüm“MeterValues.req” mesajları için bu işlemi tekrarlar.
 Sonuç:Şarj oturumu bittiğinde, CSMS faturayı manipüle edilmiş, daha düşük veriler üzerinden hesaplar.

Tespit Yöntemleri

Güvenli İletişim Protokolleri (mTLS): İstasyon ve merkez arasında Karşılıklı Kimlik Doğrulama (Mutual TLS) zorunlu kılınırsa, saldırgan araya giremez çünkü geçerli bir istemci sertifikasına sahip değildir. Bu, saldırıyı en başından engeller.
Anomali Tespiti:Merkezi sistem, bir şarj oturumundaki tüketim verilerinin akışını analiz edebilir. Veride mantıksız sıçramalar veya beklenen tüketim eğrisinden sapmalar (örn: şarjın ortasında tüketimin aniden düşmesi) bir alarm üretebilir.


Etki ve Sonuçlar

Finansal Kayıp: Şarj istasyonu operatörü (CPO) doğrudan gelir kaybeder.
Veri Güvenilirliğinin Kaybı:Enerji talep planlaması için kullanılan veriler yanıltıcı hale gelir ve şebeke yönetimini olumsuz etkileyebilir.
Güven Kaybı:Sistemin suistimale açık olduğunun anlaşılması, kullanıcıların ve yatırımcıların sisteme olan güvenini sarsar.

