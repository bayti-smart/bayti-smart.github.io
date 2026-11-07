# -*- coding: utf-8 -*-
# دليلان جديدان مرتبطان بقسم الدورات. {C} يُستبدل برابط صفحة الدورات بحسب اللغة.
TITLES = {
 "start": {"ar": "المنزل الذكي للمبتدئين: من أين تبدأ", "en": "Smart home for beginners: where to start",
           "fr": "Maison connectée pour débutants : par où commencer", "es": "Hogar inteligente para principiantes: por dónde empezar",
           "de": "Smart Home für Einsteiger: womit du anfängst"},
 "network": {"ar": "أساسيات شبكة المنزل للأجهزة الذكية", "en": "Home network basics for smart devices",
             "fr": "Bases du réseau domestique pour les appareils connectés", "es": "Conceptos básicos de la red doméstica para dispositivos inteligentes",
             "de": "Heimnetzwerk-Grundlagen für Smart-Home-Geräte"},
}

BODY = {}
BODY[("start", "en")] = """<p>You do not need to buy everything at once. A good first smart home is three or four devices that solve one real problem, run from one app, so you can see whether you actually use them.</p>
<h2>Pick one app first</h2>
<p>Many low-cost devices work through the Tuya / Smart Life app, others use their own app, and some use Zigbee with a gateway. Mixing many apps is the most common reason a smart home feels annoying. Choose one app, and one voice assistant such as Alexa or Google Home if you want voice control, then check compatibility on each product page.</p>
<h2>A sensible first set</h2>
<ul>
<li><strong>A smart plug or bulb:</strong> the easiest way to learn schedules and scenes.</li>
<li><strong>A door/window or motion sensor:</strong> lets something happen automatically, such as a light turning on.</li>
<li><strong>A camera:</strong> only if you have a clear place and reason for it.</li>
<li><strong>A Zigbee gateway:</strong> only when you plan more than a few sensors.</li>
</ul>
<h2>Learn more</h2>
<p>To go further into IoT, electronics or home networking, see our <a href="{C}">courses section</a>, which lists Coursera courses on these topics. We have not reviewed them, so check each course page for level, language and price.</p>
<h2>Questions people ask</h2>
<h3>How much should I spend first?</h3>
<p>Start small with one or two low-cost devices. Prices on this site are approximate and change, so check the store page before ordering.</p>
<h3>Do I need to program anything?</h3>
<p>No. Most devices are set up from an app. Programming only matters for advanced projects such as Arduino or Home Assistant.</p>
<h3>Is it safe to order from an overseas store?</h3>
<p>Check the seller's rating, the plug type and voltage, and the return terms. Our guides on plugs and electrical work cover the safety points.</p>
"""
BODY[("start", "ar")] = """<p>لا تحتاج أن تشتري كل شيء دفعة واحدة. أفضل بداية للمنزل الذكي ثلاثة أو أربعة أجهزة تحل مشكلة واحدة حقيقية، وتعمل من تطبيق واحد، لتعرف هل تستخدمها فعلًا.</p>
<h2>اختر تطبيقًا واحدًا أولًا</h2>
<p>كثير من الأجهزة الرخيصة تعمل عبر تطبيق Tuya / Smart Life، وبعضها له تطبيقه الخاص، وبعضها يعمل بـZigbee مع بوابة. خلط تطبيقات كثيرة هو أشيع سبب لشعورك بأن منزلك الذكي مزعج. اختر تطبيقًا واحدًا، ومساعدًا صوتيًا واحدًا مثل Alexa أو Google Home إن أردت التحكم بالصوت، ثم راجع التوافق في صفحة كل منتج.</p>
<h2>مجموعة أولى معقولة</h2>
<ul>
<li><strong>مقبس ذكي أو مصباح:</strong> أسهل طريقة لتعلّم الجداول والمشاهد.</li>
<li><strong>حساس باب/نافذة أو حركة:</strong> يجعل شيئًا يحدث تلقائيًا، كإضاءة مصباح.</li>
<li><strong>كاميرا:</strong> فقط إن كان لها مكان وسبب واضحان.</li>
<li><strong>بوابة Zigbee:</strong> فقط حين تخطط لأكثر من بضعة حساسات.</li>
</ul>
<h2>للتعلّم أكثر</h2>
<p>للتعمق في إنترنت الأشياء أو الإلكترونيات أو شبكات المنزل، اطّلع على <a href="{C}">قسم الدورات</a> الذي يعرض دورات Coursera في هذه المواضيع. لم نراجعها، فراجع صفحة كل دورة لمعرفة المستوى واللغة والسعر.</p>
<h2>أسئلة يطرحها الناس</h2>
<h3>كم أنفق في البداية؟</h3>
<p>ابدأ بقليل: جهاز أو جهازان رخيصان. الأسعار في هذا الموقع تقريبية وتتغير، فراجع صفحة المتجر قبل الطلب.</p>
<h3>هل أحتاج إلى البرمجة؟</h3>
<p>لا. معظم الأجهزة تُضبط من تطبيق. البرمجة تهم المشاريع المتقدمة فقط مثل Arduino أو Home Assistant.</p>
<h3>هل الطلب من متجر خارج بلدي آمن؟</h3>
<p>راجع تقييم البائع ونوع القابس والجهد وشروط الإرجاع. دليلا المقابس والكهرباء عندنا يغطيان نقاط السلامة.</p>
"""
BODY[("start", "fr")] = """<p>Inutile de tout acheter d'un coup. Une bonne première maison connectée, ce sont trois ou quatre appareils qui résolvent un vrai problème, pilotés depuis une seule application, pour voir si vous les utilisez vraiment.</p>
<h2>Choisissez d'abord une application</h2>
<p>Beaucoup d'appareils bon marché fonctionnent avec l'application Tuya / Smart Life, d'autres ont leur propre application, et certains utilisent Zigbee avec une passerelle. Multiplier les applications est la cause la plus fréquente d'agacement. Choisissez une application, et un assistant vocal comme Alexa ou Google Home si vous voulez la commande vocale, puis vérifiez la compatibilité sur chaque page produit.</p>
<h2>Un premier ensemble raisonnable</h2>
<ul>
<li><strong>Une prise ou une ampoule connectée :</strong> le moyen le plus simple d'apprendre programmations et scénarios.</li>
<li><strong>Un capteur d'ouverture ou de mouvement :</strong> déclenche automatiquement une action, comme allumer une lumière.</li>
<li><strong>Une caméra :</strong> seulement si vous avez un emplacement et une raison claire.</li>
<li><strong>Une passerelle Zigbee :</strong> seulement si vous prévoyez plus de quelques capteurs.</li>
</ul>
<h2>Pour aller plus loin</h2>
<p>Pour approfondir l'IoT, l'électronique ou les réseaux domestiques, consultez notre <a href="{C}">section cours</a>, qui liste des cours Coursera sur ces sujets. Nous ne les avons pas examinés : vérifiez sur la page de chaque cours le niveau, la langue et le prix.</p>
<h2>Questions fréquentes</h2>
<h3>Combien dépenser au départ ?</h3>
<p>Commencez petit avec un ou deux appareils bon marché. Les prix de ce site sont approximatifs et changent, vérifiez la page de la boutique avant de commander.</p>
<h3>Faut-il programmer ?</h3>
<p>Non. La plupart des appareils se configurent depuis une application. La programmation ne concerne que les projets avancés comme Arduino ou Home Assistant.</p>
<h3>Est-il sûr de commander sur une boutique étrangère ?</h3>
<p>Vérifiez la note du vendeur, le type de fiche et la tension, ainsi que les conditions de retour. Nos guides sur les prises et l'électricité couvrent les points de sécurité.</p>
"""
BODY[("start", "es")] = """<p>No necesitas comprarlo todo de una vez. Un buen primer hogar inteligente son tres o cuatro dispositivos que resuelven un problema real, manejados desde una sola app, para ver si de verdad los usas.</p>
<h2>Elige primero una app</h2>
<p>Muchos dispositivos baratos funcionan con la app Tuya / Smart Life, otros tienen su propia app y algunos usan Zigbee con una pasarela. Mezclar muchas apps es la causa más común de que un hogar inteligente resulte molesto. Elige una app y, si quieres control por voz, un asistente como Alexa o Google Home; luego comprueba la compatibilidad en la página de cada producto.</p>
<h2>Un primer conjunto razonable</h2>
<ul>
<li><strong>Un enchufe o una bombilla inteligente:</strong> la forma más fácil de aprender horarios y escenas.</li>
<li><strong>Un sensor de puerta/ventana o de movimiento:</strong> hace que algo ocurra solo, como encender una luz.</li>
<li><strong>Una cámara:</strong> solo si tienes un lugar y un motivo claros.</li>
<li><strong>Una pasarela Zigbee:</strong> solo cuando planees más de unos pocos sensores.</li>
</ul>
<h2>Para aprender más</h2>
<p>Para profundizar en IoT, electrónica o redes domésticas, mira nuestra <a href="{C}">sección de cursos</a>, que lista cursos de Coursera sobre estos temas. No los hemos revisado, así que comprueba en la página de cada curso el nivel, el idioma y el precio.</p>
<h2>Preguntas frecuentes</h2>
<h3>¿Cuánto gasto al principio?</h3>
<p>Empieza poco a poco con uno o dos dispositivos baratos. Los precios de este sitio son aproximados y cambian, así que revisa la página de la tienda antes de pedir.</p>
<h3>¿Necesito programar?</h3>
<p>No. La mayoría de los dispositivos se configuran desde una app. Programar solo importa en proyectos avanzados como Arduino o Home Assistant.</p>
<h3>¿Es seguro pedir a una tienda del extranjero?</h3>
<p>Comprueba la valoración del vendedor, el tipo de clavija y el voltaje, y las condiciones de devolución. Nuestras guías de enchufes y de instalación eléctrica cubren los puntos de seguridad.</p>
"""
BODY[("start", "de")] = """<p>Du musst nicht alles auf einmal kaufen. Ein guter erster Smart-Home-Start sind drei oder vier Geräte, die ein echtes Problem lösen und über eine App laufen, damit du siehst, ob du sie wirklich nutzt.</p>
<h2>Wähle zuerst eine App</h2>
<p>Viele günstige Geräte arbeiten mit der Tuya / Smart Life App, andere haben eine eigene App, manche nutzen Zigbee mit einem Gateway. Zu viele verschiedene Apps sind der häufigste Grund, warum sich ein Smart Home lästig anfühlt. Wähle eine App und, wenn du Sprachsteuerung willst, einen Assistenten wie Alexa oder Google Home, und prüfe die Kompatibilität auf jeder Produktseite.</p>
<h2>Ein vernünftiges erstes Set</h2>
<ul>
<li><strong>Eine smarte Steckdose oder Lampe:</strong> der einfachste Weg, Zeitpläne und Szenen zu lernen.</li>
<li><strong>Ein Tür-/Fenster- oder Bewegungssensor:</strong> löst automatisch etwas aus, etwa das Einschalten eines Lichts.</li>
<li><strong>Eine Kamera:</strong> nur, wenn du einen klaren Ort und Grund dafür hast.</li>
<li><strong>Ein Zigbee-Gateway:</strong> nur, wenn du mehr als ein paar Sensoren planst.</li>
</ul>
<h2>Mehr lernen</h2>
<p>Wenn du dich in IoT, Elektronik oder Heimnetzwerke vertiefen willst, schau in unseren <a href="{C}">Kursbereich</a>, der Coursera-Kurse zu diesen Themen auflistet. Wir haben sie nicht geprüft, achte also auf der Seite jedes Kurses auf Niveau, Sprache und Preis.</p>
<h2>Häufige Fragen</h2>
<h3>Wie viel sollte ich zuerst ausgeben?</h3>
<p>Fang klein an, mit ein oder zwei günstigen Geräten. Die Preise auf dieser Seite sind ungefähr und ändern sich, prüfe also die Shop-Seite vor der Bestellung.</p>
<h3>Muss ich programmieren?</h3>
<p>Nein. Die meisten Geräte richtest du per App ein. Programmieren braucht man nur für fortgeschrittene Projekte wie Arduino oder Home Assistant.</p>
<h3>Ist die Bestellung bei einem Shop im Ausland sicher?</h3>
<p>Prüfe die Bewertung des Verkäufers, Steckertyp und Spannung sowie die Rückgabebedingungen. Unsere Ratgeber zu Steckdosen und Elektroinstallation behandeln die Sicherheitspunkte.</p>
"""
BODY[("network", "en")] = """<p>Most smart-home problems are network problems. A few habits keep your devices connected and your home network safer.</p>
<h2>What to check</h2>
<ul>
<li><strong>2.4 GHz:</strong> many low-cost Wi-Fi devices only work on 2.4 GHz. If your router shows 2.4 and 5 GHz under one name, setup can fail; connect the phone to 2.4 GHz while pairing.</li>
<li><strong>Router position:</strong> place it centrally, away from metal and thick walls. Distance and walls matter more than headline speed.</li>
<li><strong>Guest network:</strong> if your router offers one, put smart devices there to keep them apart from your computers and phones.</li>
<li><strong>Passwords:</strong> change default passwords, use a strong Wi-Fi password, and keep the router firmware up to date.</li>
<li><strong>No open ports:</strong> do not expose cameras or devices to the internet; use the maker's app or a secure remote-access option.</li>
</ul>
<h2>Common mistakes</h2>
<ul>
<li>Pairing a device while the phone is on a 5 GHz-only network.</li>
<li>Leaving the router in a cabinet or a far corner, then blaming the device.</li>
<li>Keeping the default password on a camera or hub.</li>
</ul>
<h2>Learn more</h2>
<p>For a deeper start on networks and security, see our <a href="{C}">courses section</a>, which lists Coursera courses on these topics. We have not reviewed them, so check each course page.</p>
<h2>Questions people ask</h2>
<h3>Why does my device not connect during setup?</h3>
<p>Most often the phone is on a 5 GHz network, or the signal at the device is weak. Move closer to the router and try again.</p>
<h3>Do I need a mesh Wi-Fi system?</h3>
<p>Only if some rooms have weak signal after you reposition the router. For a small flat, one router is usually enough.</p>
<h3>What is a guest network for?</h3>
<p>It keeps devices you trust less, such as cheap cameras, on a separate network from your computers and phones.</p>
"""
BODY[("network", "ar")] = """<p>معظم مشاكل المنزل الذكي هي مشاكل شبكة. بضع عادات تُبقي أجهزتك متصلة وشبكة بيتك أكثر أمانًا.</p>
<h2>ما الذي تتحقق منه</h2>
<ul>
<li><strong>2.4 غيغاهرتز:</strong> كثير من أجهزة Wi-Fi الرخيصة تعمل على 2.4 غيغاهرتز فقط. إن كان الراوتر يعرض 2.4 و5 غيغاهرتز باسم واحد فقد يفشل الإعداد؛ صِل الهاتف بـ2.4 أثناء الاقتران.</li>
<li><strong>مكان الراوتر:</strong> ضعه في موضع مركزي بعيدًا عن المعادن والجدران السميكة. المسافة والجدران أهم من السرعة المعلنة.</li>
<li><strong>شبكة الضيوف:</strong> إن وفّرها الراوتر فضع فيها الأجهزة الذكية لتبقى بعيدة عن حواسيبك وهواتفك.</li>
<li><strong>كلمات السر:</strong> غيّر الافتراضية، واستخدم كلمة سر قوية للواي فاي، وحدّث برنامج الراوتر.</li>
<li><strong>لا منافذ مفتوحة:</strong> لا تعرّض الكاميرات والأجهزة للإنترنت؛ استخدم تطبيق الشركة أو وصولًا عن بُعد آمنًا.</li>
</ul>
<h2>أخطاء شائعة</h2>
<ul>
<li>إقران جهاز والهاتف على شبكة 5 غيغاهرتز فقط.</li>
<li>ترك الراوتر في خزانة أو زاوية بعيدة ثم لوم الجهاز.</li>
<li>إبقاء كلمة السر الافتراضية على كاميرا أو هَب.</li>
</ul>
<h2>للتعلّم أكثر</h2>
<p>لبداية أعمق في الشبكات والأمان، اطّلع على <a href="{C}">قسم الدورات</a> الذي يعرض دورات Coursera في هذه المواضيع. لم نراجعها، فراجع صفحة كل دورة.</p>
<h2>أسئلة يطرحها الناس</h2>
<h3>لماذا لا يتصل جهازي أثناء الإعداد؟</h3>
<p>غالبًا يكون الهاتف على شبكة 5 غيغاهرتز، أو الإشارة عند الجهاز ضعيفة. اقترب من الراوتر وأعد المحاولة.</p>
<h3>هل أحتاج إلى نظام Wi-Fi شبكي (Mesh)؟</h3>
<p>فقط إن بقيت غرف ضعيفة الإشارة بعد تغيير مكان الراوتر. لشقة صغيرة يكفي غالبًا راوتر واحد.</p>
<h3>ما فائدة شبكة الضيوف؟</h3>
<p>تُبقي الأجهزة الأقل ثقة، مثل الكاميرات الرخيصة، على شبكة منفصلة عن حواسيبك وهواتفك.</p>
"""
BODY[("network", "fr")] = """<p>La plupart des problèmes de maison connectée sont des problèmes de réseau. Quelques habitudes gardent vos appareils connectés et votre réseau domestique plus sûr.</p>
<h2>Ce qu'il faut vérifier</h2>
<ul>
<li><strong>2,4 GHz :</strong> beaucoup d'appareils Wi-Fi bon marché ne fonctionnent qu'en 2,4 GHz. Si votre routeur affiche 2,4 et 5 GHz sous un même nom, la configuration peut échouer ; connectez le téléphone en 2,4 GHz pendant l'appairage.</li>
<li><strong>Position du routeur :</strong> placez-le au centre, loin du métal et des murs épais. Distance et murs comptent plus que le débit annoncé.</li>
<li><strong>Réseau invité :</strong> si votre routeur en propose un, mettez-y les appareils connectés pour les séparer de vos ordinateurs et téléphones.</li>
<li><strong>Mots de passe :</strong> changez ceux par défaut, utilisez un mot de passe Wi-Fi robuste et gardez le micrologiciel du routeur à jour.</li>
<li><strong>Pas de ports ouverts :</strong> n'exposez pas caméras ni appareils sur internet ; utilisez l'application du fabricant ou un accès à distance sécurisé.</li>
</ul>
<h2>Erreurs fréquentes</h2>
<ul>
<li>Appairer un appareil alors que le téléphone est sur un réseau uniquement 5 GHz.</li>
<li>Laisser le routeur dans un meuble ou un coin éloigné, puis accuser l'appareil.</li>
<li>Garder le mot de passe par défaut sur une caméra ou un hub.</li>
</ul>
<h2>Pour aller plus loin</h2>
<p>Pour une base plus solide en réseaux et sécurité, consultez notre <a href="{C}">section cours</a>, qui liste des cours Coursera sur ces sujets. Nous ne les avons pas examinés : vérifiez la page de chaque cours.</p>
<h2>Questions fréquentes</h2>
<h3>Pourquoi mon appareil ne se connecte-t-il pas à la configuration ?</h3>
<p>Le plus souvent, le téléphone est sur un réseau 5 GHz ou le signal est faible près de l'appareil. Rapprochez-vous du routeur et réessayez.</p>
<h3>Ai-je besoin d'un système Wi-Fi Mesh ?</h3>
<p>Seulement si certaines pièces restent mal couvertes après avoir déplacé le routeur. Pour un petit appartement, un routeur suffit en général.</p>
<h3>À quoi sert un réseau invité ?</h3>
<p>Il garde les appareils auxquels vous faites moins confiance, comme des caméras bon marché, sur un réseau séparé de vos ordinateurs et téléphones.</p>
"""
BODY[("network", "es")] = """<p>La mayoría de los problemas del hogar inteligente son problemas de red. Unos pocos hábitos mantienen tus dispositivos conectados y tu red doméstica más segura.</p>
<h2>Qué comprobar</h2>
<ul>
<li><strong>2,4 GHz:</strong> muchos dispositivos Wi-Fi baratos solo funcionan en 2,4 GHz. Si tu router muestra 2,4 y 5 GHz con un mismo nombre, la configuración puede fallar; conecta el móvil a 2,4 GHz durante el emparejamiento.</li>
<li><strong>Posición del router:</strong> colócalo en el centro, lejos de metal y paredes gruesas. La distancia y las paredes importan más que la velocidad anunciada.</li>
<li><strong>Red de invitados:</strong> si tu router ofrece una, pon ahí los dispositivos inteligentes para separarlos de tus ordenadores y móviles.</li>
<li><strong>Contraseñas:</strong> cambia las que vienen por defecto, usa una contraseña Wi-Fi fuerte y mantén actualizado el firmware del router.</li>
<li><strong>Sin puertos abiertos:</strong> no expongas cámaras ni dispositivos a internet; usa la app del fabricante o un acceso remoto seguro.</li>
</ul>
<h2>Errores comunes</h2>
<ul>
<li>Emparejar un dispositivo con el móvil en una red solo de 5 GHz.</li>
<li>Dejar el router en un armario o en una esquina lejana y culpar al dispositivo.</li>
<li>Mantener la contraseña por defecto en una cámara o hub.</li>
</ul>
<h2>Para aprender más</h2>
<p>Para una base más sólida en redes y seguridad, mira nuestra <a href="{C}">sección de cursos</a>, que lista cursos de Coursera sobre estos temas. No los hemos revisado, así que consulta la página de cada curso.</p>
<h2>Preguntas frecuentes</h2>
<h3>¿Por qué mi dispositivo no se conecta durante la configuración?</h3>
<p>Lo más habitual es que el móvil esté en una red de 5 GHz o que la señal en el dispositivo sea débil. Acércate al router y vuelve a intentarlo.</p>
<h3>¿Necesito un sistema Wi-Fi Mesh?</h3>
<p>Solo si algunas habitaciones siguen con poca señal tras reubicar el router. En un piso pequeño suele bastar un router.</p>
<h3>¿Para qué sirve una red de invitados?</h3>
<p>Mantiene los dispositivos en los que confías menos, como cámaras baratas, en una red separada de tus ordenadores y móviles.</p>
"""
BODY[("network", "de")] = """<p>Die meisten Smart-Home-Probleme sind Netzwerkprobleme. Ein paar Gewohnheiten halten deine Geräte verbunden und dein Heimnetz sicherer.</p>
<h2>Worauf du achten solltest</h2>
<ul>
<li><strong>2,4 GHz:</strong> Viele günstige WLAN-Geräte funktionieren nur mit 2,4 GHz. Zeigt dein Router 2,4 und 5 GHz unter einem Namen, kann die Einrichtung scheitern; verbinde das Handy beim Koppeln mit 2,4 GHz.</li>
<li><strong>Router-Standort:</strong> Stelle ihn zentral auf, fern von Metall und dicken Wänden. Entfernung und Wände zählen mehr als die angegebene Geschwindigkeit.</li>
<li><strong>Gastnetz:</strong> Bietet dein Router eines an, lege die Smart-Home-Geräte dorthin, getrennt von Computern und Handys.</li>
<li><strong>Passwörter:</strong> Ändere die Standardpasswörter, nutze ein starkes WLAN-Passwort und halte die Router-Firmware aktuell.</li>
<li><strong>Keine offenen Ports:</strong> Setze Kameras und Geräte nicht ungeschützt ins Internet; nutze die App des Herstellers oder einen sicheren Fernzugriff.</li>
</ul>
<h2>Häufige Fehler</h2>
<ul>
<li>Ein Gerät koppeln, während das Handy in einem reinen 5-GHz-Netz ist.</li>
<li>Den Router im Schrank oder in einer fernen Ecke lassen und dann das Gerät beschuldigen.</li>
<li>Das Standardpasswort an einer Kamera oder einem Hub lassen.</li>
</ul>
<h2>Mehr lernen</h2>
<p>Für einen tieferen Einstieg in Netzwerke und Sicherheit schau in unseren <a href="{C}">Kursbereich</a>, der Coursera-Kurse zu diesen Themen auflistet. Wir haben sie nicht geprüft, sieh dir also die Seite jedes Kurses an.</p>
<h2>Häufige Fragen</h2>
<h3>Warum verbindet sich mein Gerät bei der Einrichtung nicht?</h3>
<p>Meist ist das Handy in einem 5-GHz-Netz oder das Signal am Gerät ist schwach. Geh näher an den Router und versuche es erneut.</p>
<h3>Brauche ich ein Mesh-WLAN-System?</h3>
<p>Nur wenn einzelne Räume nach dem Umstellen des Routers schwach versorgt bleiben. In einer kleinen Wohnung genügt meist ein Router.</p>
<h3>Wofür ist ein Gastnetz gut?</h3>
<p>Es hält Geräte, denen du weniger vertraust, etwa günstige Kameras, in einem eigenen Netz, getrennt von deinen Computern und Handys.</p>
"""
