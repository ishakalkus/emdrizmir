#!/usr/bin/env python3
"""Konu sayfalarının gözden geçirilmiş metinleri (21 TR + 19 EN).

Konu sayfaları eski sitede kurum (ajans) tarafından yazılmıştı; hekimin
kendi metni değildir. HANDOFF.md gereği yanıltıcı ya da abartılı ifadeler
yumuşatıldı, tıbbi terim hataları ve yazım hataları düzeltildi. Her
değişiklik migration/content-changes.md'de listelidir.

İngilizce sayfalar eski sitede makine çevirisiydi ve tıbbi olarak yanlış
ifadeler içeriyordu ("delusions", "dissolution reactions" …); düzeltilmiş
Türkçe metnin sadık çevirisiyle değiştirildi.

Bu betik src/content/pages/<dil>/<slug>.md dosyalarının yalnızca gövdesini
ve `description` alanını yazar; diğer alanlara dokunmaz.
"""

import json
import re
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "src" / "content" / "pages"

TR = {
"aile-iliskileri": ("Aile içi iletişim sorunları, kuşak çatışması ve eşler arası sorunlar; aile bireylerinin birbirini daha sağlıklı biçimde anlamasına yönelik destek.", """
Aynı evi paylaştığımız insanlarla yaşadığımız sorunlar çok çeşitli olabilir.

Çocuklarımızla kuşak çatışmasından kaynaklı sorunlar yaşayabiliriz.

Eşimizle sayısız nedenle sorunlar yaşayabiliriz.

Tüm bunlar çoğu zaman iç içe geçmiştir ve ailedeki herkesi yıpratır. Çaresizlik ve tükenmişlik hissine neden olabilir.

Böyle durumlarda ani bir karar vermeden önce bir uzmandan destek almak yararlı olabilir.

Terapist, üçüncü bir göz olarak aile bireylerinin iletişimini engelleyen unsurları fark etmelerine, bakış açılarını gözden geçirmelerine ve sorunları birbirleriyle daha sağlıklı bir şekilde konuşabilmelerine yardımcı olmayı amaçlar.

İlgili: [Çift ve aile terapisi](/tr/cift-aile-terapisi/)
"""),
"ayrilik-kaygisi": ("Ayrılık kaygısı: değer verdiğimiz kişileri kaybetme ya da onlardan ayrılma kaygısının günlük yaşamı ve iş-okul performansını etkilemesi.", """
Anne, baba, kardeşimizi ya da değer verdiğimiz diğer kişileri kaybetme, onlardan birinden ayrılma kaygısı rutin hayatımızı etkiliyor, günlük yaşamımızı ve iş-okul performansımızı düşürüyorsa ayrılık kaygısından (ayrılık anksiyetesi) söz edilebilir.

Bu yoğun kaygının nedenlerini anlamak, kaygıyla baş etmenin önemli bir adımıdır. Bu süreçte bir ruh sağlığı uzmanından destek alınabilir.

İlgili: [Çocuk ve ergen terapisi](/tr/cocuk-ve-ergen-terapisi-/), [bireysel yetişkin psikoterapisi](/tr/bireysel-yetiskin-psikoterapisi/)
"""),
"cinsel-sorunlar": ("Cinsel işlev bozuklukları: erken ve geç boşalma, sertleşme güçlüğü, orgazm bozukluğu, düşük cinsel istek ve vajinismus hakkında bilgi.", """
Cinsel işlev bozuklukları kendi içinde; kişi istemediği hâlde **geç boşalma**, **sertleşme** sağlamada ya da sürdürmede güçlük, **kadında orgazm bozukluğu**, erkekte düşük cinsel istek bozukluğu, kişinin kendi isteğinden önce **erken boşalma** ve vajinismus gibi sorunlara ayrılmaktadır.

**Vajinismus**, genito-pelvik ağrı / içe girme bozukluğu olarak da bilinmektedir. Vajinaya girme sırasında, pelviste ya da cinsel organda yineleyici ağrı duyma hâlidir. Kasların aşırı gerilmesi ya da kasılması görülebilir.

**Erkekte ve kadında düşük cinsel istek bozukluğunda** ilgisizlik ya da az ilgi gösterme, cinsel isteğin az olması, karşılık vermeme gibi belirtiler görülebilir.

İlgili: [Bireysel yetişkin psikoterapisi](/tr/bireysel-yetiskin-psikoterapisi/), [çift ve aile terapisi](/tr/cift-aile-terapisi/)
"""),
"depresyon": ("Depresyon belirtileri: çökkün ve umutsuz duygudurum, ilgi ve zevk kaybı, uyku ve iştah değişiklikleri, enerji düşüklüğü, odaklanma güçlüğü.", """
Kişi günün büyük bir bölümünü çökkün, üzüntülü, umutsuz geçirir. Neredeyse bütün etkinliklere, aktivitelere, hobilere karşı ilgide azalma, zevk alamama durumu oluşur. Kilo ve uyku düzenlerinde bozulmalar görülebilir. Enerji düşüklüğü, bitkinlik, yavaşlama, odaklanmada güçlük çekme gibi belirtiler olabilir. Olumsuz düşünceye odaklanma (değersizim, güçsüzüm, çaresizim), intihar düşünceleri, planlama, eyleme geçme gibi durumlar oluşabilir. Hayatının genelinde işlevsellik alanlarında düşüş meydana gelebilir.

İntihar düşünceleriniz varsa beklemeyin: 112 Acil Çağrı Merkezi'ni arayın ya da en yakın acil servise başvurun.

İlgili: [Hamilelik süreci ve sonrası – depresyon](/tr/hamilelik-sureci-ve-sonrasi--depresyon/), [bireysel yetişkin psikoterapisi](/tr/bireysel-yetiskin-psikoterapisi/)
"""),
"davranis-bozukluklari": ("Davranım bozukluğu ile karşı olma / karşı gelme bozukluğu: saldırganlık, kural çiğneme, öfke ve tartışmacı tutum gibi belirtiler.", """
**Davranım bozukluğunda** insanlara ve hayvanlara karşı saldırganlık, eşyalara zarar verme, bilinçli olarak yangın çıkarma, hırsızlık yapma, kuralları büyük ölçüde çiğneme gibi belirtiler görülebilir.

Sık sık öfkeli olma, alınganlık gösterme, tartışma yaratma, kin besleme gibi belirtiler ise **karşı olma / karşı gelme bozukluğu** kapsamında değerlendirilir.

İlgili: [Çocuk ve ergen terapisi](/tr/cocuk-ve-ergen-terapisi-/)
"""),
"iliski-ve-evlilik-sorunlari": ("İlişki ve evlilik sorunları: iletişim güçlükleri, çatışma, öfke, cinsel sorunlar, evlilik öncesi danışmanlık ve boşanma süreçlerinde destek.", """
İletişim sorunları, öfke kontrolü, çatışma, uzlaşma, tartışma, mutsuzluk ve cinsel sorunlar gibi güçlükler ilişkiyi belirgin biçimde zorlamaya başladığında danışmanlık desteği alınabilir; evlilik öncesi danışmanlık da bu kapsamdadır. Evlendikten sonraki dönemde oluşan anne-baba-çocuk üçgeni sorunları, bağımlılık sorunları, anne ile baba arasındaki ilişkisel problemler ve boşanma gibi durumlarda da yardım alınabilir.

İlgili: [Çift ve aile terapisi](/tr/cift-aile-terapisi/)
"""),
"kisilik-bozukluklari": ("Kişilik bozuklukları: yatkınlık ve çevresel etkenlerle şekillenen bozukluklar; paranoid, borderline, narsisistik, çekingen ve diğer türler.", """
Doğuştan getirilen yatkınlıklar ve çevresel etkenlerle şekillenen bozukluk türleridir. Kişilik bozuklukları üç ana küme altında toplanır.

Paranoid, şizoid, şizotipal, antisosyal, borderline, histriyonik, narsisistik, çekingen, bağımlı ve obsesif kompulsif kişilik bozuklukları gibi geniş kapsamlı bir alandır. Genel olarak kişinin işlevselliğinde belirgin bir düşüş görülür ve belirtiler kişinin zamanının önemli bir bölümünü alır.

İlgili: [Bireysel yetişkin psikoterapisi](/tr/bireysel-yetiskin-psikoterapisi/)
"""),
"ders-basarisizligi-ve-sinav-kaygisi": ("Ergenlerde ders başarısızlığı, okul ve sınav kaygısı: belirtiler ve anne-baba-çocuk görüşmeleriyle yürütülen destek süreci.", """
Ergen bireylerde ders başarısıyla ilgili sorunlar ve okul kaygısı sık görülmektedir. Bununla ilgili anne-baba-çocuk görüşmeleri ve çocukla bire bir görüşmeler yapılır. Sınav kaygısı döneminde birey kaygılı, endişeli, depresif hissedebilir. İşlevsellikte düşüş, etkinliklere karşı ilgide azalma, sosyal ortamdan kaçınma davranışları görülebilir. Bu dönemde yardım alınabilir.

İlgili: [Çocuk ve ergen terapisi](/tr/cocuk-ve-ergen-terapisi-/), [okula uyum](/tr/okula-uyum/)
"""),
"hamilelik-sureci-ve-sonrasi--depresyon": ("Hamilelik ve doğum sonrası dönemde depresyon: hüzün, yorgunluk, enerji kaybı, uyku ve iştah değişiklikleri gibi belirtiler.", """
Kişinin hayatında hamilelik süresince ve doğum sonrası lohusalık döneminde fizyolojik, hormonal, psikolojik ve sosyal açıdan birçok alanda değişimler meydana gelir. Kişinin yatkınlığına göre bu süreç daha sorunsuz ya da daha zorlu geçebilir. Hüzün, duyarsızlık, yorgunluk, enerji kaybı, uyku ve iştah bozukluğu gibi belirtiler görülebilir.

İlgili: [Depresyon](/tr/depresyon/)
"""),
"okula-uyum": ("Okula uyum sorunları: arkadaş ve öğretmen ilişkilerinde güçlük, saldırganlık ve uyumsuzluk yaşayan öğrenciler için bilgi.", """
Arkadaşlarımızın bizi anlamadığını, değer vermediğini mi düşünüyoruz?

Öğretmenlerimizin davranışlarından rahatsız mı oluyoruz? Yoksa onlara karşı saldırgan mı davranıyoruz?

Kişiler arası ilişkilerde daha iyi olabiliriz; çevremizdeki insanlarla dengeli ilişkiler kurabiliriz. Bu konuda bir ruh sağlığı uzmanından destek alınabilir.

İlgili: [Çocuk ve ergen terapisi](/tr/cocuk-ve-ergen-terapisi-/), [ders başarısızlığı ve sınav kaygısı](/tr/ders-basarisizligi-ve-sinav-kaygisi/)
"""),
"is-yasamina-iliskin-sorunlar": ("İş yaşamına ilişkin sorunlar: ekip içi iletişim, çatışma, performans kaygısı, topluluk önünde konuşma ve kariyer konularında danışmanlık.", """
Kariyer danışmanlığı, ekip içi iletişim, çatışma, uzlaşma, performans kaygısı, topluluk önünde konuşamama, sunum yapamama, uyumlu çalışma, ilişki ve iletişim kurma gibi konularda danışmanlık alınabilmektedir.

İlgili: [Psikoterapi ve psikolojik danışmanlık](/tr/psikoterapi-ve-psikolojik-danismanlik-hizmetleri/)
"""),
"kaygi-bozukluklari": ("Kaygı bozuklukları: özgül fobi, sosyal fobi, panik bozukluk ve yaygın kaygı bozukluğunun belirtileri hakkında bilgi.", """
**Özgül fobi:** Özgül bir nesne ya da duruma karşı belirgin bir korku, kaygı duyma durumudur. Bu durumdan kaçınılır ve bu korku gerçek tehlikeye göre orantısız bir korkudur. Hayvan, uçak, deprem, yükseklik, çevresel durumlar, kan-iğne fobileri gibi nesnel ve durumsal örnekler verilebilir.

**Sosyal fobi:** Birden çok toplumsal durumda ya da başkaları tarafından gözleneceği, değerlendirileceği durumlarda kişinin yoğun kaygı ve korku duymasıdır. Kişi olumsuz olarak değerlendirilmekten korkar ve kaçınma davranışı sergiler. Orantısız bir kaygı ve korku durumu vardır. Sunum yapma, karşılıklı konuşma, tanımadık insanlarla karşılaşma gibi durumlarda görülebilir.

**Panik bozukluk:** Tekrarlayan panik atak olma durumudur. Yoğun bir korku, kaygı ve sıkıntıyla dakikalar içinde ortaya çıkan bir durumdur. Çarpıntı, terleme, titreme, göğüs ağrısı / sıkışması, baş dönmesi, uyuşma, ateş basması, öz denetimini yitirme korkusu, ölüm korkusu gibi belirtilerle karşımıza gelmektedir.

**Yaygın kaygı bozukluğu:** En az 6 aylık sürenin çoğunda genel durumlara ve etkinliklere (iş, okul, sosyal çevre, özel hayat, performans) karşı aşırı kaygı ve kuruntu hâlidir. Kişi bu kuruntuları kontrol altına almakta güçlük çeker. Huzursuzluk, gergin olma hâli, kolay yorulma, odaklanmada güçlük, kas gerginliği, kolay öfkelenme, uyku düzensizliği gibi belirtiler görülebilir.

İlgili: [Panik atak](/tr/panik-atak/), [sanal gerçeklik (VR) ile alıştırma tedavisi](/tr/sanal-gerceklik-vr-ile-alistirma--exposure-tedavisi/)
"""),
"obsesif--kompulsif-bozukluk": ("Obsesif kompulsif bozukluk (OKB): istenmeden gelen, sıkıntı veren düşünce ve imgeler (obsesyon) ile yineleyici eylemler (kompulsiyon).", """
Zorla ve istenmeden gelen, belirgin kaygı ve sıkıntıya neden olan yineleyici, sürekli düşünceler (obsesyon) ya da imgelerdir. Kişi düşünce ve imgeleri bastırmaya çalışsa da kontrol edemez. Bu takıntıya karşı yapmak zorunda hissettiği eylemlere (kompulsiyon) geçer. El yıkama, düzenleme, sürekli kontrol etme, dinsel sözler söyleme, sayı sayma gibi örnekler verilebilir. Düşünce ve eylemler kişinin oldukça zamanını alır ve işlevsellikte düşüş meydana gelir.

İlgili: [Bireysel yetişkin psikoterapisi](/tr/bireysel-yetiskin-psikoterapisi/)
"""),
"ofke-kontrolu": ("Öfke kontrolü: aile, iş ve toplum içinde yoğun öfke; öfkenin öğrenilmiş bir davranış olabileceği ve düşünce kalıplarıyla ilişkisi.", """
Bazılarımız aile, iş, arkadaş ortamında, trafikte, toplum içinde çok sinirli olabiliyoruz.

Öfke, tüm ilişkilerimizi, mutluluğumuzu, iş veya okul performansımızı etkileyebiliyor.

Öfke, küçük yaştan bu yana yaşadığımız ortam ve biriktirdiğimiz deneyimler sonucunda öğrenilmiş bir davranış olabilir.

Bu durumda düşüncelerimizi gözden geçirerek olaylara yeni bir pencereden bakabiliriz.

Düşüncelerimiz değiştikçe duygularımız ve davranışlarımız da değişebilir. Öfkeyle baş etmek öğrenilebilir bir beceridir; bu süreçte bir ruh sağlığı uzmanından destek alınabilir.

İlgili: [Stresle başa çıkma ve öfke kontrolü](/tr/stresle-basa-cikma-ve-ofke-kontrolu/)
"""),
"psikosomatik-bozukluklar": ("Psikosomatik bozukluklar: sıkıntı veren bedensel belirtiler, sağlıkla ilgili aşırı kaygı ve kaçınma davranışları hakkında bilgi.", """
Sıkıntı veren ve günlük yaşamı ciddi bir şekilde etkileyen, birden çok bedensel belirtiyle giden bir durumdur. Kişi sağlığıyla ilgili aşırı düzeyde kaygı, korku hisseder. Bedensel belirtileriyle ilgili orantısız ve sürekli düşüncelere kapılır. Sağlığıyla ilgili araştırmaya aşırı zaman harcar. Ağır bir hastalığı olduğunu ya da olacağını düşünür. Uygunsuz kaçınma davranışlarında bulunabilir.

Bedensel belirtilerin tıbbi bir nedeni olup olmadığının hekim tarafından değerlendirilmesi önemlidir.
"""),
"travma-sonrasi-stres-bozuklugu": ("Travma sonrası stres bozukluğu (TSSB): ölüm tehdidi, ağır yaralanma ya da cinsel saldırı gibi olayların ardından görülebilen belirtiler.", """
Gerçek ya da tehdit edici bir ölümle, ağır yaralanmayla ya da cinsel saldırıyla karşılaşmış ya da örseleyici (travmatik) bir olayı doğrudan yaşamış kişilerde görülebilir. Başkasının başına gelen olaya bire bir tanık olma ya da ailesinin, yakınlarının başına örseleyici olaylar geldiğini öğrenme gibi durumlarda da oluşabilir. Örseleyici olay, sıkıntı veren anılara ve düşlere dönüşebilir. Olay yeniden oluyormuş gibi hissedilen çözülme (dissosiyatif) tepkileri olabilir. Olayla bağlantılı kişi ve durumlarla karşılaşıldığında yoğun bir sıkıntı görülebilir.

EMDR, travma sonrası stres bozukluğunda uluslararası tedavi kılavuzlarında yer alan yöntemlerden biridir ([EMDR nedir](/#emdr)). Tedavi planı, yüz yüze değerlendirme sonrasında kişiye özel olarak belirlenir.

İlgili: [Bireysel yetişkin psikoterapisi](/tr/bireysel-yetiskin-psikoterapisi/)
"""),
"yeme-bozukluklari": ("Yeme bozuklukları: anoreksiya nervoza ve bulimiya nervozanın belirtileri hakkında bilgi.", """
Yeme bozuklukları kendi arasında ayrı başlıklara ayrılmaktadır.

**Anoreksiya nervoza:** Düşük bir vücut ağırlığının olması, enerji alımını kısıtlama, kilo almaktan korkma, vücut biçimine ve kiloya orantısız bir önem yükleme gibi belirtiler görülebilir.

**Bulimiya nervoza:** Yineleyici tıkanırcasına yeme dönemleri, yemek yemeyi durduramama, kilo almamak için kendini kusturma, aşırı spor yapma gibi belirtiler görülebilir.
"""),
"stresle-basa-cikma-ve-ofke-kontrolu": ("Stresle başa çıkma ve öfke kontrolü: stres ve öfke orantısız hâle geldiğinde görülebilen belirtiler ve destek.", """
Öfke ve stres, topluma ve çevrenize göre orantısız bir hâldeyse destek alabilirsiniz. Stresle baş edemediğinizi düşünebilir, depresif hissedebilirsiniz. Etkinliklere karşı ilginizde azalma, kaçınma davranışı sergileme gibi belirtiler olabilir. Öfke hissettiğiniz durumlarda aşırı tepki verme, şiddete yönelme gibi belirtilerde yardım alabilirsiniz.

İlgili: [Öfke kontrolü](/tr/ofke-kontrolu/)
"""),
"panik-atak": ("Panik atak: aniden gelişen yoğun kaygı atağı; göğüs ağrısı, terleme, hızlı nefes alma gibi belirtiler ve ne zaman destek alınabileceği.", """
Panik atak, bir anda gelişen ve yoğun bir şekilde ortaya çıkan kaygı atağı olarak kendini gösterebilir.

Aniden göğsümüzde ağrı, terleme, sık sık ve kuvvetli nefes alma, o anı atlatamayacakmış gibi düşüncelere kapılıyorsak panik atak geçiriyor olabiliriz. Göğüs ağrısı gibi belirtilerin kalp ya da başka bir tıbbi nedene bağlı olmadığından emin olmak için önce hekim değerlendirmesi gerekir.

Ataklar sıklaşıyor ya da günlük yaşamı kısıtlamaya başlıyorsa bir ruh sağlığı uzmanından destek almak yararlı olabilir.

İlgili: [Kaygı bozuklukları](/tr/kaygi-bozukluklari/), [sanal gerçeklik (VR) ile alıştırma tedavisi](/tr/sanal-gerceklik-vr-ile-alistirma--exposure-tedavisi/)
"""),
"uyum-problemleri": ("Uyum sorunları: iş, ev, evlilik ve sosyal ortamda yaşanan uyumsuzluk, çatışma ve iletişim güçlükleri.", """
Uyum gerektiren durum ve alanlarınızda belirgin uyumsuzluk, tartışma, çatışma, öfke ya da iletişimsizlik varsa yardım alınabilir. İş hayatı, ev hayatı, evlilik süreci, sosyal ortam gibi alanlarda uyumsuzluk nedeniyle huzursuzluk, kaygı, endişe ve kaçınma gibi belirtiler görülebilir.

İlgili: [Psikoterapi ve psikolojik danışmanlık](/tr/psikoterapi-ve-psikolojik-danismanlik-hizmetleri/)
"""),
"yas-sureci": ("Yas süreci: sevilen birinin kaybının ardından gelişen doğal süreç, belirtileri ve ne zaman destek alınabileceği.", """
Yas, kişinin sevdiği yakınını kaybettikten sonra gelişen doğal bir süreçtir. Bu sürecin evreleri vardır. Kişinin kaybettiği yakınıyla ilişkisi ve ölümün biçimi, yasın etkisini ve seyrini değiştirebilir. Öfke, depresif belirtiler, kızgınlık, ölümü inkâr etme, bedensel belirtiler, karamsarlık, çaresizlik, kabul edememe, sorgulama, odaklanamama, kaçınma gibi belirtiler görülebilir. Bu süreç hayatın geneline yayılıyor, uzun süre devam ediyor ve işlevsellikte azalmaya yol açıyorsa danışmanlık desteği alınabilir.
"""),
}

EN = {
"anxiety-disorders": ("Anxiety disorders: information on the symptoms of specific phobia, social phobia, panic disorder and generalised anxiety disorder.", """
**Specific phobia:** a marked fear or anxiety about a particular object or situation. The object or situation is avoided, and the fear is out of proportion to the actual danger. Examples include animals, flying, earthquakes, heights, certain environments, and blood or needles.

**Social phobia:** intense anxiety and fear in one or more social situations, or in situations where the person may be observed or judged by others. The person fears being judged negatively and avoids such situations; the anxiety and fear are out of proportion. It can occur, for example, when giving a presentation, having a conversation or meeting unfamiliar people.

**Panic disorder:** recurrent panic attacks – episodes of intense fear, anxiety and distress that build up within minutes. They present with symptoms such as palpitations, sweating, trembling, chest pain or tightness, dizziness, numbness, hot flushes, fear of losing control and fear of dying.

**Generalised anxiety disorder:** excessive anxiety and worry, on most days for at least six months, about everyday matters and activities (work, school, social life, private life, performance). The person finds it hard to control these worries. Symptoms such as restlessness, feeling on edge, being easily tired, difficulty concentrating, muscle tension, irritability and sleep problems may occur.

Related: [panic attack](/en/panic-attack/), [virtual reality exposure therapy](/en/virtual-reality-exposure-therapy/)
"""),
"adaptation-problems": ("Adaptation problems: disharmony, conflict and communication difficulties at work, at home, in a marriage or in social settings.", """
Help can be sought when there is marked disharmony, argument, conflict, anger or a breakdown in communication in the situations and areas of life that require adjustment. Restlessness, anxiety, worry and avoidance may appear as a result of disharmony at work, at home, in a marriage or in social settings.

Related: [psychotherapy and psychological counselling](/en/psychotherapy-and-psychological-counselling/)
"""),
"anger-management": ("Anger management: intense anger at home, at work or in public; anger as a learned behaviour and its link with patterns of thinking.", """
Some of us can become very angry within the family, at work, among friends, in traffic or in public.

Anger can affect all of our relationships, our happiness, and our performance at work or school.

Anger may be a behaviour learned through the environment we have grown up in and the experiences we have gathered since childhood.

In that case, by reconsidering our thoughts, we can look at events from a new perspective.

As our thoughts change, our feelings and behaviour can change too. Coping with anger is a skill that can be learned, and support from a mental health professional can help along the way.

Related: [coping with stress and anger management](/en/coping-with-stress-and-anger-management/)
"""),
"coping-with-stress-and-anger-management": ("Coping with stress and anger: when stress or anger feel out of proportion, with symptoms such as low mood, avoidance or overreacting.", """
If your anger or stress feels out of proportion to your surroundings, you can seek support. You may feel that you cannot cope with stress, or you may feel low. Symptoms may include a loss of interest in activities and avoidance. When you feel angry, you can also seek help for reactions such as overreacting or turning to violence.

Related: [anger management](/en/anger-management/)
"""),
"course-failure-and-exam-anxiety": ("Poor school performance and exam anxiety in adolescents: symptoms, and support through parent–child and one-to-one sessions.", """
Difficulties with schoolwork and school-related anxiety are common among adolescents. In this area, sessions are held with the parents and child together, as well as one-to-one with the child. During periods of exam anxiety, a young person may feel anxious, worried and low. Reduced functioning, loss of interest in activities and withdrawal from social situations may be seen. Help can be sought during this time.

Related: [child and adolescent therapy](/en/child-and-adolescent-therapy/)
"""),
"eating-disorders": ("Eating disorders: information on the symptoms of anorexia nervosa and bulimia nervosa.", """
Eating disorders are divided into several types.

**Anorexia nervosa:** symptoms may include low body weight, restricted energy intake, fear of gaining weight, and giving disproportionate importance to body shape and weight.

**Bulimia nervosa:** symptoms may include recurrent episodes of binge eating, feeling unable to stop eating, and self-induced vomiting or excessive exercise to avoid gaining weight.
"""),
"problems-regarding-business-life": ("Problems at work: counselling for team communication, conflict, performance anxiety, public speaking and career questions.", """
Counselling is available for issues such as career questions, communication within a team, conflict and reconciliation, performance anxiety, difficulty speaking in public or giving presentations, working in harmony with others, and building relationships and communication.

Related: [psychotherapy and psychological counselling](/en/psychotherapy-and-psychological-counselling/)
"""),
"obsessive-compulsive-disorder": ("Obsessive-compulsive disorder (OCD): intrusive, distressing thoughts and images (obsessions) and repetitive acts (compulsions).", """
Obsessions are recurrent, persistent thoughts or images that are intrusive and unwanted and cause marked anxiety and distress. Although the person tries to suppress these thoughts or images, they cannot control them. They then turn to actions (compulsions) that they feel driven to perform in response to the obsession – for example hand washing, arranging, repeated checking, saying religious phrases or counting. The thoughts and actions take up a great deal of time, and everyday functioning declines.

Related: [individual adult psychotherapy](/en/individual-adult-psychotherapy/)
"""),
"separation-anxiety": ("Separation anxiety: when fear of losing or being separated from people we care about affects daily life and performance at work or school.", """
If the fear of losing, or being separated from, our mother, father, siblings or other people we care about affects our routine, our daily life and our performance at work or school, this may be separation anxiety.

Understanding the reasons behind this intense anxiety is an important step in coping with it, and support from a mental health professional can help along the way.

Related: [child and adolescent therapy](/en/child-and-adolescent-therapy/), [individual adult psychotherapy](/en/individual-adult-psychotherapy/)
"""),
"family-relations": ("Family relations: communication problems, generational conflict and difficulties between partners; support to help family members understand each other.", """
The problems we have with the people we share a home with can take many forms.

We may have problems with our children due to generational conflict.

We may have problems with our partner for all kinds of reasons.

All of this is often intertwined and wears down everyone in the family. It can lead to feelings of helplessness and burnout.

In such situations, it can help to seek support from a professional before making any sudden decisions.

Acting as a third eye, the therapist aims to help family members notice what is blocking their communication, reconsider their points of view, and talk about their problems with one another in a healthier way.

Related: [couple and family therapy](/en/couple-and-family-therapy/)
"""),
"post-traumatic-stress-disorder": ("Post-traumatic stress disorder (PTSD): symptoms that can follow events such as threatened death, serious injury or sexual assault.", """
PTSD can develop in people who have been exposed to actual or threatened death, serious injury or sexual violence, or who have directly experienced another traumatic event. It can also develop after witnessing such an event happen to someone else, or on learning that a traumatic event has happened to a family member or someone close. The traumatic event may return as distressing memories and dreams. There may be dissociative reactions in which the person feels as if the event were happening again. Intense distress may be felt when facing people or situations connected with the event.

EMDR is one of the methods included in international treatment guidelines for post-traumatic stress disorder ([what is EMDR](/en/#emdr)). The treatment plan is decided individually after a face-to-face assessment.

Related: [individual adult psychotherapy](/en/individual-adult-psychotherapy/)
"""),
"relationship-and-marriage-problems": ("Relationship and marriage problems: communication difficulties, conflict, anger, sexual problems, premarital counselling and divorce.", """
Counselling can be sought when difficulties such as communication problems, anger, conflict, reconciliation, arguments, unhappiness or sexual problems begin to put a clear strain on the relationship; premarital counselling is also available. After marriage, help can also be sought for problems in the mother–father–child triangle, addiction, difficulties in the relationship between the parents, and divorce.

Related: [couple and family therapy](/en/couple-and-family-therapy/)
"""),
"panic-attack": ("Panic attack: a sudden, intense anxiety attack with symptoms such as chest pain, sweating and rapid breathing, and when to seek support.", """
A panic attack can present as an anxiety attack that comes on suddenly and intensely.

If we suddenly have chest pain, sweating, rapid and heavy breathing, and feel as if we will not get through the moment, we may be having a panic attack. A medical assessment is needed first to make sure that symptoms such as chest pain are not caused by the heart or another physical condition.

If attacks become more frequent or begin to limit daily life, support from a mental health professional can be helpful.

Related: [anxiety disorders](/en/anxiety-disorders/), [virtual reality exposure therapy](/en/virtual-reality-exposure-therapy/)
"""),
"personality-disorder": ("Personality disorders: patterns shaped by predisposition and environment, including paranoid, borderline, narcissistic and avoidant types.", """
Personality disorders are shaped by inborn predispositions and environmental factors. They are grouped into three main clusters.

The field is broad and includes paranoid, schizoid, schizotypal, antisocial, borderline, histrionic, narcissistic, avoidant, dependent and obsessive-compulsive personality disorders. In general, the person’s functioning is markedly reduced and the symptoms take up a large part of their time.

Related: [individual adult psychotherapy](/en/individual-adult-psychotherapy/)
"""),
"sexual-problems": ("Sexual dysfunctions: premature and delayed ejaculation, erectile difficulties, orgasmic disorder, low sexual desire and vaginismus.", """
Sexual dysfunctions include problems such as **delayed ejaculation** when the person does not want a delay, difficulty getting or keeping an **erection**, **female orgasmic disorder**, low sexual desire in men, **premature ejaculation** before the person wishes, and vaginismus.

**Vaginismus**, also known as genito-pelvic pain / penetration disorder, is recurrent pain in the vagina, pelvis or genitals during penetration. Marked tensing or tightening of the muscles may occur.

In **low sexual desire disorder in men and women**, symptoms such as lack of interest or little interest, low sexual desire and not responding may be seen.

Related: [individual adult psychotherapy](/en/individual-adult-psychotherapy/), [couple and family therapy](/en/couple-and-family-therapy/)
"""),
"psychosomatic-disorders": ("Psychosomatic disorders: distressing physical symptoms, excessive worry about health and avoidance behaviour.", """
This is a condition with several distressing physical symptoms that seriously affect daily life. The person feels excessive anxiety and fear about their health. They have disproportionate and persistent thoughts about their physical symptoms and spend a great deal of time researching their health. They believe that they have, or will develop, a serious illness, and may avoid situations inappropriately.

It is important that a doctor assesses whether the physical symptoms have a medical cause.
"""),
"the-pregnancy-process-and-its-consequences---depression": ("Depression during pregnancy and after birth: sadness, fatigue, loss of energy, and changes in sleep and appetite.", """
During pregnancy and in the period after birth, physiological, hormonal, psychological and social changes take place in many areas of a person’s life. Depending on the person’s predisposition, this period may go more smoothly or be more difficult. Symptoms such as sadness, emotional numbness, fatigue, loss of energy, and disturbed sleep and appetite may be seen.
"""),
"the-mourning-process": ("The grieving process: a natural response to losing a loved one, its symptoms, and when support can help.", """
Grief is a natural process that follows the loss of someone we love, and it has stages. The relationship with the person who died and the circumstances of the death can shape its impact and course. Symptoms such as anger, low mood, irritability, denial of the death, physical symptoms, pessimism, helplessness, difficulty accepting the loss, questioning, difficulty concentrating and avoidance may be seen. If grief spreads to all areas of life, continues for a long time and reduces functioning, counselling support can be sought.
"""),
"behaviour-disorders": ("Conduct disorder and oppositional defiant disorder: symptoms such as aggression, rule-breaking, anger and argumentativeness.", """
In **conduct disorder**, symptoms may include aggression towards people and animals, damaging property, deliberately setting fires, stealing and serious rule-breaking.

Symptoms such as frequent anger, touchiness, arguing and holding grudges are assessed under **oppositional defiant disorder**.

Related: [child and adolescent therapy](/en/child-and-adolescent-therapy/)
"""),
}


def apply(lang, table):
    for slug, (description, body) in table.items():
        assert len(description) <= 170, (lang, slug, len(description))
        p = OUT / lang / f"{slug}.md"
        text = p.read_text(encoding="utf-8")
        m = re.match(r"---\n(.*?)\n---\n", text, re.S)
        assert m, p
        fm = m.group(1)
        fm = re.sub(r'^description: .*$', "description: " + json.dumps(description, ensure_ascii=False), fm, flags=re.M)
        p.write_text(f"---\n{fm}\n---\n\n{body.strip()}\n", encoding="utf-8")
    print(lang, len(table))


if __name__ == "__main__":
    apply("tr", TR)
    apply("en", EN)
