"""Writes site/i18n.json (UI strings, category intros, banner strings) for ar/en/fr/es/de.
Run once after editing; the build reads the JSON."""
import json, os

L = ('ar', 'en', 'fr', 'es', 'de')
UI = {}


def t(key, ar, en, fr, es, de):
    UI[key] = dict(zip(L, (ar, en, fr, es, de)))


t('skip', 'تخطَّ إلى المحتوى', 'Skip to content', 'Aller au contenu', 'Saltar al contenido', 'Zum Inhalt springen')
t('menu', 'القائمة', 'Menu', 'Menu', 'Menú', 'Menü')
t('nav_products', 'المنتجات', 'Products', 'Produits', 'Productos', 'Produkte')
t('nav_categories', 'الفئات', 'Categories', 'Catégories', 'Categorías', 'Kategorien')
t('nav_guides', 'أدلة الشراء', 'Buying guides', "Guides d'achat", 'Guías de compra', 'Kaufratgeber')
t('nav_about', 'من نحن', 'About', 'À propos', 'Quiénes somos', 'Über uns')
t('nav_privacy', 'الخصوصية', 'Privacy', 'Confidentialité', 'Privacidad', 'Datenschutz')
t('search_placeholder', 'ابحث عن جهاز…', 'Search devices…', 'Rechercher un appareil…', 'Buscar un dispositivo…', 'Gerät suchen…')
t('search_label', 'بحث', 'Search', 'Rechercher', 'Buscar', 'Suchen')
t('lang_label', 'اللغة', 'Language', 'Langue', 'Idioma', 'Sprache')
t('a11y_label', 'إمكانية الوصول', 'Accessibility', 'Accessibilité', 'Accesibilidad', 'Barrierefreiheit')
t('font_dec', 'تصغير الخط', 'Smaller text', 'Texte plus petit', 'Texto más pequeño', 'Kleinerer Text')
t('font_inc', 'تكبير الخط', 'Larger text', 'Texte plus grand', 'Texto más grande', 'Größerer Text')
t('comfort', 'وضع حماية العين', 'Eye comfort mode', 'Mode confort visuel', 'Modo protección visual', 'Augenschonmodus')
t('back_to_top', 'العودة للأعلى', 'Back to top', 'Haut de page', 'Volver arriba', 'Nach oben')

t('hero_eyebrow', 'اختيارات مستقلة للمنزل الذكي', 'Independent smart home picks',
  'Sélection indépendante de maison connectée', 'Selección independiente de hogar inteligente',
  'Unabhängige Smart-Home-Empfehlungen')
t('hero_title', 'ابنِ منزلًا أذكى دون أن تهدر مالك', 'Build a smarter home without wasting money',
  'Construisez une maison plus intelligente sans gaspiller votre argent',
  'Crea un hogar más inteligente sin malgastar dinero', 'Baue ein smarteres Zuhause, ohne Geld zu verschwenden')
t('hero_sub',
  'أجهزة منزل ذكي مختارة بعناية من AliExpress مع أدلة شراء صريحة عن الجهد والقوابس والبوابات وما يعمل معًا فعلًا.',
  'Hand-picked smart home devices from AliExpress with honest buying guides on voltage, plugs, hubs and what actually works together.',
  "Des appareils de maison connectée choisis avec soin sur AliExpress, avec des guides d'achat honnêtes sur la tension, les prises, les passerelles et ce qui fonctionne vraiment ensemble.",
  'Dispositivos de hogar inteligente seleccionados de AliExpress, con guías de compra sinceras sobre tensión, enchufes, pasarelas y qué funciona realmente junto.',
  'Handverlesene Smart-Home-Geräte von AliExpress mit ehrlichen Kaufratgebern zu Spannung, Steckern, Gateways und dem, was wirklich zusammenarbeitet.')
t('cta_browse', 'تصفّح المنتجات', 'Browse products', 'Parcourir les produits', 'Explorar productos', 'Produkte ansehen')
t('cta_guides', 'اقرأ أدلة الشراء', 'Read buying guides', "Lire les guides d'achat", 'Leer las guías de compra', 'Kaufratgeber lesen')

t('trust1_t', 'مستقلون', 'Independent', 'Indépendant', 'Independiente', 'Unabhängig')
t('trust1_d', 'لا نبيع شيئًا. تشتري مباشرة من المتجر.', 'We do not sell anything. You buy directly from the store.',
  'Nous ne vendons rien. Vous achetez directement auprès de la boutique.',
  'No vendemos nada. Compras directamente en la tienda.', 'Wir verkaufen nichts. Du kaufst direkt im Shop.')
t('trust2_t', 'أدلة صريحة', 'Honest guides', 'Guides honnêtes', 'Guías sinceras', 'Ehrliche Ratgeber')
t('trust2_d', 'نشرح الجهد والقوابس والبوابات قبل أن تطلب.', 'Voltage, plugs, hubs and gateways explained before you order.',
  'Tension, prises, hubs et passerelles expliqués avant de commander.',
  'Tensión, enchufes, hubs y pasarelas explicados antes de pedir.', 'Spannung, Stecker, Hubs und Gateways erklärt, bevor du bestellst.')
t('trust3_t', 'شفافية في العمولة', 'Clear about money', "Transparent sur l'argent", 'Claros con el dinero', 'Transparent bei Geld')
t('trust3_d', 'بعض الروابط تسويقية: قد نحصل على عمولة دون أي تكلفة إضافية عليك.',
  'Some links are affiliate links: we may earn a commission at no extra cost to you.',
  "Certains liens sont des liens d'affiliation : nous pouvons percevoir une commission sans frais supplémentaires pour vous.",
  'Algunos enlaces son de afiliados: podemos recibir una comisión sin coste adicional para ti.',
  'Einige Links sind Affiliate-Links: Wir erhalten möglicherweise eine Provision ohne Mehrkosten für dich.')
t('trust4_t', 'خمس لغات', 'Five languages', 'Cinq langues', 'Cinco idiomas', 'Fünf Sprachen')
LANGLINE = 'English · العربية · Français · Español · Deutsch'
t('trust4_d', LANGLINE, LANGLINE, LANGLINE, LANGLINE, LANGLINE)

t('sec_categories', 'تسوّق حسب الفئة', 'Shop by category', 'Parcourir par catégorie', 'Compra por categoría', 'Nach Kategorie stöbern')
t('sec_categories_sub', 'اعثر على الجهاز المناسب لكل غرفة.', 'Find the right device for every room.',
  "Trouvez l'appareil adapté à chaque pièce.", 'Encuentra el dispositivo adecuado para cada habitación.',
  'Finde das passende Gerät für jeden Raum.')
t('sec_latest', 'أحدث الاختيارات', 'Latest picks', 'Dernières sélections', 'Últimas selecciones', 'Neueste Empfehlungen')
t('sec_latest_sub', 'أُضيفت حديثًا إلى الكتالوج.', 'Recently added to the catalog.', 'Récemment ajoutés au catalogue.',
  'Añadidos recientemente al catálogo.', 'Kürzlich zum Katalog hinzugefügt.')
t('sec_guides_sub', 'نصائح عملية قبل أن تطلب.', 'Practical advice before you order.', 'Des conseils pratiques avant de commander.',
  'Consejos prácticos antes de pedir.', 'Praktische Tipps vor der Bestellung.')
t('sec_how', 'كيف نختار', 'How we choose', 'Comment nous choisissons', 'Cómo elegimos', 'So wählen wir aus')
t('how1_t', 'نختار ولا نعرض كل شيء', 'We shortlist, not list everything', 'Nous sélectionnons, nous ne listons pas tout',
  'Seleccionamos, no listamos todo', 'Wir wählen aus, statt alles aufzulisten')
t('how1_d', 'نبحث عن منتجات رائجة بتقييمات جيدة من المشترين، ثم نستبعد المكرر والعروض الضعيفة.',
  'We look for widely sold products with strong buyer ratings, then remove duplicates and weak listings.',
  'Nous cherchons des produits très vendus et bien notés par les acheteurs, puis écartons les doublons et les annonces faibles.',
  'Buscamos productos muy vendidos y bien valorados por los compradores, y descartamos duplicados y anuncios flojos.',
  'Wir suchen viel verkaufte Produkte mit guten Käuferbewertungen und sortieren Duplikate und schwache Angebote aus.')
t('how2_t', 'نقرأ إعلان المنتج بعناية', 'We read the listing carefully', 'Nous lisons attentivement la fiche',
  'Leemos la ficha con atención', 'Wir lesen das Angebot sorgfältig')
t('how2_d', 'الأوصاف مأخوذة من معلومات المتجر المعلنة. ولا نزعم أننا اختبرنا منتجًا ما لم نذكر ذلك.',
  "Descriptions come from the store's published information. We do not claim to have tested a product unless we say so.",
  "Les descriptions viennent des informations publiées par la boutique. Nous ne prétendons pas avoir testé un produit sauf mention contraire.",
  'Las descripciones proceden de la información publicada por la tienda. No afirmamos haber probado un producto salvo que lo indiquemos.',
  'Die Beschreibungen stammen aus den veröffentlichten Angaben des Shops. Wir behaupten nicht, ein Produkt getestet zu haben, es sei denn, wir sagen es.')
t('how3_t', 'ننبّه إلى ما يجب التحقق منه', 'We flag what to check', 'Nous signalons ce qu’il faut vérifier',
  'Señalamos lo que conviene comprobar', 'Wir weisen auf Prüfpunkte hin')
t('how3_d', 'نذكر الجهد ونوع القابس ومتطلبات البوابة ومخاطر التركيب حيث تهم.',
  'Voltage, plug type, hub requirements and installation risks are noted where they matter.',
  "Tension, type de prise, besoin d'un hub et risques d'installation sont indiqués là où c'est important.",
  'Tensión, tipo de enchufe, necesidad de hub y riesgos de instalación se indican donde importan.',
  'Spannung, Steckertyp, Hub-Bedarf und Installationsrisiken werden dort genannt, wo sie wichtig sind.')

t('view_all', 'عرض كل المنتجات', 'View all products', 'Voir tous les produits', 'Ver todos los productos', 'Alle Produkte ansehen')
t('read_guide', 'اقرأ الدليل', 'Read the guide', 'Lire le guide', 'Leer la guía', 'Ratgeber lesen')
t('view_details', 'التفاصيل', 'View details', 'Voir les détails', 'Ver detalles', 'Details ansehen')
t('view_store', 'عرض على AliExpress', 'View on AliExpress', 'Voir sur AliExpress', 'Ver en AliExpress', 'Auf AliExpress ansehen')
t('price_approx', 'السعر التقريبي', 'Approx. price', 'Prix approximatif', 'Precio aproximado', 'Ca.-Preis')
t('price_note',
  'سعر تقريبي وقت إضافتنا للمنتج. يتغير كثيرًا ويعتمد على بلدك والخيار الذي تختاره: تحقق من السعر الحالي على AliExpress.',
  'Approximate price when we added the product. It changes often and depends on your country and the option you choose: check the current price on AliExpress.',
  "Prix approximatif au moment de l'ajout du produit. Il change souvent et dépend de votre pays et de l'option choisie : vérifiez le prix actuel sur AliExpress.",
  'Precio aproximado cuando añadimos el producto. Cambia a menudo y depende de tu país y de la opción elegida: comprueba el precio actual en AliExpress.',
  'Ungefährer Preis zum Zeitpunkt, als wir das Produkt hinzugefügt haben. Er ändert sich oft und hängt von deinem Land und der gewählten Variante ab: Prüfe den aktuellen Preis auf AliExpress.')
t('price_note_short', 'الأسعار تقريبية وتتغير: تحقق منها على AliExpress.',
  'Prices are approximate and change often: check them on AliExpress.',
  'Les prix sont approximatifs et changent souvent : vérifiez-les sur AliExpress.',
  'Los precios son aproximados y cambian a menudo: compruébalos en AliExpress.',
  'Preise sind ungefähr und ändern sich oft: Prüfe sie auf AliExpress.')
t('affiliate_note', 'قد نحصل على عمولة إن اشتريت عبر هذا الرابط دون أي تكلفة إضافية عليك.',
  'We may earn a commission if you buy through this link, at no extra cost to you.',
  'Nous pouvons percevoir une commission si vous achetez via ce lien, sans frais supplémentaires pour vous.',
  'Podemos recibir una comisión si compras a través de este enlace, sin coste adicional para ti.',
  'Wir erhalten möglicherweise eine Provision, wenn du über diesen Link kaufst, ohne Mehrkosten für dich.')
t('breadcrumb_home', 'الرئيسية', 'Home', 'Accueil', 'Inicio', 'Startseite')
t('before_buy', 'قبل أن تشتري', 'Before you buy', "Avant d'acheter", 'Antes de comprar', 'Bevor du kaufst')
t('before1', 'تحقق من جهد الكهرباء ونوع القابس في بلدك.', 'Check the voltage and plug type for your country.',
  'Vérifiez la tension et le type de prise de votre pays.', 'Comprueba la tensión y el tipo de enchufe de tu país.',
  'Prüfe Spannung und Steckertyp für dein Land.')
t('before2', 'اقرأ تقييمات المتجر والخيارات وتفاصيل الشحن.', 'Read the store reviews, options and shipping details.',
  'Lisez les avis, les options et les détails de livraison de la boutique.',
  'Lee las reseñas, las opciones y los detalles de envío de la tienda.',
  'Lies die Bewertungen, Varianten und Versandangaben im Shop.')
t('before3', 'تأكد من السعر الحالي والتوفر في صفحة المتجر.', 'Confirm the current price and availability on the store page.',
  'Confirmez le prix et la disponibilité actuels sur la page de la boutique.',
  'Confirma el precio y la disponibilidad actuales en la página de la tienda.',
  'Bestätige aktuellen Preis und Verfügbarkeit auf der Shop-Seite.')
t('related_guide', 'دليل ذو صلة', 'Related guide', 'Guide associé', 'Guía relacionada', 'Passender Ratgeber')
t('related_products', 'منتجات ذات صلة', 'Related products', 'Produits similaires', 'Productos relacionados', 'Ähnliche Produkte')
t('guide_products', 'منتجات ذات صلة بهذا الدليل', 'Products related to this guide', 'Produits liés à ce guide',
  'Productos relacionados con esta guía', 'Produkte zu diesem Ratgeber')
t('all_guides', 'كل الأدلة', 'All guides', 'Tous les guides', 'Todas las guías', 'Alle Ratgeber')
t('products_count', '{n} منتج', '{n} products', '{n} produits', '{n} productos', '{n} Produkte')
t('all_products', 'كل المنتجات', 'All products', 'Tous les produits', 'Todos los productos', 'Alle Produkte')
t('filter_placeholder', 'صفِّ المنتجات…', 'Filter products…', 'Filtrer les produits…', 'Filtrar productos…', 'Produkte filtern…')
t('no_results', 'لا توجد منتجات مطابقة لبحثك. جرّب كلمة أخرى.', 'No products match your search. Try another word.',
  'Aucun produit ne correspond à votre recherche. Essayez un autre terme.',
  'Ningún producto coincide con tu búsqueda. Prueba con otro término.',
  'Keine Produkte gefunden. Versuche einen anderen Suchbegriff.')
t('chip_all', 'الكل', 'All', 'Tout', 'Todo', 'Alle')

t('footer_tag', 'اختيارات مستقلة للمنزل الذكي وأدلة شراء.', 'Independent smart home picks and buying guides.',
  "Sélection indépendante de maison connectée et guides d'achat.",
  'Selección independiente de hogar inteligente y guías de compra.',
  'Unabhängige Smart-Home-Empfehlungen und Kaufratgeber.')
t('footer_explore', 'استكشف', 'Explore', 'Explorer', 'Explorar', 'Entdecken')
t('footer_site', 'الموقع', 'Site', 'Site', 'Sitio', 'Website')
t('footer_follow', 'تابعنا', 'Follow us', 'Suivez-nous', 'Síguenos', 'Folge uns')
t('disclosure',
  'إفصاح: هذا الموقع يشارك في برامج تسويق بالعمولة (مثل AliExpress Affiliate)، وقد نحصل على عمولة عند الشراء عبر روابطنا دون أي تكلفة إضافية عليك.',
  'Disclosure: this site participates in affiliate programs (such as the AliExpress Affiliate Program) and may earn a commission on purchases made through our links at no extra cost to you.',
  "Divulgation : ce site participe à des programmes d'affiliation (comme AliExpress Affiliate) et peut percevoir une commission sur les achats effectués via nos liens, sans coût supplémentaire pour vous.",
  'Divulgación: este sitio participa en programas de afiliados (como AliExpress Affiliate) y puede recibir una comisión por las compras realizadas a través de nuestros enlaces, sin coste adicional para ti.',
  'Offenlegung: Diese Website nimmt an Partnerprogrammen teil (z. B. AliExpress Affiliate) und erhält ggf. eine Provision für Käufe über unsere Links, ohne Mehrkosten für dich.')
t('not_found_title', 'الصفحة غير موجودة', 'Page not found', 'Page introuvable', 'Página no encontrada', 'Seite nicht gefunden')
t('not_found_text', 'الصفحة التي تبحث عنها غير موجودة أو نُقلت.', 'The page you are looking for does not exist or has moved.',
  "La page que vous cherchez n'existe pas ou a été déplacée.", 'La página que buscas no existe o se ha movido.',
  'Die gesuchte Seite existiert nicht oder wurde verschoben.')
t('go_home', 'العودة إلى الرئيسية', 'Back to home', "Retour à l'accueil", 'Volver al inicio', 'Zurück zur Startseite')
t('site_title', 'Smart Casa (بيتي الذكي) — اختيارات المنزل الذكي وأدلة الشراء',
  'Smart Casa — Smart home picks and buying guides', "Smart Casa — Sélection maison connectée et guides d'achat",
  'Smart Casa — Selección de hogar inteligente y guías de compra', 'Smart Casa — Smart-Home-Empfehlungen und Kaufratgeber')
t('site_desc', 'أجهزة منزل ذكي مختارة من AliExpress مع أدلة شراء صريحة عن الجهد والقوابس والبوابات والتوافق.',
  'Hand-picked smart home devices from AliExpress with honest buying guides on voltage, plugs, hubs and compatibility.',
  "Appareils de maison connectée choisis sur AliExpress, avec des guides d'achat honnêtes sur la tension, les prises, les passerelles et la compatibilité.",
  'Dispositivos de hogar inteligente seleccionados de AliExpress, con guías de compra sinceras sobre tensión, enchufes, pasarelas y compatibilidad.',
  'Handverlesene Smart-Home-Geräte von AliExpress mit ehrlichen Kaufratgebern zu Spannung, Steckern, Gateways und Kompatibilität.')

CAT = {}


def c(cid, ar, en, fr, es, de):
    CAT[cid] = dict(zip(L, (ar, en, fr, es, de)))


c('lighting', 'مصابيح وشرائط LED ولمبات ذكية تعتّمها وتجدولها وتلوّنها من هاتفك. تحقق من جهد الكهرباء ونوع القاعدة قبل الطلب.',
  'Smart bulbs, LED strips and lamps you can dim, schedule and colour from your phone. Check your voltage and bulb base before ordering.',
  'Ampoules, rubans LED et lampes connectés que vous pouvez varier, programmer et colorer depuis votre téléphone. Vérifiez votre tension et votre culot avant de commander.',
  'Bombillas, tiras LED y lámparas inteligentes que puedes regular, programar y colorear desde el móvil. Comprueba tu tensión y el casquillo antes de pedir.',
  'Smarte Lampen, LED-Streifen und Leuchten, die du per Handy dimmen, zeitlich steuern und einfärben kannst. Prüfe vor der Bestellung Spannung und Sockel.')
c('security', 'كاميرات وإنذارات وصفارات وكاشفات دخان وغاز وأقفال ذكية لمراقبة منزلك. الكاشفات طبقة أمان إضافية وليست بديلًا عن الأجهزة المعتمدة.',
  'Cameras, alarms, sirens, smoke and gas detectors and smart locks to keep an eye on your home. Detectors are an extra layer, not a replacement for certified alarms.',
  "Caméras, alarmes, sirènes, détecteurs de fumée et de gaz et serrures connectées pour garder un œil sur votre maison. Les détecteurs sont une protection supplémentaire, pas un remplaçant d'alarmes certifiées.",
  'Cámaras, alarmas, sirenas, detectores de humo y gas y cerraduras inteligentes para vigilar tu casa. Los detectores son una capa extra, no un sustituto de alarmas certificadas.',
  'Kameras, Alarme, Sirenen, Rauch- und Gasmelder und smarte Schlösser, um dein Zuhause im Blick zu behalten. Melder sind eine zusätzliche Ebene und kein Ersatz für zertifizierte Alarme.')
c('power', 'مقابس ذكية وعدادات طاقة ووحدات كهرباء لتشغيل الأجهزة ومعرفة استهلاكها. التزم بالحمل الأقصى لكل جهاز.',
  "Smart plugs, energy meters and power modules to switch appliances and see what they consume. Stay within each device's rated load.",
  "Prises connectées, compteurs d'énergie et modules d'alimentation pour piloter vos appareils et suivre leur consommation. Respectez la charge nominale de chaque appareil.",
  'Enchufes inteligentes, medidores de energía y módulos de potencia para encender aparatos y ver cuánto consumen. Respeta la carga nominal de cada dispositivo.',
  'Smarte Steckdosen, Energiemessgeräte und Leistungsmodule, um Geräte zu schalten und ihren Verbrauch zu sehen. Halte die Nennlast jedes Geräts ein.')
c('control', 'مفاتيح جدارية وريليهات وأجهزة تحكم ومحركات ستائر لأتمتة ما تملكه أصلًا. الأجهزة الموصولة بالأسلاك يُفضَّل أن يركّبها كهربائي.',
  'Wall switches, relays, remotes and curtain motors to automate what you already own. Wired devices should be installed by an electrician.',
  'Interrupteurs muraux, relais, télécommandes et moteurs de rideaux pour automatiser ce que vous possédez déjà. Les appareils câblés doivent être installés par un électricien.',
  'Interruptores de pared, relés, mandos y motores de cortinas para automatizar lo que ya tienes. Los dispositivos cableados deben instalarlos un electricista.',
  'Wandschalter, Relais, Fernbedienungen und Vorhangmotoren, um Vorhandenes zu automatisieren. Fest verdrahtete Geräte sollte ein Elektriker installieren.')
c('sensors', 'حساسات حركة وحرارة ورطوبة وتسرّب مياه وإضاءة تشغّل الأتمتة وترسل التنبيهات.',
  'Motion, temperature, humidity, water-leak and light sensors that trigger automations and send alerts.',
  "Capteurs de mouvement, de température, d'humidité, de fuite d'eau et de lumière qui déclenchent des automatisations et envoient des alertes.",
  'Sensores de movimiento, temperatura, humedad, fugas de agua y luz que activan automatizaciones y envían avisos.',
  'Bewegungs-, Temperatur-, Feuchte-, Wasser- und Lichtsensoren, die Automatisierungen auslösen und Meldungen senden.')
c('audio', 'سماعات ومحوّلات صوت للموسيقى في أرجاء المنزل.', 'Speakers and audio adapters for music around the house.',
  'Enceintes et adaptateurs audio pour la musique dans toute la maison.',
  'Altavoces y adaptadores de audio para la música por toda la casa.', 'Lautsprecher und Audioadapter für Musik im ganzen Haus.')
c('garden', 'ري وإضاءة شمسية ومستلزمات خارجية للحديقة والشرفة.', 'Watering, solar lights and outdoor gear for the garden and balcony.',
  "Arrosage, éclairage solaire et équipements d'extérieur pour le jardin et le balcon.",
  'Riego, luces solares y equipamiento exterior para el jardín y el balcón.',
  'Bewässerung, Solarleuchten und Outdoor-Zubehör für Garten und Balkon.')
c('climate', 'ثرموستات وصمامات مشعات وأجهزة تحكم بالمكيّفات لراحة الغرف وتقليل الهدر.',
  'Thermostats, radiator valves and air-conditioner controls to keep rooms comfortable and cut waste.',
  'Thermostats, vannes de radiateur et commandes de climatiseur pour garder les pièces confortables et limiter le gaspillage.',
  'Termostatos, válvulas de radiador y mandos de aire acondicionado para mantener las habitaciones confortables y reducir el desperdicio.',
  'Thermostate, Heizkörperventile und Klimaanlagen-Fernbedienungen für behagliche Räume und weniger Verschwendung.')
c('pets', 'مغذّيات ونوافير وألعاب تُبقي حيواناتك الأليفة مُطعمة ومشغولة وأنت منشغل أو غائب.',
  'Feeders, fountains and toys that keep pets fed and entertained while you are busy or away.',
  'Distributeurs, fontaines et jouets qui gardent vos animaux nourris et occupés quand vous êtes pris ou absent.',
  'Comederos, fuentes y juguetes que mantienen a tus mascotas alimentadas y entretenidas mientras estás ocupado o fuera.',
  'Futterautomaten, Brunnen und Spielzeug, die Haustiere versorgt und beschäftigt halten, wenn du beschäftigt oder unterwegs bist.')
c('network', 'راوترات ومكرّرات ومحوّلات ومعدات Zigbee تُبقي شبكة منزلك وأجهزتك الذكية متصلة.',
  'Routers, repeaters, adapters and Zigbee gear that keep your home network and smart devices connected.',
  'Routeurs, répéteurs, adaptateurs et équipements Zigbee qui maintiennent votre réseau domestique et vos appareils connectés.',
  'Routers, repetidores, adaptadores y equipos Zigbee que mantienen conectadas tu red doméstica y tus dispositivos inteligentes.',
  'Router, Repeater, Adapter und Zigbee-Zubehör, die dein Heimnetz und deine smarten Geräte verbunden halten.')
c('misc', 'أجهزة مفيدة أخرى لم تجد لها فئة مناسبة.', 'Other useful gadgets that did not fit anywhere else.',
  "D'autres gadgets utiles qui ne rentraient dans aucune autre catégorie.",
  'Otros gadgets útiles que no encajaban en ninguna otra categoría.', 'Weitere nützliche Gadgets, die in keine andere Kategorie passten.')

BANNER = {
    'ar': {'text': 'هل تفضّل قراءة الموقع بالعربية؟', 'go': 'العربية', 'close': 'إغلاق'},
    'en': {'text': 'Prefer to read this site in English?', 'go': 'English', 'close': 'Close'},
    'fr': {'text': 'Préférez-vous lire ce site en français ?', 'go': 'Français', 'close': 'Fermer'},
    'es': {'text': '¿Prefieres leer este sitio en español?', 'go': 'Español', 'close': 'Cerrar'},
    'de': {'text': 'Möchtest du diese Website auf Deutsch lesen?', 'go': 'Deutsch', 'close': 'Schließen'},
}

out = {'ui': UI, 'cat_intro': CAT, 'banner': BANNER}
for k, v in UI.items():
    assert all(v[l] for l in L), k
for k, v in CAT.items():
    assert all(v[l] for l in L), k
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'i18n.json')
json.dump(out, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', path, '| ui keys:', len(UI), '| categories:', len(CAT))
