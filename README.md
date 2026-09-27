# بيتي الذكي — موقع أفيليت أوتوماتيكي (مجاني بالكامل)

موقع ستاتيكي يعرض منتجات تسويق بالعمولة، مع تحديث تلقائي يومي عبر GitHub Actions
ونشر مجاني عبر GitHub Pages. لا حاجة لأي استضافة مدفوعة أو سيرفر.

## الخطوة 1 — إنشاء حساب GitHub (إن لم يكن لديك)
اذهب إلى https://github.com/signup وأنشئ حسابًا مجانيًا.

## الخطوة 2 — رفع المشروع
1. أنشئ مستودع (Repository) جديد باسم مناسب، مثلًا `smart-home-affiliate`.
   اجعله **Public** (لازم يكون عام حتى تعمل GitHub Actions مجانًا بلا حدود).
2. ارفع جميع ملفات هذا المجلد إليه. أسهل طريقة من جهازك:
   ```bash
   cd affiliate-site
   git init
   git add .
   git commit -m "أول نسخة من الموقع"
   git branch -M main
   git remote add origin https://github.com/USERNAME/smart-home-affiliate.git
   git push -u origin main
   ```

## الخطوة 3 — تفعيل GitHub Pages
1. من المستودع: **Settings → Pages**
2. تحت "Build and deployment" اختر **Source: GitHub Actions**
3. بعد أول تشغيل لـ Workflow (خطوة تالية)، سيظهر رابط موقعك مثل:
   `https://USERNAME.github.io/smart-home-affiliate/`

## الخطوة 4 — تشغيل الأتمتة لأول مرة
من تبويب **Actions** في المستودع، افتح workflow باسم
"تحديث المنتجات ونشر الموقع" واضغط **Run workflow** يدويًا أول مرة.
بعدها سيعمل تلقائيًا كل يوم حسب الجدولة في الملف
`.github/workflows/update-and-deploy.yml`.

## الخطوة 5 — إضافة منتجاتك الحقيقية
عدّل ملف `scripts/sources.csv` وأضف صفوفًا جديدة (كل صف = منتج).
الأعمدة:
```
id, title, category, price, currency, rating, reviews_count, image, description, affiliate_url, network, tags
```
احفظ الملف وارفعه (`git add . && git commit -m "منتجات جديدة" && git push`) —
سيتحدث الموقع تلقائيًا خلال دقائق.

## الخطوة 6 — الانضمام لبرامج العمولة (مجانية)
- **AliExpress Affiliate**: https://portals.aliexpress.com — تسجيل مجاني فوري،
  تحصل على رابط أفيليت لأي منتج على الموقع.
- **Amazon Associates**: https://affiliate-program.amazon.com — تسجيل مجاني،
  يتطلب أول عملية بيع خلال 180 يومًا وإلا يُغلق الحساب (انتبه لهذا الشرط).
- **Awin**: https://www.awin.com — شبكة تجمع مئات المتاجر ببرنامج تسجيل واحد.

انسخ رابط الأفيليت الخاص بكل منتج وضعه في عمود `affiliate_url`.

## الخطوة 7 (اختياري) — تفعيل الجلب التلقائي عبر API بدل CSV
الوضع الحالي يعتمد على CSV تحرره يدويًا (بسيط وموثوق ومجاني 100%).
إذا أردت جلبًا كاملًا بدون تدخل يدوي:
1. سجّل واحصل على مفاتيح API من AliExpress Affiliate أو Amazon PA API.
2. أضف المفاتيح كـ **Repository Secrets** من Settings → Secrets → Actions.
3. عدّل `scripts/fetch_products.py` وفعّل الدالة المُعلَّقة (TODO) في أعلى الملف.

ملاحظة: بعض الشروط في برامج العمولة تمنع السحب الآلي المباشر (Scraping) لصفحات
المنتج نفسها؛ استخدم الـ API الرسمي فقط لتفادي أي مخالفة لشروط الاستخدام.

## الخطوة 8 — تخصيص الهوية والنيتش
- غيّر اسم الموقع في `index.html` (`<title>` و`.brand-name`).
- غيّر الألوان من متغيرات CSS في أعلى ملف `style.css` (`:root`).
- الفئات الحالية تجريبية (منزل ذكي) — غيّرها في `products.json` وفي دالة
  `build_categories()` داخل `scripts/fetch_products.py`.

## قانوني مهم
- نص الإفصاح عن العمولة موجود بالفعل في تذييل الصفحة — لا تحذفه، وهو مطلوب
  قانونيًا في معظم الدول وفي شروط برامج العمولة نفسها.
- تأكد من قراءة الشروط والأحكام لكل برنامج عمولة تنضم إليه قبل الأتمتة الكاملة.

## هيكل الملفات
```
affiliate-site/
├── index.html              # الصفحة الرئيسية
├── style.css                # التصميم
├── script.js                 # عرض المنتجات + البحث + الفلترة
├── products.json             # بيانات المنتجات (تُحدَّث تلقائيًا)
├── scripts/
│   ├── fetch_products.py     # سكربت التحديث
│   └── sources.csv           # مصدر المنتجات اليدوي
└── .github/workflows/
    └── update-and-deploy.yml # الأتمتة (تحديث يومي + نشر)
```
