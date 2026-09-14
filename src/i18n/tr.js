export default {
  code: 'tr',
  htmlLang: 'tr',
  name: 'Türkçe',
  ogLocale: 'tr_TR',

  meta: {
    title: 'EMDR İzmir — Psikiyatri Uzmanı Hekimlerle EMDR Terapisi | Güzelbahçe',
    description:
      "İzmir Güzelbahçe'de psikiyatri uzmanı hekimler tarafından uygulanan EMDR terapisi, sanal gerçeklik ile alıştırma tedavisi ve kanıta dayalı psikoterapi. Travma, kaygı, panik atak ve depresyonda randevu alın.",
    ogImageAlt: 'EMDR İzmir — Güzelbahçe, İzmir',
  },

  a11y: {
    skip: 'İçeriğe atla',
    brandHome: 'EMDR İzmir — ana sayfa',
    mainNav: 'Ana menü',
    themeToggle: 'Açık / koyu temayı değiştir',
    openMenu: 'Menüyü aç',
    langSwitch: 'Dil seçin',
    langCurrent: 'Geçerli dil',
    footerNav: 'Alt menü',
    stars: '5 üzerinden 5',
  },

  cta: {
    appointment: 'Randevu Al',
    whatsapp: 'WhatsApp',
  },

  nav: [
    { href: '#emdr', label: 'EMDR Nedir' },
    { href: '#protokol', label: 'Protokol' },
    { href: '#hizmetler', label: 'Çalışma Alanları' },
    { href: '#ekip', label: 'Ekibimiz' },
    { href: '#makaleler', label: 'Makaleler' },
    { href: '#iletisim', label: 'İletişim' },
  ],

  drawer: [
    { href: '#emdr', label: 'EMDR Nedir' },
    { href: '#protokol', label: 'Sekiz Aşamalı Protokol' },
    { href: '#hizmetler', label: 'Çalışma Alanlarımız' },
    { href: '#ekip', label: 'Ekibimiz' },
    { href: '#neden', label: 'Neden EMDR' },
    { href: '#makaleler', label: 'Makaleler' },
    { href: '#iletisim', label: 'İletişim' },
  ],

  hero: {
    eyebrow: "Güzelbahçe, İzmir · 1999'dan beri hekimlik",
    titleHtml: 'Geçmişte kalması gereken bir anı, <em>bugünü</em> yönetmemeli.',
    lede:
      'EMDR İzmir; psikiyatri uzmanı hekimler tarafından yürütülen, etik değerlerin gözetildiği ve kanıta dayalı terapi yöntemlerinin uygulandığı bir merkezdir. Travma, kaygı, panik atak ve depresyonda EMDR terapisi ile çalışıyoruz.',
    trust: [
      { b: 'Türk Psikiyatri Derneği', rest: 'üye' },
      { b: 'EMDR Derneği', rest: 'üye' },
      { b: 'VR destekli', rest: 'alıştırma tedavisi' },
      { b: 'Online', rest: 'görüşme mümkün' },
    ],
    bls: {
      title: 'Çift yönlü uyarım',
      rate: '~0,5 Hz · sol ↔ sağ',
      trackAlt:
        'EMDR seansında kullanılan, soldan sağa hareket eden ışık noktasının canlandırması.',
      note:
        "EMDR'ın çekirdeği budur: anıyı hatırlarken dikkatin ritmik olarak iki yana yönlendirilmesi.",
      pause: 'Duraklat',
      resume: 'Devam et',
    },
    imageAlt: '',
  },

  emdr: {
    eyebrow: 'EMDR Nedir',
    h2: 'Göz hareketleri ile duyarsızlaştırma ve yeniden işlemleme',
    lead:
      'Tüm kaygı bozukluklarında, depresyonda, kişilik bozukluklarında ve bunların altında yatan psikolojik köklerin neden olduğu tıbbi hastalıkların tedavisinde etkili bir yöntemdir.',
    parasHtml: [
      'Günde yaklaşık 20 bin anıyı kaydediyoruz. Bu anıların bazıları olumlu, bazıları olumsuz, birçoğu ise önemsiz ve nötr olanlardan oluşuyor. Olumlu ve nötr anılar, bilgi işleme sürecinden normal bir şekilde geçip hafızaya atılır.',
      'Olumsuz ve travmatik anılar ise, tıpkı bilgisayara giren virüs gibi, bu süreci bozarlar. Bu anılar, anlamlandırma sürecinin normal çalışmasını engeller. Olumsuz anı, sadece geçmişte yaşamakla kalmıyor; etkisini hâlâ <em>bugün</em> yaşanmışçasına canlı olarak sürdürüyor.',
      'EMDR terapisi, o anıyı silmez. Anının yükünü çözer — böylece hatırladığınızda bedeniniz artık alarma geçmez.',
    ],
    stat: {
      imageAlt:
        'Çift yönlü uyarım çubuğu, gözlük ve bir bardak su bulunan terapi sehpası',
      number: '20.000',
      label:
        'Beynin bir günde kaydettiği yaklaşık anı sayısı. Sorun anıların çokluğu değil, aralarından işlenemeden kalanlardır.',
      scales: [
        {
          dt: 'SUD ölçeği',
          dd: "0–10 · Anıyı düşündüğünüzde hissettiğiniz sıkıntının öznel düzeyi. Hedef, seans sonunda 0'a yaklaşmasıdır.",
        },
        {
          dt: 'VOC ölçeği',
          dd: "1–7 · Olumlu inancın ne kadar “doğru hissettirdiği”. Hedef, 7'ye yaklaşmasıdır.",
        },
      ],
    },
  },

  protocol: {
    eyebrow: 'Standart Protokol',
    h2: 'Bir EMDR süreci sekiz aşamada ilerler',
    intro:
      'EMDR doğaçlama bir sohbet değildir; uluslararası kabul görmüş, sırası belli bir protokolü vardır. Aşağıdaki sekiz aşama, hangi terapistle çalışırsanız çalışın aynıdır — değişen, sizin hızınızdır.',
    phases: [
      {
        title: 'Öykü alma ve tedavi planı',
        en: 'Client History & Treatment Planning',
        text: 'Yaşam öykünüz dinlenir, bugünkü belirtilerin kökenindeki anılar belirlenir ve birlikte bir yol haritası çıkarılır.',
      },
      {
        title: 'Hazırlık',
        en: 'Preparation',
        text: 'Yöntem anlatılır ve “güvenli yer” gibi sakinleşme teknikleri çalışılır. Seanslar arasında kendinizi toparlayabilmeniz bu aşamada güvence altına alınır.',
      },
      {
        title: 'Değerlendirme',
        en: 'Assessment',
        text: 'Hedef anı; görüntüsü, olumsuz inancı, duygusu ve bedendeki yeri ile netleştirilir. Başlangıç düzeyleri ölçülür.',
      },
      {
        title: 'Duyarsızlaştırma',
        en: 'Desensitization',
        text: 'Çift yönlü uyarım eşliğinde anı üzerinde çalışılır. Sıkıntı düzeyi (SUD) düşene kadar setler tekrarlanır.',
      },
      {
        title: 'Yerleştirme',
        en: 'Installation',
        text: 'Olumsuz inancın yerini alacak olumlu inanç güçlendirilir: “Artık güvendeyim”, “Elimden geleni yaptım”.',
      },
      {
        title: 'Beden taraması',
        en: 'Body Scan',
        text: 'Anı yeniden düşünülürken bedende kalan gerginlik aranır. Kalan varsa üzerinde çalışılır — travma yalnızca zihinde tutulmaz.',
      },
      {
        title: 'Kapanış',
        en: 'Closure',
        text: 'Seans, işlem tamamlanmamış olsa bile dengeye getirilerek bitirilir. Odadan çıkarken ne yapacağınızı bilirsiniz.',
      },
      {
        title: 'Yeniden değerlendirme',
        en: 'Reevaluation',
        text: 'Bir sonraki seansın başında kazanımların kalıcılığı kontrol edilir ve plandaki bir sonraki hedefe geçilir.',
      },
    ],
  },

  services: {
    eyebrow: 'Çalışma Alanlarımız',
    h2: 'Altı başlıkta hizmet veriyoruz',
    intro:
      'Bilişim ve teknolojinin her geçen gün hayatımızda daha etkin kullanılmasıyla, terapilerimizi sanal gerçeklik ve EMDR ekipmanlarıyla destekliyoruz.',
    items: [
      {
        image: 'svc-individual',
        alt: 'Karşılıklı yerleştirilmiş iki koltuk ve aralarındaki küçük sehpa',
        title: 'Bireysel Yetişkin Psikoterapisi',
        text: 'Bire bir, düzenli seanslarla yürütülen yetişkin psikoterapisi. Yönteme sizinle birlikte karar veriyoruz.',
        tags: [
          'EMDR',
          'Psikodinamik Psikoterapi',
          'Kognitif Davranışçı Terapi',
          'Kabul ve Adanmışlık Terapisi',
        ],
      },
      {
        image: 'svc-couple-family',
        alt: 'Kanepe ve koltuktan oluşan üç kişilik oturma düzeni',
        title: 'Çift ve Aile Terapisi',
        text: 'İlişki içindeki tekrar eden döngüleri birlikte görünür kılmak ve dili yeniden kurmak üzerine çalışılır.',
        tags: ['Çift görüşmesi', 'Aile görüşmesi'],
      },
      {
        image: 'svc-vr',
        alt: 'Ahşap masada duran sanal gerçeklik başlığı ve not defteri',
        title: 'Sanal Gerçeklik (VR) ile Alıştırma Tedavisi',
        text: 'Korkulan durumla, güvenli bir odada, kontrollü ve kademeli olarak karşılaşma. Uçak, yükseklik, kalabalık gibi fobilerde kullanılır.',
        tags: ['Exposure', 'Fobiler', 'Panik atak'],
      },
      {
        image: 'svc-online',
        alt: 'Pencere önündeki masada açık dizüstü bilgisayar ve fincan',
        title: 'Online Bireysel Terapi',
        text: 'İzmir dışından veya yurt dışından danışanlar için görüntülü görüşme ile yürütülen bireysel terapi.',
        tags: ['Görüntülü seans', 'Yurt dışı'],
      },
      {
        image: 'svc-counselling',
        alt: 'Üstten görünüm: açık not defteri, dolma kalem ve gözlük',
        title: 'Psikoterapi ve Psikolojik Danışmanlık',
        text: 'Tanı odaklı olmayan, yaşam olayları ve karar süreçleri üzerine yürütülen danışmanlık görüşmeleri.',
        tags: ['Danışmanlık', 'Kurumsal görüşme'],
      },
      {
        image: 'svc-child-adolescent',
        alt: 'Çocuk masasında kum tepsisi, ahşap figürler ve kuru boyalar',
        title: 'Çocuk ve Ergen Terapisi',
        text: 'Yaşa uygun yöntemlerle, aile ile iş birliği içinde yürütülen çocuk ve ergen görüşmeleri.',
        tags: ['Çocuk', 'Ergen', 'Aile katılımı'],
      },
    ],
    topicsLabel: 'Üzerinde Çalıştığımız Konular',
    topics: [
      'Anksiyete (kaygı) bozuklukları',
      'Panik atak',
      'Depresyon',
      'Travma sonrası stres bozukluğu',
      'Fobi',
      'Bipolar bozukluk',
      'Stres bozuklukları',
      'Erişkin dikkat eksikliği',
    ],
  },

  team: {
    eyebrow: 'Ekibimiz',
    h2: 'Her biri alanında uzman, akredite psikoterapistler',
    intro:
      'Önceliğimiz acılarınızı kucaklayıp bu yolculukta size eşlik ederken psikolojik iyilik hâlinize katkıda bulunmaktır.',
    open: 'Özgeçmişin tamamı',
    close: 'Kapat',
    members: [
      {
        image: 'dr-mehmet-oguz',
        alt: 'Uzm. Dr. Mehmet Oğuz, psikiyatri uzmanı',
        name: 'Uzm. Dr. Mehmet Oğuz',
        role: 'Psikiyatri Uzmanı',
        summary:
          "1999 Marmara Üniversitesi Tıp Fakültesi mezunu. Türk Hava Kuvvetleri'nde ambulans uçak ve uçuş hekimliği yaptığı dönemde çok sayıda travma sonrası stres bozukluğu vakasını takip etti. 2014'te binbaşı rütbesindeyken ayrılarak özel sektörde çalışmaya başladı.",
        paras: [
          "Mehmet Oğuz 1999 yılında Marmara Üniversitesi Tıp Fakültesi'ni başarı ile tamamlayarak tıp doktoru unvanını almaya hak kazanmıştır. 1999–2001 yılları arasında Azizler Köyü Sağlık Ocağı'nda pratisyen hekim olarak görev yapmıştır.",
          "Ardından 2001 yılında katıldığı Türk Hava Kuvvetleri bünyesinde ambulans uçak ve uçuş hekimliği görevlerini üstlenmiştir. Bu esnada 2004 yılında Gülhane Askeri Tıp Akademisi Haydarpaşa Eğitim ve Araştırma Hastanesi'nde psikiyatri asistanlığını başarıyla tamamlayarak psikiyatri uzmanı olmuştur. Askeri kurumlarda görev yaptığı dönemde birçok travma sonrası stres bozukluğu vakasının takibini üstlenmiştir.",
          "2014 yılında binbaşı rütbesindeyken Türk Hava Kuvvetleri'nden ayrılıp psikiyatri doktoru ve psikoterapist olarak özel sektörde, uzman ekibiyle birlikte meslek hayatına devam etmektedir. EMDR terapisini birçok ruhsal problemin tedavisinde kullanmaktadır. Bunun dışında psikodinamik yönelimli psikoterapiler, Bilişsel-Davranışçı Terapi ve Şema Terapi gibi yöntemleri de uygulamaktadır. Türk Psikiyatri Derneği ve EMDR Derneği üyesidir.",
        ],
        groups: [
          {
            h4: 'Eğitim',
            items: [
              'Lisans — Marmara Üniversitesi Tıp Fakültesi',
              'Uzmanlık — Gülhane Askeri Tıp Akademisi Haydarpaşa Eğitim ve Araştırma Hastanesi',
            ],
          },
          {
            h4: 'Deneyim',
            items: [
              'Kendi özel muayenehanesinde psikiyatri hekimliği',
              'Türk Hava Kuvvetleri ambulans uçak ve uçuş hekimliği (2001–2014)',
              'Azizler Köyü Sağlık Ocağı pratisyen hekimliği (1999–2001)',
            ],
          },
          {
            h4: 'Uyguladığı terapi yöntemleri',
            items: [
              'EMDR terapisi',
              'Bilişsel Davranışçı Terapi',
              'Şema Terapi',
              'Psikodinamik yönelimli psikoterapiler',
            ],
          },
          {
            h4: 'Üzerinde çalıştığı konular',
            items: [
              'Anksiyete (kaygı) bozuklukları',
              'Bipolar bozukluk (iki uçlu duygu durum bozukluğu)',
              'Depresyon',
              'Fobi',
              'Panik atak',
              'Stres bozuklukları',
            ],
          },
        ],
        publicationsTitle: 'Yayınlar',
        citationsHtml: [
          'R. Tütüncü, M. Oğuz, A. Ateş, S. Ümit Başar, C. Başoğlu. “The Relationship Between Comorbid Psychiatric Illnesses and Psychopathy Levels On Male Individuals with Antisocial Personality Disorder in the Turkish Community.” <i>European Psychiatry</i>, 2015.',
          'Nihan Oğuz, Timuçin Oral, Mehmet Oğuz. “Temperament and Personality Traits of Bipolar Disorder I Patients Comorbid with Adult ADHD.” <i>Anadolu Psikiyatri Dergisi</i>, 2014.',
        ],
      },
      {
        image: 'dr-nihan-oguz',
        alt: 'Uzm. Dr. Nihan Oğuz, psikiyatri uzmanı',
        name: 'Uzm. Dr. Nihan Oğuz',
        role: 'Psikiyatri Uzmanı',
        summary:
          "Marmara Üniversitesi İngilizce Tıp Fakültesi mezunu; uzmanlığını Bakırköy Ruh Sağlığı ve Hastalıkları Eğitim ve Araştırma Hastanesi'nde tamamladı. Erenköy, Erzurum Bölge, İzmir Katip Çelebi AMATEM ve Urla Devlet Hastanesi'nde psikiyatri uzmanı olarak görev yaptı.",
        paras: [
          "1975 yılında Lüleburgaz'da doğdu. İlk ve orta öğrenimini Babaeski'de tamamladı.",
          "1992 yılında Marmara Üniversitesi İngilizce Tıp Fakültesi'ne başladı. 2000 yılında Bakırköy Ruh Sağlığı ve Hastalıkları Eğitim ve Araştırma Hastanesi'nde “Ruh Sağlığı ve Hastalıkları” uzmanlık eğitimine başladı. Bitirme tezi, “Remisyonda iki uçlu mizaç bozukluğunda erişkin dikkat eksikliği ve hiperaktivite bozukluğunun komorbiditesi”dir. 2005 yılında BRSHH'den ayrıldı.",
        ],
        groups: [
          {
            h4: 'Görev yaptığı kurumlar',
            items: [
              'Erenköy Ruh ve Sinir Hastalıkları Eğitim ve Araştırma Hastanesi (2006–2009)',
              'Erzurum Bölge Eğitim ve Araştırma Hastanesi (2009–2013)',
              'İzmir Katip Çelebi Üniversitesi Atatürk EAH, AMATEM polikliniği (2013–2016)',
              'Urla Devlet Hastanesi (2016–2020)',
            ],
          },
        ],
        publicationsTitle: 'Yayınlar',
        citationsHtml: [
          'Nihan Oğuz, Niyazi Uygur. “Bir Olgu Nedeniyle Bebek Bezi Fetişizmi.” <i>Türk Psikiyatri Dergisi</i>, 2005; 16(2):133–138.',
          'Nihan Oğuz, Cem İlnem, Ferhan Yener. “Viral Ensefalite Bağlı Deliryum: Bir Olgu Sunumu.”',
        ],
      },
      {
        image: 'ahmet-cengiz-koksal',
        alt: 'Ahmet Cengiz Köksal, kurum müdürü',
        name: 'Ahmet Cengiz Köksal',
        role: 'Kurum Müdürü',
        summary:
          "Ankara Siyasal Bilgiler mezunu; uzmanlığını İngiltere'de Dover Wilmington Üniversitesi'nde yaptı. Özel sektörde yöneticilik deneyiminin ardından kurum müdürü olarak EMDR İzmir ekibine katıldı.",
        paras: [
          "1983 yılında Elazığ'da doğmuştur. Elazığ'da ilk ve orta öğretimini tamamladıktan sonra üniversite eğitimini Ankara Siyasal Bilgiler'de tamamlamış, daha sonra uzmanlığını İngiltere Dover Wilmington Üniversitesi'nde yapmıştır.",
          "Sırasıyla Büyük Okyanus Şirketler Grubu'nda ve Vakıfbank'ta yönetici pozisyonunda çalıştıktan sonra kurum müdürü olarak EMDR İzmir ekibine katılmıştır.",
        ],
        groups: [],
        publicationsTitle: 'Yayınlar',
        citationsHtml: [],
      },
    ],
  },

  why: {
    eyebrow: 'Hekimin Kaleminden',
    h2: 'Neden EMDR',
    intro: [
      'Ben size neden EMDR terapisi almalısınızı değil, neden EMDR terapisi yapmayı seçtiğimi anlatmak istiyorum.',
      'Kullanılan terapi yöntemleri çok uzun sürüyor, çözüm odaklı olmuyor ve hasta belki de hayatı boyunca ilaç kullanmak zorunda bırakılıyordu. Daha temel bir çözüm arayışına girdim.',
    ],
    open: 'Yazının tamamını oku',
    close: 'Kısalt',
    body: [
      "Benim tek bir soruyla Tıp Fakültesi'ne gitme sebebim — istediğim mühendisliği tutturmuşken üstelik — kayıtsız şartsız insanlara yardım etmekti. Bütün doktorlar aynı sebeple fakülteye başlıyor ve hepsinin tek amacı insanlık için bir şey yapmak.",
      'Peki neden psikiyatri? Hepinizden çok farklı değilim, hiçbir insan diğerinden çok farklı değil. Travmalarımızın şekillendirdiği bir “şimdi” yaşıyoruz. Ben mesleğim sayesinde travmalarımın hangi otomatik olumsuz düşünceleri doğurduğu, hangi algılarımda çarpıklık olduğu, daha doğrusu hangi duygularımın düşüncelerimi büktüğü konusunda biraz daha şanslıydım. Ama yine de yetmiyordu.',
      "Ben EMDR eğitimi için İstanbul'a gittiğimde, herkes bana “saçma” olduğunu söyledi; oysa gerçekten bilimsel dayanağı olan, ispatlanmış ve çözüm odaklı bir yöntemdi. Daha fazla insana daha kısa sürede yardımcı olmak için gittim. Çünkü ben de sizin gibiydim, onlar gibiydim, hepimiz gibiydim; çocukluğumda yaşadığım her şeyin günümüzdeki etkileriyle yüzleştikçe sizleri daha iyi anlamaya başladım.",
      'EMDR eğitimine gittiğim için hiç pişman olmadım. Sizlere duygularımı çok net açamam; ben sizin terapistinizim, aynanızım. Ama şunu bilmeniz için yazıyorum: acılarınızı anlıyorum.',
      'Tek bir gün fazla ruhsal acı çekmenizi istemediğim için EMDR terapisi yapmayı seçtim. Birçok sertifikam var ama en kalıcı sonuçları, tecrübelerime dayanarak EMDR terapisi ile aldığım için EMDR terapisi yapmayı seçtim.',
      'Sizin için EMDR terapisi yapmayı seçtim. Hayata dört elle sarılın, her anın keyfini alın, bir çiçeğe baktığınızda onun güzelliğini görün diye. Zor günler yaşıyoruz, hepimiz, el ele… Sevgiyle ve barışla kalın, kardeşlerim.',
    ],
    sign: { name: 'Uzm. Dr. Mehmet Oğuz', role: 'Psikiyatri Uzmanı' },
    closing:
      '“Hayat bir yolculuk; cam kenarından yolu seyretmeyi seçin, cama yansıyan yorgun yüzünüzü değil. Güçlü olmayı değil, dayanıklı olmayı seçin. Mutlu olmayı değil, dengede olmayı hedefleyin. Hayat yeterince zor ve yorucu; siz en çok da kendinizi sevmeyi seçin.”',
  },

  articles: {
    eyebrow: 'Makalelerimiz',
    h2: 'Yayınlar ve yazılar',
    items: [
      {
        title: 'Bir Olgu Nedeniyle Bebek Bezi Fetişizmi',
        meta: ['Türk Psikiyatri Dergisi', '2005 · 16(2):133–138'],
        authors: 'Dr. Nihan Oğuz, Dr. Niyazi Uygur',
      },
      {
        title: 'Viral Ensefalite Bağlı Deliryum: Bir Olgu Sunumu',
        meta: ['Olgu sunumu'],
        authors: 'Nihan Oğuz, Cem İlnem, Ferhan Yener',
      },
      {
        title:
          'Beyin Tümörlerinin Neden Olduğu Psikiyatrik Tablolar: İki Olgu Sunumu',
        meta: ['Olgu sunumu'],
        authors: 'EMDR İzmir',
      },
      {
        title:
          'The Relationship Between Comorbid Psychiatric Illnesses and Psychopathy Levels On Male Individuals with Antisocial Personality Disorder in the Turkish Community',
        meta: ['European Psychiatry', '2015'],
        authors: 'R. Tütüncü, M. Oğuz, A. Ateş, S. Ümit Başar, C. Başoğlu',
      },
      {
        title:
          'Temperament and Personality Traits of Bipolar Disorder I Patients Comorbid with Adult ADHD',
        meta: ['Anadolu Psikiyatri Dergisi', '2014'],
        authors: 'Nihan Oğuz, Timuçin Oral, Mehmet Oğuz',
      },
      {
        title: 'Covid-19 ve Ruhsal Değişim: Olmak ya da Olmamak!',
        meta: ['Blog yazısı'],
        authors: 'Uzm. Dr. Mehmet Oğuz',
      },
      {
        title: 'Hayata Başlangıç Boş Bir Tahta mıdır?',
        meta: ['Blog yazısı'],
        authors: 'Uzm. Dr. Mehmet Oğuz',
      },
    ],
  },

  contact: {
    eyebrow: 'İletişim',
    h2: 'Randevu alın',
    intro:
      'Size en uygun zamanı seçerek randevu talep edebilirsiniz. Formu doldurduğunuzda mesajınız hazırlanır; göndermeden önce dilediğiniz gibi düzenleyebilirsiniz.',
    labels: {
      address: 'Adres',
      phone: 'Telefon',
      email: 'E-posta',
      hours: 'Çalışma saatleri',
      languages: 'Görüşme dilleri',
      social: 'Sosyal medya',
    },
    hoursValue: 'Pazartesi – Cumartesi · 10:00 – 18:00',
    hoursClosed: 'Pazar kapalı',
    languagesValue: 'Türkçe · English · Deutsch · Français',
    imageAlt: '',
    form: {
      h3: 'Randevu talebi',
      note: 'Mesajınız WhatsApp veya e-posta uygulamanızda hazır olarak açılır. Gönderme kararı sizindir.',
      name: { label: 'Ad Soyad', placeholder: 'Adınız ve soyadınız' },
      tel: {
        label: 'Telefon',
        optional: '(isteğe bağlı)',
        placeholder: '05xx xxx xx xx',
      },
      mode: {
        label: 'Görüşme şekli',
        options: [
          'Yüz yüze — Güzelbahçe',
          'Online — görüntülü',
          'Fark etmez',
        ],
      },
      msg: {
        label: 'Mesajınız',
        placeholder: 'Birkaç cümle yeterli. Ayrıntıları görüşmede konuşuruz.',
      },
      sendWa: "WhatsApp'ta aç",
      sendMail: 'E-posta ile aç',
      privacy:
        'Bu form bilgilerinizi hiçbir sunucuya göndermez; yalnızca sizin cihazınızda bir mesaj metni hazırlar. Kişisel sağlık verileriniz, 6698 sayılı Kişisel Verilerin Korunması Kanunu kapsamında yalnızca açık rızanızla kaydedilir.',
    },
    message: {
      greeting: 'Merhaba, randevu talebinde bulunmak istiyorum.',
      name: 'Ad Soyad',
      tel: 'Telefon',
      mode: 'Görüşme şekli',
      subject: 'Randevu talebi',
    },
    map: {
      iframeTitle:
        'EMDR İzmir — Yalı Mah. 268. Sk. No: 17, Güzelbahçe / İzmir harita konumu',
      consentButton: 'Haritayı yükle',
      consentNote:
        'Haritayı açtığınızda Google Maps yüklenir ve IP adresiniz Google ile paylaşılır. Yüklemeden yol tarifi almak için aşağıdaki bağlantıyı kullanabilirsiniz.',
      directions: 'Yol tarifi al',
    },
  },

  footer: {
    about:
      'Etik değerlerin gözetildiği, kanıta dayalı terapi yöntemlerinin uygulandığı bir psikiyatri ve psikoterapi merkezi. Güzelbahçe, İzmir.',
    pagesTitle: 'Sayfalar',
    pages: [
      { href: '#emdr', label: 'EMDR Nedir' },
      { href: '#protokol', label: 'Sekiz Aşamalı Protokol' },
      { href: '#hizmetler', label: 'Çalışma Alanlarımız' },
      { href: '#ekip', label: 'Ekibimiz' },
      { href: '#neden', label: 'Neden EMDR' },
      { href: '#makaleler', label: 'Makaleler' },
    ],
    contactTitle: 'İletişim',
    crisisHtml:
      "<b>Acil durum:</b> Kendinize veya bir başkasına zarar verme düşünceniz varsa lütfen beklemeyin — <b>112 Acil Çağrı Merkezi</b>'ni arayın ya da en yakın acil servise başvurun. Bu site tıbbi tavsiye yerine geçmez; tanı ve tedavi yalnızca yüz yüze değerlendirme ile yapılır.",
    legal: {
      title: 'Kurum bilgileri',
      officialName: 'Ruhsat unvanı',
      facilityType: 'Kuruluş türü',
      licence: 'Ruhsat / faaliyet izin belgesi',
      licenceAuthority: 'Belgeyi veren',
      responsibleManager: 'Mesul müdür',
      lastUpdated: 'Son güncelleme',
      editor: 'Site editörü',
    },
    rights: 'EMDR İzmir · Tüm hakları saklıdır.',
    kvkk: 'KVKK aydınlatma ve onam metnimiz muayenehanemizde erişilebilirdir.',
  },
};
