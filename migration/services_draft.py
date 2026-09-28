#!/usr/bin/env python3
"""Hizmet sayfalarının ilk taslakları (6 hizmet × 4 dil).

Eski sitede hizmet sayfaları boştu; bu metinler yeni yazıldı ve yayından
önce hekimin onayını bekliyor (Yönetmelik md. 5/1/b: sağlık hizmetine
ilişkin bilgilendirmeyi yetkili sağlık meslek mensubu yapar). Onaylanan
sayfada `draft` satırı silinir.

Yazım ilkeleri (Yönetmelik RG 12/11/2025, 33075, md. 5):
  - tedavi garantisi ya da kanıtlanmamış iddia yok (5/1/ç),
  - hastayı hekime yönlendiren çağrı yok, ör. "hemen randevu alın" (5/1/f, g),
  - üstünlük ifadesi yok (5/1/h), ücret yok (5/1/m),
  - sonuçların kişiden kişiye değiştiği açıkça yazılır.

Bir kez çalıştırılır; var olan dosyanın üzerine yazmaz.
"""

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "src" / "content" / "pages"

DRAFT = {
    "tr": "Yeni yazılan hizmet metni; yayından önce hekim onayı gerekiyor (Yönetmelik md. 5/1/b).",
    "xx": "Yeni yazılan hizmet metni ve çevirisi; yayından önce hekim onayı gerekiyor (Yönetmelik md. 5/1/b). Çeviri, dili bilen biri tarafından okunmalı.",
}
ONLINE = " Uzaktan sağlık hizmeti yetkisi ayrıca teyit edilmeli (DEPLOY.md)."

# (grup, {dil: (slug, başlık, açıklama, gövde)})
PAGES = [
    ("bireysel-yetiskin-psikoterapisi", {
        "tr": ("bireysel-yetiskin-psikoterapisi", "Bireysel Yetişkin Psikoterapisi",
               "Bireysel yetişkin psikoterapisi: değerlendirme, hedeflerin birlikte belirlenmesi ve EMDR, psikodinamik terapi, BDT gibi yöntemlerle bire bir görüşmeler.",
               """Bireysel yetişkin psikoterapisi, danışan ile terapistin bire bir ve düzenli aralıklarla yaptığı görüşmelerden oluşur. Amaç, kişinin yaşadığı zorlukları anlamlandırmak, bunlarla baş etme yollarını geliştirmek ve gündelik yaşamdaki işlevselliğini desteklemektir.

## Süreç nasıl işler?

İlk görüşmelerde yakınmalar, bunların ne zamandır sürdüğü, kişinin yaşam öyküsü ve beklentileri değerlendirilir. Psikiyatri uzmanı hekim, gerekiyorsa tıbbi değerlendirmeyi de bu aşamada yapar. Değerlendirmenin ardından hedefler ve kullanılacak yöntem danışanla birlikte belirlenir. Görüşmelerin sıklığı ve süresi kişiye ve hedeflere göre değişir.

## Kullanılan yöntemler

- **EMDR** (Göz Hareketleriyle Duyarsızlaştırma ve Yeniden İşleme)
- **Psikodinamik psikoterapi**
- **Bilişsel davranışçı terapi**
- **Kabul ve adanmışlık terapisi**

Hangi yöntemin uygun olduğu ve yöntemlerin birlikte kullanılıp kullanılmayacağı, değerlendirme sonrasında kişiye özel olarak kararlaştırılır.

## Hangi konularda?

[Kaygı](/tr/kaygi-bozukluklari/) ve [panik](/tr/panik-atak/) yakınmaları, [travmatik yaşantıların etkileri](/tr/travma-sonrasi-stres-bozuklugu/), [depresif duygudurum](/tr/depresyon/), [ilişkilerde](/tr/iliski-ve-evlilik-sorunlari/) ve [iş yaşamında](/tr/is-yasamina-iliskin-sorunlar/) yaşanan güçlükler gibi pek çok konu bireysel psikoterapide ele alınabilir. Her kişinin süreci farklıdır; süre ve sonuç kişiden kişiye değişir."""),
        "en": ("individual-adult-psychotherapy", "Individual adult psychotherapy",
               "Individual adult psychotherapy in İzmir: an initial assessment, goals agreed together, and one-to-one sessions using EMDR, psychodynamic therapy or CBT.",
               """Individual adult psychotherapy consists of regular one-to-one sessions between the client and the therapist. Its aim is to make sense of the difficulties the person is facing, to develop ways of coping with them and to support day-to-day functioning.

## How does it work?

The first sessions explore the presenting concerns, how long they have lasted, the person’s life history and their expectations. Where needed, the psychiatrist also carries out a medical assessment at this stage. After the assessment, goals and methods are agreed together with the client. The frequency and length of sessions vary with the person and the goals.

## Methods used

- **EMDR** (Eye Movement Desensitisation and Reprocessing)
- **Psychodynamic psychotherapy**
- **Cognitive behavioural therapy**
- **Acceptance and commitment therapy**

Which method is suitable, and whether methods are combined, is decided individually after the assessment.

## Which concerns?

Many concerns can be addressed in individual psychotherapy, such as [anxiety](/en/anxiety-disorders/) and [panic](/en/panic-attack/), the effects of [traumatic experiences](/en/post-traumatic-stress-disorder/), low mood, and difficulties in [relationships](/en/relationship-and-marriage-problems/) or [working life](/en/problems-regarding-business-life/). Every person’s process is different; duration and outcome vary from person to person."""),
        "de": ("bireysel-yetiskin-psikoterapisi", "Einzelpsychotherapie für Erwachsene",
               "Einzelpsychotherapie für Erwachsene in İzmir: Abklärung, gemeinsam festgelegte Ziele und Einzelsitzungen mit EMDR, psychodynamischer Therapie oder KVT.",
               """Die Einzelpsychotherapie für Erwachsene besteht aus regelmäßigen Einzelgesprächen mit der Therapeutin oder dem Therapeuten. Ziel ist es, die Schwierigkeiten, mit denen jemand konfrontiert ist, zu verstehen, Wege des Umgangs damit zu entwickeln und die Bewältigung des Alltags zu unterstützen.

## Wie läuft sie ab?

In den ersten Gesprächen werden die Beschwerden, ihre Dauer, die Lebensgeschichte und die Erwartungen besprochen. Bei Bedarf nimmt der Facharzt für Psychiatrie in dieser Phase auch eine ärztliche Abklärung vor. Anschließend werden Ziele und Methode gemeinsam festgelegt. Häufigkeit und Dauer der Sitzungen richten sich nach der Person und den Zielen.

## Methoden

- **EMDR** (Eye Movement Desensitization and Reprocessing)
- **Psychodynamische Psychotherapie**
- **Kognitive Verhaltenstherapie**
- **Akzeptanz- und Commitment-Therapie**

Welche Methode geeignet ist und ob Methoden kombiniert werden, wird nach der Abklärung individuell entschieden.

## Welche Anliegen?

Viele Anliegen können in der Einzelpsychotherapie bearbeitet werden, etwa Angst- und Panikbeschwerden, die Folgen belastender Erlebnisse, gedrückte Stimmung sowie Schwierigkeiten in Beziehungen oder im Berufsleben. Jeder Verlauf ist anders; Dauer und Ergebnis sind von Person zu Person verschieden."""),
        "fr": ("psychotherapie-individuelle-adulte", "Psychothérapie individuelle de l’adulte",
               "Psychothérapie individuelle de l’adulte à İzmir : évaluation, objectifs définis ensemble et séances individuelles (EMDR, thérapie psychodynamique, TCC).",
               """La psychothérapie individuelle de l’adulte repose sur des séances régulières en tête-à-tête avec le ou la thérapeute. Elle vise à donner du sens aux difficultés rencontrées, à développer des moyens d’y faire face et à soutenir le fonctionnement au quotidien.

## Comment se déroule-t-elle ?

Les premières séances permettent d’explorer les motifs de consultation, leur durée, l’histoire de vie et les attentes de la personne. Si nécessaire, le psychiatre réalise également une évaluation médicale à ce stade. Les objectifs et la méthode sont ensuite définis ensemble. La fréquence et la durée des séances varient selon la personne et les objectifs.

## Méthodes utilisées

- **EMDR** (désensibilisation et retraitement par les mouvements oculaires)
- **Psychothérapie psychodynamique**
- **Thérapie cognitive et comportementale**
- **Thérapie d’acceptation et d’engagement**

Le choix de la méthode, et la combinaison éventuelle de plusieurs approches, sont décidés individuellement après l’évaluation.

## Pour quelles difficultés ?

De nombreuses difficultés peuvent être abordées en psychothérapie individuelle : anxiété et crises de panique, conséquences d’expériences traumatiques, humeur dépressive, difficultés relationnelles ou professionnelles. Chaque parcours est différent ; la durée et les résultats varient d’une personne à l’autre."""),
    }),
    ("cift-aile-terapisi", {
        "tr": ("cift-aile-terapisi", "Çift ve Aile Terapisi",
               "Çift ve aile terapisi: ilişkide tekrar eden döngüleri ve iletişim güçlüklerini birlikte ele alan görüşmeler. İzmir, Güzelbahçe.",
               """Çift ve aile terapisi, ilişkideki sorunları tek bir kişinin sorunu olarak değil, kişiler arasındaki etkileşimin bir parçası olarak ele alır. Görüşmelere çiftin ya da ailenin birden fazla üyesi birlikte katılır; gerektiğinde bireysel görüşmeler de yapılır.

## Neler üzerinde çalışılır?

İlişki içinde tekrar eden çatışma döngüleri, iletişim güçlükleri, güven sorunları, ebeveynlik ve aile içi rol değişiklikleri, ayrılık ve boşanma süreçleri, yas ya da hastalık gibi ailenin tamamını etkileyen yaşam olayları bu görüşmelerde ele alınabilir.

## Süreç nasıl işler?

İlk görüşmelerde her bir tarafın bakış açısı dinlenir ve ilişkinin öyküsü değerlendirilir. Ardından görüşmelerin amacı ve sıklığı birlikte belirlenir. Terapistin rolü taraf tutmak değil, ilişkideki döngüleri birlikte görünür kılmak ve yeni bir iletişim dilinin kurulmasına eşlik etmektir.

İlgili konular: [İlişki ve evlilik sorunları](/tr/iliski-ve-evlilik-sorunlari/), [aile ilişkileri](/tr/aile-iliskileri/)."""),
        "en": ("couple-and-family-therapy", "Couple and family therapy",
               "Couple and family therapy in İzmir: sessions that look together at recurring cycles and communication difficulties in a relationship.",
               """Couple and family therapy approaches relationship problems not as one person’s problem, but as part of the interaction between people. Sessions are attended jointly by the couple or by several family members; individual sessions are added when needed.

## What is worked on?

Recurring cycles of conflict, communication difficulties, trust issues, parenting and changing roles within the family, separation and divorce, and life events that affect the whole family – such as bereavement or illness – can be addressed in these sessions.

## How does it work?

In the first sessions each person’s point of view is heard and the history of the relationship is explored. The aim and frequency of the sessions are then agreed together. The therapist’s role is not to take sides but to help make the cycles in the relationship visible and to accompany the building of a new way of communicating.

Related topics: [relationship and marriage problems](/en/relationship-and-marriage-problems/), [family relations](/en/family-relations/)."""),
        "de": ("cift-aile-terapisi", "Paar- und Familientherapie",
               "Paar- und Familientherapie in İzmir: Gespräche, in denen wiederkehrende Muster und Kommunikationsschwierigkeiten gemeinsam betrachtet werden.",
               """Die Paar- und Familientherapie betrachtet Beziehungsprobleme nicht als Problem einer einzelnen Person, sondern als Teil des Zusammenspiels zwischen Menschen. An den Sitzungen nehmen das Paar oder mehrere Familienmitglieder gemeinsam teil; bei Bedarf kommen Einzelgespräche hinzu.

## Woran wird gearbeitet?

Sich wiederholende Konfliktmuster, Kommunikationsschwierigkeiten, Vertrauensfragen, Elternschaft und sich verändernde Rollen in der Familie, Trennung und Scheidung sowie Lebensereignisse, die die ganze Familie betreffen – etwa Trauer oder Krankheit – können in diesen Gesprächen bearbeitet werden.

## Wie läuft sie ab?

In den ersten Sitzungen wird die Sicht jeder beteiligten Person gehört und die Geschichte der Beziehung besprochen. Danach werden Ziel und Häufigkeit der Sitzungen gemeinsam festgelegt. Aufgabe der Therapeutin oder des Therapeuten ist nicht, Partei zu ergreifen, sondern die Muster in der Beziehung gemeinsam sichtbar zu machen und den Aufbau einer neuen Art der Verständigung zu begleiten."""),
        "fr": ("therapie-de-couple-et-de-famille", "Thérapie de couple et de famille",
               "Thérapie de couple et de famille à İzmir : des séances pour examiner ensemble les cycles qui se répètent et les difficultés de communication.",
               """La thérapie de couple et de famille aborde les difficultés relationnelles non comme le problème d’une seule personne, mais comme une partie des interactions entre les personnes. Le couple ou plusieurs membres de la famille participent ensemble aux séances ; des entretiens individuels sont ajoutés si nécessaire.

## Sur quoi travaille-t-on ?

Les cycles de conflit qui se répètent, les difficultés de communication, les questions de confiance, la parentalité et l’évolution des rôles dans la famille, la séparation et le divorce, ainsi que les événements de vie qui touchent toute la famille – un deuil ou une maladie par exemple – peuvent être abordés.

## Comment cela se déroule-t-il ?

Lors des premières séances, le point de vue de chacun est entendu et l’histoire de la relation est explorée. L’objectif et la fréquence des séances sont ensuite définis ensemble. Le rôle du ou de la thérapeute n’est pas de prendre parti, mais de rendre visibles les cycles de la relation et d’accompagner la construction d’une nouvelle manière de communiquer."""),
    }),
    ("sanal-gerceklik-vr-ile-alistirma--exposure-tedavisi", {
        "tr": ("sanal-gerceklik-vr-ile-alistirma--exposure-tedavisi", "Sanal Gerçeklik (VR) ile Alıştırma Tedavisi",
               "Sanal gerçeklik ile alıştırma (exposure): fobiler ve kaçınma davranışlarında korkulan durumla kontrollü ve kademeli karşılaşma. İzmir.",
               """Alıştırma (maruz bırakma, İngilizcesiyle *exposure*) çalışmaları, kişinin kaçındığı ve yoğun kaygı duyduğu durumlarla kontrollü ve kademeli biçimde karşılaşmasına dayanan, bilişsel davranışçı terapinin yerleşik tekniklerindendir. Sanal gerçeklik ile alıştırmada bu durumlar, gerçek ortama gitmeden, özel bir gözlükle görüntülenen sanal bir ortamda canlandırılır.

## Nasıl uygulanır?

Çalışma muayenehanede, terapist eşliğinde yürütülür. Önce kaygı yaratan durumlar ve bunların şiddeti birlikte belirlenir. Ardından kişi, en az zorlayandan başlayarak bu durumlarla sanal ortamda karşılaşır. Her adımın hızı kişinin kendi kontrolündedir; zorlandığında uygulama durdurulabilir.

## Hangi durumlarda kullanılır?

Uçak, yükseklik, kalabalık ve kapalı alan korkusu gibi belirli fobiler ile panik atakla birlikte görülen kaçınma davranışları, sanal gerçeklik ile alıştırmanın kullanıldığı başlıca alanlardır. Uygun olup olmadığına ön değerlendirme sonrasında karar verilir; sonuçlar kişiden kişiye değişir.

Sanal ortamda baş dönmesi ya da mide bulantısı gibi geçici yan etkiler görülebilir; bu durumda uygulama kişinin isteğiyle hemen sonlandırılır.

İlgili konular: [Kaygı bozuklukları](/tr/kaygi-bozukluklari/), [panik atak](/tr/panik-atak/)."""),
        "en": ("virtual-reality-exposure-therapy", "Virtual reality (VR) exposure therapy",
               "Virtual reality exposure therapy in İzmir: gradual, controlled facing of feared situations for phobias and avoidance, at the practice.",
               """Exposure work – gradually and safely facing situations a person avoids because they cause intense anxiety – is an established technique of cognitive behavioural therapy. In virtual reality exposure, these situations are recreated in a virtual environment viewed through a headset, without having to go to the real place.

## How is it done?

Sessions take place at the practice, with the therapist present. First, the situations that cause anxiety, and how strongly they do so, are identified together. The person then faces these situations in the virtual environment, starting with the least challenging. The pace of each step stays under the person’s own control, and the exercise can be stopped at any time.

## When is it used?

Specific phobias – such as fear of flying, heights, crowds or enclosed spaces – and the avoidance that often accompanies panic attacks are the main areas in which VR exposure is used. Whether it is suitable is decided after an initial assessment; results vary from person to person.

Temporary side effects such as dizziness or nausea may occur in the virtual environment; if so, the exercise is stopped straight away at the person’s request.

Related topics: [anxiety disorders](/en/anxiety-disorders/), [panic attack](/en/panic-attack/)."""),
        "de": ("sanal-gerceklik-vr-ile-alistirma--exposure-tedavisi", "Expositionstherapie mit Virtual Reality (VR)",
               "Expositionstherapie mit Virtual Reality in İzmir: schrittweise, kontrollierte Konfrontation mit gefürchteten Situationen bei Phobien und Vermeidung.",
               """Expositionsübungen – das schrittweise und kontrollierte Sich-Stellen gegenüber Situationen, die starke Angst auslösen und deshalb vermieden werden – gehören zu den etablierten Techniken der kognitiven Verhaltenstherapie. Bei der VR-Exposition werden diese Situationen in einer virtuellen Umgebung nachgestellt, die über eine Brille betrachtet wird, ohne dass man sich an den realen Ort begeben muss.

## Wie wird sie durchgeführt?

Die Übungen finden in der Praxis und in Anwesenheit der Therapeutin oder des Therapeuten statt. Zunächst werden die angstauslösenden Situationen und deren Stärke gemeinsam festgelegt. Anschließend stellt man sich diesen Situationen in der virtuellen Umgebung, beginnend mit der am wenigsten belastenden. Das Tempo jedes Schritts bleibt unter eigener Kontrolle; die Übung kann jederzeit beendet werden.

## Wann wird sie eingesetzt?

Hauptanwendungsgebiete sind spezifische Phobien – etwa Flugangst, Höhenangst, Angst vor Menschenmengen oder vor engen Räumen – sowie das Vermeidungsverhalten, das Panikattacken häufig begleitet. Ob sie geeignet ist, wird nach einer Vorabklärung entschieden; die Ergebnisse sind von Person zu Person verschieden.

In der virtuellen Umgebung können vorübergehend Schwindel oder Übelkeit auftreten; in diesem Fall wird die Übung auf Wunsch sofort beendet."""),
        "fr": ("therapie-exposition-realite-virtuelle", "Thérapie d’exposition en réalité virtuelle (RV)",
               "Thérapie d’exposition en réalité virtuelle à İzmir : affronter progressivement et de manière contrôlée les situations redoutées (phobies, évitement).",
               """Les exercices d’exposition – affronter de manière progressive et contrôlée des situations évitées parce qu’elles suscitent une forte anxiété – font partie des techniques établies de la thérapie cognitive et comportementale. Dans l’exposition en réalité virtuelle, ces situations sont recréées dans un environnement virtuel visualisé à l’aide d’un casque, sans avoir à se rendre dans le lieu réel.

## Comment se déroule-t-elle ?

Les séances ont lieu au cabinet, en présence du ou de la thérapeute. Les situations anxiogènes et leur intensité sont d’abord définies ensemble. La personne affronte ensuite ces situations dans l’environnement virtuel, en commençant par la moins difficile. Le rythme de chaque étape reste sous son propre contrôle et l’exercice peut être interrompu à tout moment.

## Dans quels cas est-elle utilisée ?

Les phobies spécifiques – peur de l’avion, du vide, de la foule ou des espaces clos – ainsi que l’évitement qui accompagne souvent les crises de panique sont les principaux domaines d’utilisation. Son indication est décidée après une évaluation préalable ; les résultats varient d’une personne à l’autre.

Des effets passagers comme des vertiges ou des nausées peuvent survenir dans l’environnement virtuel ; l’exercice est alors arrêté immédiatement à la demande de la personne."""),
    }),
    ("online-bireysel-terapi", {
        "tr": ("online-bireysel-terapi", "Online Bireysel Terapi",
               "Online bireysel terapi: İzmir dışında yaşayan ya da muayenehaneye gelmesi güç olan danışanlar için görüntülü görüşmeyle bireysel psikoterapi.",
               """Online bireysel terapi, bireysel psikoterapi görüşmelerinin görüntülü görüşme ile yürütülmesidir. İzmir dışında yaşayan ya da muayenehaneye gelmesi güç olan danışanlar için bir seçenektir.

## Nasıl yürütülür?

Görüşmeler, kişinin kendini rahat hissettiği, sessiz ve başkalarının duyamayacağı bir ortamdan, güvenli bir görüntülü görüşme bağlantısıyla yapılır. Görüşme öncesinde teknik gereksinimler ve gizlilik konusunda bilgi verilir. Sürecin yapısı yüz yüze bireysel terapiye benzer: önce değerlendirme yapılır, ardından hedefler ve görüşme sıklığı birlikte belirlenir.

## Hangi durumlarda uygun değildir?

Her durum çevrim içi görüşmeye uygun değildir. Acil yardım gereken durumlarda, ağır ruhsal belirtilerde ya da yüz yüze tıbbi değerlendirmenin gerektiği hâllerde görüşmenin muayenehanede yapılması önerilir. Uygunluk ilk değerlendirmede birlikte kararlaştırılır.

Kendinize ya da bir başkasına zarar verme düşünceniz varsa beklemeyin: 112 Acil Çağrı Merkezi'ni arayın ya da en yakın acil servise başvurun."""),
        "en": ("online-individual-therapy", "Online individual therapy",
               "Online individual therapy: individual psychotherapy by video call for clients who live outside İzmir or find it hard to come to the practice.",
               """Online individual therapy means holding individual psychotherapy sessions by video call. It is an option for clients who live outside İzmir or who find it difficult to come to the practice.

## How does it work?

Sessions take place over a secure video connection, from a quiet place where the person feels comfortable and cannot be overheard. Information on technical requirements and confidentiality is given beforehand. The structure is similar to face-to-face therapy: an assessment first, then goals and session frequency agreed together.

## When is it not suitable?

Not every situation is suitable for online sessions. When urgent help is needed, when symptoms are severe, or when a face-to-face medical assessment is required, sessions at the practice are recommended. Suitability is decided together at the first assessment.

If you are having thoughts of harming yourself or someone else, do not wait: call 112, the emergency number in Türkiye, or go to the nearest emergency department."""),
        "de": ("online-bireysel-terapi", "Online-Einzeltherapie",
               "Online-Einzeltherapie: Einzelpsychotherapie per Videogespräch für Menschen, die außerhalb von İzmir leben oder schwer in die Praxis kommen können.",
               """Bei der Online-Einzeltherapie finden die Sitzungen der Einzelpsychotherapie per Videogespräch statt. Sie ist eine Möglichkeit für Menschen, die außerhalb von İzmir leben oder denen der Weg in die Praxis schwerfällt.

## Wie läuft sie ab?

Die Sitzungen erfolgen über eine sichere Videoverbindung, von einem ruhigen Ort aus, an dem Sie sich wohlfühlen und nicht mitgehört werden können. Vorab erhalten Sie Informationen zu den technischen Voraussetzungen und zur Vertraulichkeit. Der Ablauf ähnelt der Therapie in der Praxis: zuerst eine Abklärung, danach werden Ziele und Häufigkeit gemeinsam festgelegt.

## Wann ist sie nicht geeignet?

Nicht jede Situation eignet sich für Online-Sitzungen. Wenn dringend Hilfe nötig ist, bei schweren Beschwerden oder wenn eine ärztliche Untersuchung vor Ort erforderlich ist, wird ein Termin in der Praxis empfohlen. Ob die Online-Therapie geeignet ist, wird beim ersten Gespräch gemeinsam entschieden.

Wenn Sie daran denken, sich selbst oder anderen etwas anzutun, warten Sie nicht: Rufen Sie die Notrufnummer 112 an oder wenden Sie sich an die nächste Notaufnahme."""),
        "fr": ("therapie-individuelle-en-ligne", "Thérapie individuelle en ligne",
               "Thérapie individuelle en ligne : psychothérapie individuelle par visioconférence pour les personnes vivant hors d’İzmir ou ne pouvant venir au cabinet.",
               """La thérapie individuelle en ligne consiste à mener les séances de psychothérapie individuelle par visioconférence. C’est une possibilité pour les personnes qui vivent en dehors d’İzmir ou pour qui il est difficile de se rendre au cabinet.

## Comment se déroule-t-elle ?

Les séances ont lieu via une connexion vidéo sécurisée, depuis un endroit calme où vous vous sentez à l’aise et où personne ne peut vous entendre. Des informations sur les aspects techniques et la confidentialité sont données au préalable. Le déroulement est semblable à celui de la thérapie au cabinet : d’abord une évaluation, puis la définition commune des objectifs et de la fréquence des séances.

## Quand n’est-elle pas adaptée ?

Toutes les situations ne se prêtent pas aux séances en ligne. En cas de besoin d’aide urgente, de symptômes sévères ou lorsqu’un examen médical en présentiel est nécessaire, des séances au cabinet sont recommandées. L’indication est décidée ensemble lors de la première évaluation.

Si vous avez des pensées de vous faire du mal ou de faire du mal à quelqu’un, n’attendez pas : appelez le 112, le numéro d’urgence en Turquie, ou rendez-vous aux urgences les plus proches."""),
    }),
    ("psikoterapi-ve-psikolojik-danismanlik-hizmetleri", {
        "tr": ("psikoterapi-ve-psikolojik-danismanlik-hizmetleri", "Psikoterapi ve Psikolojik Danışmanlık",
               "Psikolojik danışmanlık: yaşam olayları, karar süreçleri ve iş yaşamına ilişkin güçlükler üzerine kısa süreli, amaca yönelik görüşmeler. İzmir.",
               """Psikolojik danışmanlık, belirli bir ruhsal bozukluğun tedavisinden çok, kişinin yaşamında karşılaştığı güçlüklerle ve vermesi gereken kararlarla ilgilenen, daha kısa süreli ve amaca yönelik görüşmelerdir.

## Hangi konularda?

İş ve kariyer değişiklikleri, taşınma ve yeni bir ortama uyum, ilişkilerdeki dönüm noktaları, ebeveynlik, yas ya da hastalık gibi zorlayıcı yaşam olayları bu görüşmelerde ele alınabilir. Kurumlar için, çalışanların iş yaşamına ilişkin güçlüklerine yönelik görüşmeler de yapılabilir.

## Psikoterapiden farkı nedir?

Danışmanlık görüşmeleri tanı koymaya ve tedavi etmeye yönelik değildir. Görüşmeler sırasında daha ayrıntılı bir değerlendirmenin ya da psikoterapinin yararlı olabileceği anlaşılırsa, bu durum kişiyle açıkça konuşulur ve psikiyatri uzmanı hekim tarafından değerlendirme yapılır.

İlgili konu: [İş yaşamına ilişkin sorunlar](/tr/is-yasamina-iliskin-sorunlar/)."""),
        "en": ("psychotherapy-and-psychological-counselling", "Psychotherapy and psychological counselling",
               "Psychological counselling in İzmir: shorter, goal-oriented sessions on life events, decisions and difficulties at work.",
               """Psychological counselling consists of shorter, goal-oriented sessions that focus less on treating a specific mental disorder and more on the difficulties a person meets in life and the decisions they need to make.

## Which topics?

Changes at work or in one’s career, moving and adjusting to a new environment, turning points in relationships, parenting, and demanding life events such as bereavement or illness can be addressed. Sessions can also be arranged for organisations, focusing on employees’ difficulties at work.

## How is it different from psychotherapy?

Counselling sessions are not aimed at making a diagnosis or providing treatment. If it becomes clear during the sessions that a more detailed assessment or psychotherapy may be helpful, this is discussed openly with the person and an assessment is carried out by the psychiatrist.

Related topic: [problems regarding working life](/en/problems-regarding-business-life/)."""),
        "de": ("psikoterapi-ve-psikolojik-danismanlik-hizmetleri", "Psychotherapie und psychologische Beratung",
               "Psychologische Beratung in İzmir: kürzere, zielgerichtete Gespräche zu Lebensereignissen, Entscheidungen und Schwierigkeiten im Beruf.",
               """Die psychologische Beratung besteht aus kürzeren, zielgerichteten Gesprächen. Im Vordergrund steht weniger die Behandlung einer bestimmten psychischen Erkrankung als die Schwierigkeiten, denen man im Leben begegnet, und die Entscheidungen, die zu treffen sind.

## Welche Themen?

Berufliche Veränderungen, ein Umzug und das Einleben in eine neue Umgebung, Wendepunkte in Beziehungen, Elternschaft sowie belastende Lebensereignisse wie Trauer oder Krankheit können besprochen werden. Für Organisationen sind auch Gespräche zu Schwierigkeiten von Mitarbeitenden im Berufsleben möglich.

## Worin unterscheidet sie sich von der Psychotherapie?

Beratungsgespräche zielen nicht auf eine Diagnose oder Behandlung. Zeigt sich im Verlauf, dass eine eingehendere Abklärung oder eine Psychotherapie hilfreich sein könnte, wird dies offen besprochen und eine Abklärung durch den Facharzt für Psychiatrie vorgenommen."""),
        "fr": ("psychotherapie-et-accompagnement-psychologique", "Psychothérapie et accompagnement psychologique",
               "Accompagnement psychologique à İzmir : des entretiens plus courts et ciblés sur les événements de vie, les décisions et les difficultés au travail.",
               """L’accompagnement psychologique consiste en des entretiens plus courts et ciblés, centrés moins sur le traitement d’un trouble psychique précis que sur les difficultés rencontrées dans la vie et les décisions à prendre.

## Quels sujets ?

Les changements professionnels, un déménagement et l’adaptation à un nouvel environnement, les tournants dans les relations, la parentalité ou des événements de vie éprouvants comme un deuil ou une maladie peuvent être abordés. Des entretiens destinés aux organisations, portant sur les difficultés des salariés au travail, sont également possibles.

## Quelle différence avec la psychothérapie ?

Les entretiens d’accompagnement ne visent pas à poser un diagnostic ni à traiter. S’il apparaît qu’une évaluation plus approfondie ou une psychothérapie pourrait être utile, cela est discuté ouvertement avec la personne et une évaluation est réalisée par le psychiatre."""),
    }),
    ("cocuk-ve-ergen-terapisi-", {
        "tr": ("cocuk-ve-ergen-terapisi-", "Çocuk ve Ergen Terapisi",
               "Çocuk ve ergen terapisi: çocuk ve gençlerle yaşa uygun yöntemlerle, aileyle iş birliği içinde yürütülen görüşmeler. İzmir, Güzelbahçe.",
               """Çocuk ve ergen terapisi, çocukların ve gençlerin duygusal, davranışsal ve gelişimsel güçlükleriyle, yaşlarına uygun yöntemlerle çalışmayı amaçlar. Çocuğun yaşamındaki en önemli etkenlerden biri aile olduğu için süreç aileyle iş birliği içinde yürütülür.

## Süreç nasıl işler?

İlk görüşmeler genellikle anne babayla yapılır: yakınmalar, çocuğun gelişim öyküsü, okul ve aile yaşamı değerlendirilir. Ardından çocukla ya da gençle görüşülür. Küçük yaşta oyun, resim ve kum tepsisi gibi araçlar; ergenlikte ise daha çok konuşmaya dayalı yöntemler kullanılır. Değerlendirmeye göre görüşme sıklığı ve ailenin sürece nasıl katılacağı birlikte belirlenir.

## Hangi konularda?

Kaygı ve korkular, [ayrılık kaygısı](/tr/ayrilik-kaygisi/), [okula uyum](/tr/okula-uyum/) ve [ders başarısıyla ilgili sorunlar, sınav kaygısı](/tr/ders-basarisizligi-ve-sinav-kaygisi/), öfke ve [davranış sorunları](/tr/davranis-bozukluklari/), yas ve aile içindeki değişikliklere (taşınma, boşanma, kardeş doğumu gibi) uyum bu görüşmelerde ele alınabilir.

Ergenlerle yapılan görüşmelerde gizlilik önemlidir; aileyle hangi bilgilerin paylaşılacağı, gencin güvenliği gözetilerek baştan konuşulur."""),
        "en": ("child-and-adolescent-therapy", "Child and adolescent therapy",
               "Child and adolescent therapy in İzmir: sessions with children and young people using age-appropriate methods, in cooperation with the family.",
               """Child and adolescent therapy works with children’s and young people’s emotional, behavioural and developmental difficulties, using methods suited to their age. Because the family is one of the most important influences in a child’s life, the process is carried out in cooperation with the family.

## How does it work?

The first sessions are usually with the parents: the concerns, the child’s developmental history, and school and family life are explored. The child or young person is then seen. With younger children, tools such as play, drawing and a sand tray are used; with adolescents, methods are mostly based on conversation. Based on the assessment, session frequency and how the family will take part are agreed together.

## Which concerns?

Anxieties and fears, [separation anxiety](/en/separation-anxiety/), difficulties at school and with schoolwork, [exam anxiety](/en/course-failure-and-exam-anxiety/), anger and [behaviour problems](/en/behaviour-disorders/), grief, and adjusting to changes in the family (such as moving, divorce or the birth of a sibling) can be addressed.

Confidentiality matters in work with adolescents; what will be shared with the family is discussed at the outset, with the young person’s safety in mind."""),
        "de": ("cocuk-ve-ergen-terapisi-", "Kinder- und Jugendlichentherapie",
               "Kinder- und Jugendlichentherapie in İzmir: Gespräche mit Kindern und Jugendlichen mit altersgerechten Methoden, in Zusammenarbeit mit der Familie.",
               """Die Kinder- und Jugendlichentherapie befasst sich mit emotionalen, verhaltensbezogenen und entwicklungsbedingten Schwierigkeiten von Kindern und Jugendlichen – mit Methoden, die ihrem Alter entsprechen. Da die Familie zu den wichtigsten Einflüssen im Leben eines Kindes gehört, erfolgt die Arbeit in Zusammenarbeit mit der Familie.

## Wie läuft sie ab?

Die ersten Gespräche finden meist mit den Eltern statt: Anliegen, Entwicklungsgeschichte des Kindes sowie Schul- und Familienleben werden besprochen. Danach folgt das Gespräch mit dem Kind oder der bzw. dem Jugendlichen. Bei jüngeren Kindern kommen Spiel, Malen und Sandspiel zum Einsatz, bei Jugendlichen überwiegend gesprächsbasierte Methoden. Auf Grundlage der Abklärung werden die Häufigkeit der Sitzungen und die Beteiligung der Familie gemeinsam festgelegt.

## Welche Anliegen?

Ängste, Trennungsangst, Schwierigkeiten in der Schule und beim Lernen, Prüfungsangst, Wut und Verhaltensprobleme, Trauer sowie die Anpassung an Veränderungen in der Familie (etwa Umzug, Scheidung oder die Geburt eines Geschwisters) können bearbeitet werden.

In der Arbeit mit Jugendlichen ist Vertraulichkeit wichtig; welche Informationen mit der Familie geteilt werden, wird zu Beginn und mit Blick auf die Sicherheit der bzw. des Jugendlichen besprochen."""),
        "fr": ("therapie-enfant-et-adolescent", "Thérapie de l’enfant et de l’adolescent",
               "Thérapie de l’enfant et de l’adolescent à İzmir : des séances adaptées à l’âge, menées en collaboration avec la famille.",
               """La thérapie de l’enfant et de l’adolescent s’intéresse aux difficultés émotionnelles, comportementales et développementales des enfants et des jeunes, avec des méthodes adaptées à leur âge. La famille étant l’une des influences les plus importantes dans la vie d’un enfant, le travail se fait en collaboration avec elle.

## Comment se déroule-t-elle ?

Les premiers entretiens ont généralement lieu avec les parents : les motifs de consultation, l’histoire du développement de l’enfant, la vie scolaire et familiale sont explorés. L’enfant ou l’adolescent est ensuite reçu. Avec les plus jeunes, on utilise le jeu, le dessin ou le bac à sable ; avec les adolescents, des méthodes surtout fondées sur la parole. Selon l’évaluation, la fréquence des séances et la place de la famille sont définies ensemble.

## Pour quelles difficultés ?

Les angoisses et les peurs, l’anxiété de séparation, les difficultés d’adaptation scolaire et d’apprentissage, l’anxiété face aux examens, la colère et les troubles du comportement, le deuil et l’adaptation aux changements familiaux (déménagement, divorce, naissance d’un frère ou d’une sœur…) peuvent être abordés.

Avec les adolescents, la confidentialité est importante : ce qui sera partagé avec la famille est discuté dès le départ, en tenant compte de la sécurité du jeune."""),
    }),
]


def main():
    for group, langs in PAGES:
        for lang, (slug, title, description, body) in langs.items():
            assert len(description) <= 170, (lang, slug, len(description))
            dest = OUT / lang / f"{slug}.md"
            if dest.exists():
                print(f"  = {lang}/{slug} (var, dokunulmadı)")
                continue
            draft = DRAFT["tr" if lang == "tr" else "xx"] + (ONLINE if group == "online-bireysel-terapi" else "")
            source = f"https://www.emdrizmir.com/{lang}/{slug}" if lang in ("tr", "de") else None
            fm = {"kind": "hizmet", "group": group, "title": title, "description": description,
                  "source": source, "draft": draft}
            lines = ["---"] + [f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in fm.items() if v] + ["---", ""]
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text("\n".join(lines) + body.strip() + "\n", encoding="utf-8")
            print(f"  + {lang}/{slug}")


if __name__ == "__main__":
    main()
