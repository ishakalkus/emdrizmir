export default {
  code: 'en',
  htmlLang: 'en',
  name: 'English',
  ogLocale: 'en_GB',

  meta: {
    title: 'EMDR İzmir — EMDR Therapy with Psychiatrists in Güzelbahçe, İzmir',
    description:
      'EMDR therapy delivered by consultant psychiatrists in Güzelbahçe, İzmir. Virtual-reality assisted exposure therapy and evidence-based psychotherapy for trauma, anxiety, panic attacks and depression. English-speaking appointments available.',
    ogImageAlt: 'EMDR İzmir — Güzelbahçe, İzmir, Turkey',
  },

  a11y: {
    skip: 'Skip to content',
    brandHome: 'EMDR İzmir — home',
    mainNav: 'Main menu',
    themeToggle: 'Switch between light and dark theme',
    openMenu: 'Open menu',
    langSwitch: 'Choose a language',
    langCurrent: 'Current language',
    footerNav: 'Footer menu',
    stars: '5 out of 5',
  },

  cta: {
    appointment: 'Book an appointment',
    whatsapp: 'WhatsApp',
  },

  nav: [
    { href: '#emdr', label: 'What is EMDR' },
    { href: '#protokol', label: 'Protocol' },
    { href: '#hizmetler', label: 'Our services' },
    { href: '#ekip', label: 'Our team' },
    { href: '#makaleler', label: 'Publications' },
    { href: '#iletisim', label: 'Contact' },
  ],

  drawer: [
    { href: '#emdr', label: 'What is EMDR' },
    { href: '#protokol', label: 'The eight-phase protocol' },
    { href: '#hizmetler', label: 'Our services' },
    { href: '#ekip', label: 'Our team' },
    { href: '#neden', label: 'Why EMDR' },
    { href: '#makaleler', label: 'Publications' },
    { href: '#iletisim', label: 'Contact' },
  ],

  hero: {
    eyebrow: 'Güzelbahçe, İzmir · Practising medicine since 1999',
    titleHtml:
      'A memory that belongs in the past should not be running <em>today</em>.',
    lede:
      'EMDR İzmir is a centre led by consultant psychiatrists, built on clear ethical standards and evidence-based methods of therapy. We work with EMDR on trauma, anxiety, panic attacks and depression.',
    trust: [
      { b: 'Turkish Psychiatric Association', rest: 'member' },
      { b: 'EMDR Association', rest: 'member' },
      { b: 'VR-assisted', rest: 'exposure therapy' },
      { b: 'Online', rest: 'sessions available' },
    ],
    bls: {
      title: 'Bilateral stimulation',
      rate: '~0.5 Hz · left ↔ right',
      trackAlt:
        'Animation of the point of light used in an EMDR session, moving from left to right.',
      note:
        'This is the core of EMDR: while you hold the memory in mind, attention is guided rhythmically from side to side.',
      pause: 'Pause',
      resume: 'Resume',
    },
    imageAlt: '',
  },

  emdr: {
    eyebrow: 'What is EMDR',
    h2: 'Eye Movement Desensitisation and Reprocessing',
    lead:
      'It is an effective method across all anxiety disorders, in depression, in personality disorders, and in medical conditions driven by the psychological roots underlying them.',
    parasHtml: [
      'We record roughly twenty thousand memories a day. Some of them are positive, some negative, and a great many are unremarkable and neutral. Positive and neutral memories pass through information processing in the ordinary way and are filed into memory.',
      'Negative and traumatic memories, however, disrupt that process — much like a virus entering a computer. They keep the work of making meaning from running properly. The negative memory does not merely stay in the past; it carries on as vividly as if it were still happening <em>today</em>.',
      'EMDR therapy does not erase the memory. It releases the charge the memory carries — so that when you remember it, your body no longer sounds the alarm.',
    ],
    stat: {
      imageAlt:
        'A therapy table holding a bilateral stimulation light bar, a pair of glasses and a glass of water',
      number: '20,000',
      label:
        'The approximate number of memories the brain records in a single day. The problem is not how many there are, but the ones left unprocessed among them.',
      scales: [
        {
          dt: 'SUD scale',
          dd: '0–10 · The subjective level of distress you feel when you bring the memory to mind. The aim is for it to approach 0 by the end of the session.',
        },
        {
          dt: 'VOC scale',
          dd: '1–7 · How “true” the positive belief feels. The aim is for it to approach 7.',
        },
      ],
    },
  },

  protocol: {
    eyebrow: 'Standard protocol',
    h2: 'An EMDR course of treatment moves through eight phases',
    intro:
      'EMDR is not an improvised conversation; it follows an internationally recognised protocol with a set order. The eight phases below are the same whichever therapist you work with — what changes is your own pace.',
    phases: [
      {
        title: 'Client history and treatment planning',
        en: '',
        text: 'We listen to your life history, identify the memories at the root of your present symptoms, and draw up a route map together.',
      },
      {
        title: 'Preparation',
        en: '',
        text: 'The method is explained and calming techniques such as the “safe place” are practised. This is the phase that makes sure you can settle yourself between sessions.',
      },
      {
        title: 'Assessment',
        en: '',
        text: 'The target memory is brought into focus: its image, the negative belief attached to it, the emotion, and where it sits in the body. Baseline levels are measured.',
      },
      {
        title: 'Desensitisation',
        en: '',
        text: 'The memory is worked through alongside bilateral stimulation. Sets are repeated until the level of distress (SUD) comes down.',
      },
      {
        title: 'Installation',
        en: '',
        text: 'The positive belief that will take the place of the negative one is strengthened: “I am safe now”, “I did what I could”.',
      },
      {
        title: 'Body scan',
        en: '',
        text: 'While the memory is brought to mind again, we look for tension left in the body. Anything remaining is worked on — trauma is not held in the mind alone.',
      },
      {
        title: 'Closure',
        en: '',
        text: 'The session is brought back into balance before it ends, even if processing is incomplete. You leave the room knowing what to do next.',
      },
      {
        title: 'Re-evaluation',
        en: '',
        text: 'At the start of the next session we check that the gains have held, then move on to the next target in the plan.',
      },
    ],
  },

  services: {
    eyebrow: 'Our services',
    h2: 'We work across six areas',
    intro:
      'As information technology takes a more active place in our lives with each passing year, we support our therapies with virtual reality and EMDR equipment.',
    items: [
      {
        image: 'svc-individual',
        alt: 'Two armchairs facing one another with a small table between them',
        title: 'Individual adult psychotherapy',
        text: 'One-to-one adult psychotherapy in regular sessions. We decide on the method together with you.',
        tags: [
          'EMDR',
          'Psychodynamic psychotherapy',
          'Cognitive behavioural therapy',
          'Acceptance and commitment therapy',
        ],
      },
      {
        image: 'svc-couple-family',
        alt: 'A seating arrangement for three, made up of a sofa and an armchair',
        title: 'Couple and family therapy',
        text: 'The work is about making the repeating cycles within a relationship visible together, and rebuilding the language used inside it.',
        tags: ['Couple sessions', 'Family sessions'],
      },
      {
        image: 'svc-vr',
        alt: 'A virtual reality headset and a notebook on a wooden table',
        title: 'Virtual reality (VR) exposure therapy',
        text: 'Meeting the feared situation in a safe room, in a controlled and graded way. Used in phobias such as flying, heights and crowds.',
        tags: ['Exposure', 'Phobias', 'Panic attacks'],
      },
      {
        image: 'svc-online',
        alt: 'An open laptop and a cup on a desk in front of a window',
        title: 'Online individual therapy',
        text: 'Individual therapy by video call, for clients outside İzmir or abroad.',
        tags: ['Video sessions', 'From abroad'],
      },
      {
        image: 'svc-counselling',
        alt: 'Seen from above: an open notebook, a fountain pen and a pair of glasses',
        title: 'Psychotherapy and psychological counselling',
        text: 'Counselling sessions that are not diagnosis-led, working on life events and decision-making.',
        tags: ['Counselling', 'Corporate sessions'],
      },
      {
        image: 'svc-child-adolescent',
        alt: "A sand tray, wooden figures and dry pastels on a child's table",
        title: 'Child and adolescent therapy',
        text: 'Sessions for children and adolescents using age-appropriate methods, in collaboration with the family.',
        tags: ['Children', 'Adolescents', 'Family involvement'],
      },
    ],
    topicsLabel: 'Conditions we work with',
    topics: [
      'Anxiety disorders',
      'Panic attacks',
      'Depression',
      'Post-traumatic stress disorder',
      'Phobias',
      'Bipolar disorder',
      'Stress disorders',
      'Adult attention deficit',
    ],
  },

  team: {
    eyebrow: 'Our team',
    h2: 'Accredited psychotherapists, each a specialist in their field',
    intro:
      'Our priority is to hold what hurts, to walk this road alongside you, and to contribute to your psychological wellbeing.',
    open: 'Full biography',
    close: 'Close',
    members: [
      {
        image: 'dr-mehmet-oguz',
        alt: 'Dr Mehmet Oğuz, consultant psychiatrist',
        name: 'Dr Mehmet Oğuz, MD',
        role: 'Consultant Psychiatrist',
        summary:
          'Graduated from Marmara University School of Medicine in 1999. While serving as an air ambulance and flight surgeon in the Turkish Air Force he followed a large number of post-traumatic stress disorder cases. He left the service in 2014 with the rank of major and moved into private practice.',
        paras: [
          'Mehmet Oğuz completed his studies at Marmara University School of Medicine with distinction in 1999, earning the title of doctor of medicine. Between 1999 and 2001 he worked as a general practitioner at the Azizler Village Health Centre.',
          'He then joined the Turkish Air Force in 2001, taking on duties as an air ambulance and flight surgeon. During this period, in 2004, he completed his psychiatry residency at the Gülhane Military Medical Academy Haydarpaşa Training and Research Hospital and qualified as a consultant psychiatrist. Throughout his service in military institutions he took charge of following many post-traumatic stress disorder cases.',
          'In 2014, holding the rank of major, he left the Turkish Air Force and has continued his professional life in private practice as a psychiatrist and psychotherapist, together with his specialist team. He uses EMDR therapy in the treatment of many mental health problems. He also practises psychodynamically oriented psychotherapies, cognitive behavioural therapy and schema therapy. He is a member of the Turkish Psychiatric Association and the EMDR Association.',
        ],
        groups: [
          {
            h4: 'Education',
            items: [
              'Degree — Marmara University School of Medicine',
              'Specialist training — Gülhane Military Medical Academy Haydarpaşa Training and Research Hospital',
            ],
          },
          {
            h4: 'Experience',
            items: [
              'Psychiatry in his own private practice',
              'Turkish Air Force air ambulance and flight surgeon (2001–2014)',
              'General practitioner, Azizler Village Health Centre (1999–2001)',
            ],
          },
          {
            h4: 'Methods of therapy practised',
            items: [
              'EMDR therapy',
              'Cognitive behavioural therapy',
              'Schema therapy',
              'Psychodynamically oriented psychotherapies',
            ],
          },
          {
            h4: 'Conditions he works with',
            items: [
              'Anxiety disorders',
              'Bipolar disorder',
              'Depression',
              'Phobias',
              'Panic attacks',
              'Stress disorders',
            ],
          },
        ],
        publicationsTitle: 'Publications',
        citationsHtml: [
          'R. Tütüncü, M. Oğuz, A. Ateş, S. Ümit Başar, C. Başoğlu. “The Relationship Between Comorbid Psychiatric Illnesses and Psychopathy Levels On Male Individuals with Antisocial Personality Disorder in the Turkish Community.” <i>European Psychiatry</i>, 2015.',
          'Nihan Oğuz, Timuçin Oral, Mehmet Oğuz. “Temperament and Personality Traits of Bipolar Disorder I Patients Comorbid with Adult ADHD.” <i>Anadolu Journal of Psychiatry</i>, 2014.',
        ],
      },
      {
        image: 'dr-nihan-oguz',
        alt: 'Dr Nihan Oğuz, consultant psychiatrist',
        name: 'Dr Nihan Oğuz, MD',
        role: 'Consultant Psychiatrist',
        summary:
          'A graduate of the English-language medical programme at Marmara University; she completed her specialist training at Bakırköy Mental Health and Neurological Diseases Training and Research Hospital. She has served as a consultant psychiatrist at Erenköy, Erzurum Regional, İzmir Katip Çelebi AMATEM and Urla State Hospital.',
        paras: [
          'She was born in Lüleburgaz in 1975 and completed her primary and secondary education in Babaeski.',
          'In 1992 she began the English-language medical programme at Marmara University. In 2000 she started specialist training in “Mental Health and Diseases” at Bakırköy Mental Health and Neurological Diseases Training and Research Hospital. Her thesis was titled “Comorbidity of adult attention deficit and hyperactivity disorder in bipolar mood disorder in remission”. She left the hospital in 2005.',
        ],
        groups: [
          {
            h4: 'Institutions where she has served',
            items: [
              'Erenköy Mental and Neurological Diseases Training and Research Hospital (2006–2009)',
              'Erzurum Regional Training and Research Hospital (2009–2013)',
              'İzmir Katip Çelebi University Atatürk Training and Research Hospital, AMATEM outpatient clinic (2013–2016)',
              'Urla State Hospital (2016–2020)',
            ],
          },
        ],
        publicationsTitle: 'Publications',
        citationsHtml: [
          'Nihan Oğuz, Niyazi Uygur. “Diaper Fetishism: A Case Report.” <i>Turkish Journal of Psychiatry</i>, 2005; 16(2):133–138.',
          'Nihan Oğuz, Cem İlnem, Ferhan Yener. “Delirium Due to Viral Encephalitis: A Case Report.”',
        ],
      },
      {
        image: 'ahmet-cengiz-koksal',
        alt: 'Ahmet Cengiz Köksal, practice manager',
        name: 'Ahmet Cengiz Köksal',
        role: 'Practice Manager',
        summary:
          'A graduate of political science in Ankara; he took his postgraduate qualification at Dover Wilmington University in England. After a career in management in the private sector he joined the EMDR İzmir team as practice manager.',
        paras: [
          'He was born in Elazığ in 1983. After completing his primary and secondary education in Elazığ he read political science in Ankara, and later took his postgraduate qualification at Dover Wilmington University in England.',
          'Having worked in management positions at the Büyük Okyanus group of companies and then at Vakıfbank, he joined the EMDR İzmir team as practice manager.',
        ],
        groups: [],
        publicationsTitle: 'Publications',
        citationsHtml: [],
      },
    ],
  },

  why: {
    eyebrow: 'From the doctor’s pen',
    h2: 'Why EMDR',
    intro: [
      'I do not want to tell you why you should have EMDR therapy, but why I chose to practise it.',
      'The methods of therapy in use took a very long time, were not solution-focused, and the patient was left having to take medication perhaps for the rest of their life. I went looking for a more fundamental answer.',
    ],
    open: 'Read the whole letter',
    close: 'Show less',
    body: [
      'My reason for going to medical school — and this with a single question, when I had already secured the engineering place I wanted — was to help people unconditionally. Every doctor starts at the faculty for the same reason, and the single aim of all of them is to do something for humanity.',
      'So why psychiatry? I am not very different from any of you; no person is very different from another. We live in a “now” shaped by our traumas. Thanks to my profession I was a little more fortunate in seeing which automatic negative thoughts my own traumas gave rise to, where my perceptions were distorted — or more precisely, which of my emotions were bending my thoughts. Even so, it was not enough.',
      'When I went to İstanbul for EMDR training, everyone told me it was “nonsense”; in fact it was a genuinely evidence-based, proven and solution-focused method. I went in order to help more people in less time. Because I was like you, I was like them, I was like all of us; the more I faced what everything from my childhood was still doing to my present, the better I came to understand you.',
      'I have never regretted going to that training. I cannot open my feelings to you very plainly; I am your therapist, your mirror. But I am writing so that you know this: I understand what hurts you.',
      'I chose to practise EMDR therapy because I do not want you to suffer a single day more than you must. I hold many certificates, but I chose EMDR because, in my experience, it is with EMDR that I have seen the most lasting results.',
      'I chose to practise EMDR therapy for you. So that you take hold of life with both hands, take pleasure in every moment, and see the beauty of a flower when you look at one. These are hard days, for all of us, hand in hand… Stay with love and with peace, my friends.',
    ],
    sign: { name: 'Dr Mehmet Oğuz, MD', role: 'Consultant Psychiatrist' },
    closing:
      '“Life is a journey; choose to watch the road from the window seat, not your own tired face reflected in the glass. Choose not to be strong, but to be resilient. Aim not at happiness, but at balance. Life is hard and tiring enough; above all, choose to love yourself.”',
  },

  articles: {
    eyebrow: 'Our writing',
    h2: 'Publications and articles',
    items: [
      {
        title: 'Diaper Fetishism: A Case Report',
        meta: ['Turkish Journal of Psychiatry', '2005 · 16(2):133–138'],
        authors: 'Dr Nihan Oğuz, Dr Niyazi Uygur',
      },
      {
        title: 'Delirium Due to Viral Encephalitis: A Case Report',
        meta: ['Case report'],
        authors: 'Nihan Oğuz, Cem İlnem, Ferhan Yener',
      },
      {
        title:
          'Psychiatric Presentations Caused by Brain Tumours: Two Case Reports',
        meta: ['Case report'],
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
        meta: ['Anadolu Journal of Psychiatry', '2014'],
        authors: 'Nihan Oğuz, Timuçin Oral, Mehmet Oğuz',
      },
      {
        title: 'Covid-19 and Mental Change: To Be or Not To Be!',
        meta: ['Blog post'],
        authors: 'Dr Mehmet Oğuz, MD',
      },
      {
        title: 'Do We Begin Life as a Blank Slate?',
        meta: ['Blog post'],
        authors: 'Dr Mehmet Oğuz, MD',
      },
    ],
  },

  contact: {
    eyebrow: 'Contact',
    h2: 'Book an appointment',
    intro:
      'You can request an appointment at the time that suits you best. Filling in the form prepares your message; you can edit it however you like before sending it.',
    labels: {
      address: 'Address',
      phone: 'Telephone',
      email: 'Email',
      languages: 'Languages spoken',
      social: 'Social media',
    },
    languagesValue: 'Türkçe · English · Deutsch · Français',
    imageAlt: '',
    form: {
      h3: 'Appointment request',
      note: 'Your message opens ready-written in WhatsApp or your email app. Whether to send it is up to you.',
      name: { label: 'Full name', placeholder: 'Your first and last name' },
      tel: {
        label: 'Telephone',
        optional: '(optional)',
        placeholder: '+90 5xx xxx xx xx',
      },
      mode: {
        label: 'Type of session',
        options: [
          'In person — Güzelbahçe',
          'Online — video call',
          'Either is fine',
        ],
      },
      msg: {
        label: 'Your message',
        placeholder:
          'A few sentences is plenty. We can go into the detail when we speak.',
      },
      sendWa: 'Open in WhatsApp',
      sendMail: 'Open in email',
      privacy:
        'This form sends nothing to any server; it only prepares message text on your own device. Your personal health data is recorded only with your explicit consent, under Turkish Personal Data Protection Law no. 6698 (KVKK) and the GDPR.',
    },
    message: {
      greeting: 'Hello, I would like to request an appointment.',
      name: 'Full name',
      tel: 'Telephone',
      mode: 'Type of session',
      subject: 'Appointment request',
    },
    map: {
      iframeTitle:
        'EMDR İzmir — map location for Yalı Mah. 268. Sk. No: 17, Güzelbahçe / İzmir',
      consentButton: 'Load the map',
      consentNote:
        'Opening the map loads Google Maps and shares your IP address with Google. To get directions without loading it, use the link below.',
      directions: 'Get directions',
    },
  },

  footer: {
    about:
      'A psychiatry and psychotherapy centre built on clear ethical standards, where evidence-based methods of therapy are practised. Güzelbahçe, İzmir.',
    pagesTitle: 'Sections',
    pages: [
      { href: '#emdr', label: 'What is EMDR' },
      { href: '#protokol', label: 'The eight-phase protocol' },
      { href: '#hizmetler', label: 'Our services' },
      { href: '#ekip', label: 'Our team' },
      { href: '#neden', label: 'Why EMDR' },
      { href: '#makaleler', label: 'Publications' },
    ],
    contactTitle: 'Contact',
    crisisHtml:
      '<b>In an emergency:</b> if you are having thoughts of harming yourself or someone else, please do not wait — call <b>112</b>, the emergency line in Turkey, or go to your nearest emergency department. This site is not a substitute for medical advice; diagnosis and treatment are given only after an in-person assessment.',
    rights: 'EMDR İzmir · All rights reserved.',
    kvkk:
      'Our KVKK/GDPR privacy notice and consent form are available at the practice.',
  },
};
