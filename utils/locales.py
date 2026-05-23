LOCALES = {
    'en': {
        'choose_language':    "🌐 Choose your language | اختر لغتك:",
        'welcome': (
            "👋 *Welcome to SityStar AI Commander!*\n\n"
            "🚀 Deploy your website to the cloud in seconds\n"
            "🧠 AI-powered professional SEO analysis\n"
            "🔐 Your credentials are fully encrypted & private\n\n"
            "Use the menu below to get started:"
        ),
        'main_menu':          "🏠 *Main Menu* — What would you like to do?",
        'language_set':       "✅ Language set to *English*.",
        'btn_my_projects':    "📁 My Projects",
        'btn_deploy_new':     "🚀 Deploy New Site",
        'btn_settings':       "⚙️ Settings",
        'btn_help':           "❓ Help",
        'btn_back':           "◀️ Back",
        'btn_delete_project': "🗑️ Delete",
        'btn_copy_url':       "🔗 Open Site",
        'send_file': (
            "📤 *Send your website file or GitHub link:*\n\n"
            "📦 Supported formats:\n"
            "• `.zip` `.rar` `.7z` `.tar.gz`\n"
            "• Single `.html` file\n"
            "• GitHub repo link\n\n"
            "💡 _Your file will be uploaded exactly as-is._"
        ),
        'downloading':        "⬇️ Downloading file...",
        'extracting':         "📂 Extracting archive...",
        'deploying':          "☁️ Deploying to {provider}...",
        'seo_gen':            "🤖 Running AI SEO analysis...",
        'processing':         "⏳ Processing... Please wait.",
        'success': (
            "✅ *Deployment Successful!*\n\n"
            "🌐 *Live URL:* {url}\n"
            "📦 *Project:* `{name}`\n"
            "📈 *SEO Score:* {score}/100\n\n"
            "🎉 Your site is now live!"
        ),
        'error_format': (
            "❌ *Unsupported format.*\n\n"
            "Please send:\n"
            "• `.zip` `.rar` `.7z` `.tar.gz` `.html`\n"
            "• A valid GitHub repository link"
        ),
        'error_general':      "❌ *Error:* `{error}`",
        'error_no_token':     "❌ No hosting token configured. Go to ⚙️ Settings first.",
        'no_projects': (
            "📭 *No projects yet!*\n\n"
            "Click *🚀 Deploy New Site* to launch your first website."
        ),
        'project_list':       "📁 *Your Projects ({count})*",
        'project_item': (
            "━━━━━━━━━━━━━━━━━━\n"
            "📦 *{name}*\n"
            "🌐 {url}\n"
            "📈 SEO Score: {score}/100\n"
            "🕒 {date}"
        ),
        'project_deleted':    "🗑️ Project `{name}` deleted.",
        'settings': (
            "⚙️ *Settings*\n\n"
            "Configure your personal engine:\n"
            "• *AI* — Model used for SEO analysis\n"
            "• *Database* — Your own cloud storage\n"
            "• *Hosting* — Netlify or Vercel token\n"
            "• *SEO Toggle* — Enable/disable analysis"
        ),
        'btn_ai':             "🧠 AI Provider",
        'btn_db':             "📁 Database",
        'btn_hosting':        "🚀 Hosting",
        'btn_lang':           "🌐 Language",
        'btn_ping':           "⚡ Connection Status",
        'btn_delete_data':    "🗑️ Delete My Data",
        'btn_seo_on':         "🟢 Auto SEO: ON",
        'btn_seo_off':        "🔴 Auto SEO: OFF",
        'ask_ai_key': (
            "🧠 *AI Configuration*\n\n"
            "Send your API key. I'll auto-detect the provider:\n"
            "• `sk-or-...` → OpenRouter\n"
            "• `sk-...` → OpenAI\n"
            "• `AIza...` → Gemini"
        ),
        'checking_ai':        "⏳ Validating API key...",
        'ai_detected':        "✅ *Detected:* {provider}\n\nChoose a model:",
        'ai_saved':           "✅ AI settings saved! ({provider} / {model})",
        'ai_key_invalid':     "❌ Invalid API key. Please try again.",
        'choose_db':          "📁 *Choose Database Provider:*",
        'btn_supabase':       "🟩 Supabase",
        'btn_mongodb':        "🍃 MongoDB",
        'btn_firebase':       "🔥 Firebase",
        'btn_skip_db':        "⏭️ Skip (use default)",
        'ask_db_creds': (
            "📁 *{provider} Credentials*\n\n"
            "Send your connection details:\n"
            "• *Supabase* → `{\"url\":\"...\", \"key\":\"...\"}`\n"
            "• *MongoDB* → Connection URI string\n"
            "• *Firebase* → Paste service account JSON"
        ),
        'testing_db':         "⏳ Testing connection...",
        'db_ping_success':    "✅ *{provider}* connected & saved!",
        'db_ping_failed':     "❌ Connection failed. Check your credentials.",
        'error_parsing_creds':"❌ Could not parse credentials: `{error}`",
        'choose_hosting':     "🚀 *Choose Hosting Provider:*",
        'btn_netlify':        "◼️ Netlify",
        'btn_vercel':         "▲ Vercel",
        'btn_skip_hosting':   "⏭️ Use default",
        'ask_hosting_token': (
            "🚀 *{provider} Token*\n\n"
            "Send your Personal Access Token.\n"
            "Get it from: *{provider} Dashboard → User Settings → Tokens*"
        ),
        'hosting_saved':      "✅ Hosting saved! (*{provider}*)",
        'ping_status': (
            "⚡ *Connection Status*\n\n"
            "🧠 AI: {ai}\n"
            "📁 Database: {db}\n"
            "🚀 Hosting: {hosting}\n\n"
            "_Configured = using your key | Default = using bot's fallback_"
        ),
        'configured':         "✅ Configured",
        'using_default':      "🔄 Using Default",
        'confirm_delete_data':"⚠️ This will permanently delete all your stored keys. Are you sure?",
        'btn_confirm_yes':    "✅ Yes, delete everything",
        'btn_confirm_no':     "❌ Cancel",
        'data_deleted':       "🗑️ All your data has been permanently deleted.",
        'help': (
            "❓ *Help & Commands*\n\n"
            "/start — Main menu\n"
            "/settings — Configure AI, DB, Hosting\n"
            "/projects — View your projects\n"
            "/deploy — Deploy a new site\n"
            "/status — Check connection status\n"
            "/help — Show this message\n\n"
            "📤 *To deploy:* send a `.zip`, `.rar`, `.7z`, `.tar.gz`, `.html` file or a GitHub link.\n\n"
            "🔐 *Security:* Your keys are encrypted with AES-256 before storage."
        ),
        'seo_report_header':  "📊 *AI SEO Report — {name}*",
        'seo_score_label':    "🏆 Score",
        'seo_title_label':    "📌 Suggested Title",
        'seo_desc_label':     "📝 Suggested Description",
        'seo_kw_label':       "🔑 Top Keywords",
        'seo_og_label':       "📣 Social Media Title",
        'seo_tips':           "💡 *Tips to improve your score:*",
    },

    'ar': {
        'choose_language':    "🌐 اختر لغتك | Choose your language:",
        'welcome': (
            "👋 *أهلاً وسهلاً بك في SityStar AI Commander!*\n\n"
            "🚀 انشر موقعك على الإنترنت في ثوانٍ معدودة\n"
            "🧠 تحليل احترافي لتحسين محركات البحث بالذكاء الاصطناعي\n"
            "🔐 بياناتك مشفرة ومحمية بالكامل\n\n"
            "استخدم القائمة أدناه للبدء:"
        ),
        'main_menu':          "🏠 *القائمة الرئيسية* — ماذا تريد أن تفعل؟",
        'language_set':       "✅ تم تعيين اللغة إلى *العربية*.",
        'btn_my_projects':    "📁 مشاريعي",
        'btn_deploy_new':     "🚀 نشر موقع جديد",
        'btn_settings':       "⚙️ الإعدادات",
        'btn_help':           "❓ المساعدة",
        'btn_back':           "◀️ رجوع",
        'btn_delete_project': "🗑️ حذف",
        'btn_copy_url':       "🔗 فتح الموقع",
        'send_file': (
            "📤 *أرسل ملف موقعك أو رابط المستودع:*\n\n"
            "📦 الصيغ المدعومة:\n"
            "• `.zip` `.rar` `.7z` `.tar.gz`\n"
            "• ملف `.html` مفرد\n"
            "• رابط مستودع GitHub\n\n"
            "💡 _سيتم رفع ملفك كما هو تماماً دون أي تعديل._"
        ),
        'downloading':        "⬇️ جاري تحميل الملف...",
        'extracting':         "📂 جاري فك ضغط الأرشيف...",
        'deploying':          "☁️ جاري النشر على {provider}...",
        'seo_gen':            "🤖 جاري تحليل الموقع لتحسين محركات البحث...",
        'processing':         "⏳ جاري المعالجة... يرجى الانتظار.",
        'success': (
            "✅ *تم النشر بنجاح!*\n\n"
            "🌐 *رابط الموقع:* {url}\n"
            "📦 *اسم المشروع:* `{name}`\n"
            "📈 *درجة الظهور في محركات البحث:* {score}/100\n\n"
            "🎉 موقعك الآن متاح للجميع على الإنترنت!"
        ),
        'error_format': (
            "❌ *صيغة الملف غير مدعومة.*\n\n"
            "يرجى إرسال أحد التالي:\n"
            "• ملف مضغوط: `.zip` `.rar` `.7z` `.tar.gz`\n"
            "• ملف `.html` مفرد\n"
            "• رابط مستودع GitHub صالح"
        ),
        'error_general':      "❌ *حدث خطأ:* `{error}`",
        'error_no_token':     "❌ لم يتم إعداد رمز منصة الاستضافة بعد. اذهب إلى ⚙️ الإعدادات أولاً.",
        'no_projects': (
            "📭 *لا توجد مشاريع بعد!*\n\n"
            "اضغط على *🚀 نشر موقع جديد* لإطلاق موقعك الأول."
        ),
        'project_list':       "📁 *مشاريعك ({count})*",
        'project_item': (
            "━━━━━━━━━━━━━━━━━━\n"
            "📦 *{name}*\n"
            "🌐 {url}\n"
            "📈 درجة الظهور: {score}/100\n"
            "🕒 {date}"
        ),
        'project_deleted':    "🗑️ تم حذف المشروع `{name}` بنجاح.",
        'settings': (
            "⚙️ *الإعدادات*\n\n"
            "قم بتكوين محرك البوت الخاص بك:\n"
            "• *الذكاء الاصطناعي* — النموذج المستخدم لتحليل موقعك\n"
            "• *قاعدة البيانات* — التخزين السحابي الخاص بك\n"
            "• *منصة الاستضافة* — رمز الوصول لـ Netlify أو Vercel\n"
            "• *تحسين محركات البحث* — تفعيل أو إيقاف التحليل التلقائي"
        ),
        'btn_ai':             "🧠 الذكاء الاصطناعي",
        'btn_db':             "📁 قاعدة البيانات",
        'btn_hosting':        "🚀 منصة الاستضافة",
        'btn_lang':           "🌐 اللغة",
        'btn_ping':           "⚡ حالة الاتصال",
        'btn_delete_data':    "🗑️ حذف بياناتي",
        'btn_seo_on':         "🟢 التحليل التلقائي: مفعّل",
        'btn_seo_off':        "🔴 التحليل التلقائي: معطّل",
        'ask_ai_key': (
            "🧠 *إعداد الذكاء الاصطناعي*\n\n"
            "أرسل مفتاح الوصول الخاص بك. سأكتشف المزود تلقائياً:\n"
            "• يبدأ بـ `sk-or-...` ← OpenRouter\n"
            "• يبدأ بـ `sk-...` ← OpenAI\n"
            "• يبدأ بـ `AIza...` ← Gemini"
        ),
        'checking_ai':        "⏳ جاري التحقق من صلاحية المفتاح...",
        'ai_detected':        "✅ *المزود المُكتشف:* {provider}\n\nاختر النموذج المناسب:",
        'ai_saved':           "✅ تم حفظ إعدادات الذكاء الاصطناعي بنجاح! ({provider} / {model})",
        'ai_key_invalid':     "❌ مفتاح الوصول غير صالح. يرجى المحاولة مرة أخرى.",
        'choose_db':          "📁 *اختر مزود قاعدة البيانات:*",
        'btn_supabase':       "🟩 Supabase",
        'btn_mongodb':        "🍃 MongoDB",
        'btn_firebase':       "🔥 Firebase",
        'btn_skip_db':        "⏭️ تخطي (استخدام الافتراضي)",
        'ask_db_creds': (
            "📁 *بيانات اتصال {provider}*\n\n"
            "أرسل بيانات الاتصال بالصيغة المناسبة:\n"
            "• *Supabase* ← `{\"url\":\"...\", \"key\":\"...\"}`\n"
            "• *MongoDB* ← رابط الاتصال بقاعدة البيانات\n"
            "• *Firebase* ← الصق محتوى ملف حساب الخدمة"
        ),
        'testing_db':         "⏳ جاري اختبار الاتصال بقاعدة البيانات...",
        'db_ping_success':    "✅ تم الاتصال بـ *{provider}* وحفظ البيانات بنجاح!",
        'db_ping_failed':     "❌ فشل الاتصال. تأكد من صحة بيانات الاتصال وحاول مجدداً.",
        'error_parsing_creds':"❌ فشل في قراءة البيانات: `{error}`",
        'choose_hosting':     "🚀 *اختر منصة الاستضافة:*",
        'btn_netlify':        "◼️ Netlify",
        'btn_vercel':         "▲ Vercel",
        'btn_skip_hosting':   "⏭️ استخدام المنصة الافتراضية",
        'ask_hosting_token': (
            "🚀 *رمز الوصول لـ {provider}*\n\n"
            "أرسل رمز الوصول الشخصي الخاص بك.\n"
            "يمكنك الحصول عليه من:\n"
            "{provider} ← لوحة التحكم ← إعدادات المستخدم ← رموز الوصول الشخصية"
        ),
        'hosting_saved':      "✅ تم حفظ منصة الاستضافة بنجاح! (*{provider}*)",
        'ping_status': (
            "⚡ *حالة الاتصال*\n\n"
            "🧠 الذكاء الاصطناعي: {ai}\n"
            "📁 قاعدة البيانات: {db}\n"
            "🚀 منصة الاستضافة: {hosting}\n\n"
            "_مُكوَّن = يستخدم مفتاحك الخاص | افتراضي = يستخدم إعدادات البوت_"
        ),
        'configured':         "✅ مُكوَّن",
        'using_default':      "🔄 يستخدم الافتراضي",
        'confirm_delete_data':(
            "⚠️ *تحذير! هذا الإجراء لا يمكن التراجع عنه.*\n\n"
            "سيتم حذف جميع مفاتيح الوصول وبيانات الإعداد الخاصة بك بشكل نهائي.\n"
            "هل أنت متأكد من المتابعة؟"
        ),
        'btn_confirm_yes':    "✅ نعم، احذف كل شيء",
        'btn_confirm_no':     "❌ إلغاء",
        'data_deleted':       "🗑️ تم حذف جميع بياناتك وإعداداتك الشخصية نهائياً.",
        'help': (
            "❓ *المساعدة والأوامر المتاحة*\n\n"
            "/start — القائمة الرئيسية\n"
            "/settings — إعداد الذكاء الاصطناعي وقاعدة البيانات ومنصة الاستضافة\n"
            "/projects — عرض مشاريعك المنشورة\n"
            "/deploy — نشر موقع جديد\n"
            "/status — فحص حالة الاتصال بالخدمات\n"
            "/help — عرض قائمة المساعدة هذه\n\n"
            "📤 *طريقة النشر:* أرسل ملفاً مضغوطاً (`.zip` أو `.rar` أو `.7z`) "
            "أو ملف `.html` أو رابط مستودع GitHub.\n\n"
            "🔐 *الأمان:* جميع مفاتيحك مشفرة قبل أي عملية حفظ."
        ),
        'seo_report_header':  "📊 *تقرير تحسين محركات البحث بالذكاء الاصطناعي — {name}*",
        'seo_score_label':    "🏆 الدرجة الإجمالية",
        'seo_title_label':    "📌 العنوان الرئيسي المقترح",
        'seo_desc_label':     "📝 الوصف المقترح",
        'seo_kw_label':       "🔑 أهم الكلمات المفتاحية",
        'seo_og_label':       "📣 عنوان منصات التواصل الاجتماعي",
        'seo_tips':           "💡 *نصائح لتحسين درجة موقعك:*",
    }
}
