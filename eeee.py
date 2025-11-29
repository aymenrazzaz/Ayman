import logging
import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# إعدادات البوت
TOKEN = "8525935096:AAH08pcMTWZ3TWH2UDAGZJDdlwEBRPaFECk"
DEVELOPER_ID = 7976303331

# إنشاء مجلد البيانات
if not os.path.exists('data'):
    os.makedirs('data')

# تحميل البيانات
def load_data(filename, default={}):
    try:
        with open(f'data/{filename}', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return default

def save_data(filename, data):
    with open(f'data/{filename}', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# تحميل البيانات
carlos = load_data('carlos.json', {
    "bot": "✅", "d6": "✅", "d7": "✅", 
    "ban": [], "admin": [], "start": "أهلاً بك في بوت التواصل! 🚀",
    "ch1": "", "ch2": "", "ch1p": "", "ch2p": "", "sudo": ""
})

meca = load_data('members.json', {"members": [], "group": [], "banbots": []})

# إعداد اللوجر
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def show_admin_panel(update: Update, context: CallbackContext, message_id=None):
    """عرض لوحة التحكم للمطور"""
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    keyboard = [
        [
            InlineKeyboardButton(f"البوت {carlos['bot']}", callback_data="bot3"),
            InlineKeyboardButton(f"التوجيه {carlos['d7']}", callback_data="d7"),
            InlineKeyboardButton(f"الإشعارات {carlos['d6']}", callback_data="d6")
        ],
        [InlineKeyboardButton("رسالة الترحيب", callback_data="4")],
        [
            InlineKeyboardButton("قسم النسخة", callback_data="Open"),
            InlineKeyboardButton("نقل الملكية", callback_data="AddAdmin")
        ],
        [
            InlineKeyboardButton("الإذاعة", callback_data="10"),
            InlineKeyboardButton("الإحصائيات", callback_data="1"),
            InlineKeyboardButton("الاشتراك", callback_data="All_Ch")
        ],
        [
            InlineKeyboardButton("قسم المحظورين", callback_data="lastban"),
            InlineKeyboardButton("قسم الأدمنية", callback_data="5")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "• أهلاً بك في لوحة الأدمن الخاصة بالبوت\n- يمكنك التحكم في البوت الخاص بك من هنا\n⎯ ⎯ ⎯ ⎯"
    
    if message_id:
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=reply_markup
        )
    else:
        update.message.reply_text(text, reply_markup=reply_markup)

# دالة البدء
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    chat_id = update.effective_chat.id
    from_id = user.id
    
    if chat_id not in meca["members"]:
        meca["members"].append(chat_id)
        save_data('members.json', meca)
    
    if str(from_id) == str(DEVELOPER_ID) or str(from_id) in carlos.get("admin", []) or str(from_id) == carlos.get("sudo", ""):
        show_admin_panel(update, context)
    else:
        start_message = carlos.get("start", "أهلاً بك في بوت التواصل! 🚀")
        keyboard = [[
            InlineKeyboardButton("𝗦𝘂𝗿𝘀 𝗫!𝗠𝗮𝘅", url="https://t.me/YU_4Io")
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.message.reply_text(
            start_message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
        if carlos["d6"] == "✅":
            context.bot.send_message(
                DEVELOPER_ID,
                f"👤 مستخدم جديد:\nالاسم: {user.first_name}\nالمعرف: @{user.username}\nالأيدي: {user.id}\n⎯ ⎯ ⎯ ⎯\nعدد المستخدمين: {len(meca['members'])}"
            )

# معالجة الكول باك
def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    
    if str(user_id) != str(DEVELOPER_ID) and str(user_id) not in carlos.get("admin", []) and str(user_id) != carlos.get("sudo", ""):
        query.answer("ليس لديك صلاحية للوصول إلى هذه اللوحة!", show_alert=True)
        return
    
    query.answer()
    
    if data == "back":
        show_admin_panel(update, context, message_id)
    
    elif data == "bot3":
        carlos["bot"] = "❎" if carlos["bot"] == "✅" else "✅"
        save_data('carlos.json', carlos)
        show_admin_panel(update, context, message_id)
    
    elif data == "d6":
        carlos["d6"] = "❎" if carlos["d6"] == "✅" else "✅"
        save_data('carlos.json', carlos)
        show_admin_panel(update, context, message_id)
    
    elif data == "d7":
        carlos["d7"] = "❎" if carlos["d7"] == "✅" else "✅"
        save_data('carlos.json', carlos)
        show_admin_panel(update, context, message_id)
    
    elif data == "1":
        md3 = len(meca["members"])
        md5 = len(meca["group"])
        countall = md3 + md5
        md4 = len(meca.get("banbots", []))
        
        stats_text = f"- عدد المستخدمين الكلي: {countall}\n- عدد الخاص: {md3}\n- عدد الكروبات: {md5}\n- عدد المحظورين: {md4}\n⎯ ⎯ ⎯ ⎯"
        
        keyboard = [
            [InlineKeyboardButton("تصفير الإحصائيات 🗑", callback_data="lstadel")],
            [InlineKeyboardButton("الغاء ↪️", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=stats_text,
            reply_markup=reply_markup
        )
    
    elif data == "4":
        keyboard = [
            [InlineKeyboardButton("عرض رسالة start", callback_data="startsho")],
            [InlineKeyboardButton("مسح رسالة start", callback_data="unset_start")],
            [InlineKeyboardButton("تغيير رسالة start", callback_data="setstart")],
            [InlineKeyboardButton("رجوع", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="أهلاً بك في قسم رسالة start",
            reply_markup=reply_markup
        )
    
    elif data == "setstart":
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="يمكنك الآن إرسال رسالة الـstart ⏳\nلعرض الاسم: #name\nلعرض الأيدي: #id\nلعرض المعرف: #user\n⎯ ⎯ ⎯ ⎯"
        )
        context.user_data['waiting_for_start'] = True
    
    elif data == "startsho":
        start_msg = carlos.get("start", "أهلاً بك في بوت التواصل! 🚀")
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"رسالة الـstart الحالية:\n⎯ ⎯ ⎯ ⎯\n{start_msg}"
        )
    
    elif data == "unset_start":
        carlos["start"] = "أهلاً بك في بوت التواصل! 🚀"
        save_data('carlos.json', carlos)
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="✅ تم حذف رسالة start المخصصة"
        )
    
    elif data == "10":
        md3 = len(meca["members"])
        md5 = len(meca["group"])
        countall = md3 + md5
        
        stats_text = f"- عدد المستخدمين الكلي: {countall}\n- عدد الخاص: {md3}\n- عدد الكروبات: {md5}\n⎯ ⎯ ⎯ ⎯"
        
        keyboard = [
            [
                InlineKeyboardButton("اذاعة للكل", callback_data="send_text"),
                InlineKeyboardButton("اذاعة توجيه للكل", callback_data="send_rep")
            ],
            [
                InlineKeyboardButton("اذاعة للخاص", callback_data="send_text1"),
                InlineKeyboardButton("اذاعة توجيه للخاص", callback_data="send_rep1")
            ],
            [
                InlineKeyboardButton("اذاعة كروبات", callback_data="send_text2"),
                InlineKeyboardButton("اذاعة توجيه كروبات", callback_data="send_rep2")
            ],
            [InlineKeyboardButton("رجوع", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=stats_text,
            reply_markup=reply_markup
        )
    
    elif data == "send_text":
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="أرسل رسالتك وسيتم إرسالها لجميع المستخدمين والكروبات"
        )
        context.user_data['broadcast_type'] = 'all_text'
    
    elif data == "send_rep":
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="أعد توجيه الرسالة التي تريد إرسالها للجميع"
        )
        context.user_data['broadcast_type'] = 'all_forward'
    
    elif data == "send_text1":
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="أرسل رسالتك وسيتم إرسالها للمستخدمين في الخاص"
        )
        context.user_data['broadcast_type'] = 'private_text'
    
    elif data == "send_rep1":
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="أعد توجيه الرسالة التي تريد إرسالها للمستخدمين في الخاص"
        )
        context.user_data['broadcast_type'] = 'private_forward'
    
    elif data == "send_text2":
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="أرسل رسالتك وسيتم إرسالها للكروبات فقط"
        )
        context.user_data['broadcast_type'] = 'groups_text'
    
    elif data == "send_rep2":
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="أعد توجيه الرسالة التي تريد إرسالها للكروبات فقط"
        )
        context.user_data['broadcast_type'] = 'groups_forward'
    
    elif data == "5":
        admin_text = "يمكنك رفع أدمن وحذف أدمن عن طريق الأزرار 🔽\n⎯ ⎯ ⎯ ⎯\nيمكن للأدمن التحقق من الإحصائيات فقط ⚠️"
        
        keyboard = []
        for admin_id in carlos.get("admin", []):
            keyboard.append([InlineKeyboardButton(f"حذف {admin_id}", callback_data=f"del_{admin_id}")])
        
        keyboard.append([InlineKeyboardButton("اضف أدمن ➕", callback_data="add_admin")])
        keyboard.append([InlineKeyboardButton("رجوع", callback_data="back")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=admin_text,
            reply_markup=reply_markup
        )
    
    elif data == "add_admin":
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="أرسل الآن أيدي الأدمن الجديد"
        )
        context.user_data['waiting_for_admin'] = True
    
    elif data.startswith("del_"):
        admin_id = data.replace("del_", "")
        if admin_id in carlos.get("admin", []):
            carlos["admin"].remove(admin_id)
            save_data('carlos.json', carlos)
            context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"✅ تم حذف الأدمن {admin_id}"
            )
    
    elif data == "lastban":
        addbanlst = len(carlos.get("ban", []))
        ban_text = f"اليك قسم المحظورين.\nعدد المحظورين: {addbanlst}\n⎯ ⎯ ⎯ ⎯"
        
        keyboard = [
            [InlineKeyboardButton("حظر عضو", callback_data="bannambar")],
            [InlineKeyboardButton("الغاء حظر", callback_data="unbannambar")],
            [InlineKeyboardButton("عرض المحظورين", callback_data="lstesban")],
            [InlineKeyboardButton("مسح المحظورين", callback_data="dellastban")],
            [InlineKeyboardButton("رجوع", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=ban_text,
            reply_markup=reply_markup
        )
    
    elif data == "bannambar":
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="أرسل أيدي العضو الذي تريد حظره"
        )
        context.user_data['waiting_for_ban'] = True
    
    elif data == "unbannambar":
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="أرسل أيدي العضو الذي تريد إلغاء حظره"
        )
        context.user_data['waiting_for_unban'] = True
    
    elif data == "lstesban":
        ban_list = carlos.get("ban", [])
        if ban_list:
            ban_text = "قائمة المحظورين:\n⎯ ⎯ ⎯ ⎯\n"
            for user_id in ban_list:
                ban_text += f"- {user_id}\n"
        else:
            ban_text = "لا يوجد محظورين حالياً"
        
        keyboard = [[InlineKeyboardButton("رجوع", callback_data="lastban")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=ban_text,
            reply_markup=reply_markup
        )
    
    elif data == "dellastban":
        carlos["ban"] = []
        save_data('carlos.json', carlos)
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="✅ تم مسح جميع المحظورين"
        )
    
    elif data == "Open":
        keyboard = [
            [InlineKeyboardButton("جلب نسخة الأعضاء", callback_data="OpenCopy")],
            [InlineKeyboardButton("جلب نسخة الإعدادات", callback_data="Openstengs")],
            [InlineKeyboardButton("رفع نسخة", callback_data="addfiles")],
            [InlineKeyboardButton("رجوع", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="اليك قسم النسخة للبوت 🗂\n⎯ ⎯ ⎯ ⎯",
            reply_markup=reply_markup
        )
    
    elif data == "OpenCopy":
        # إرسال نسخة الأعضاء
        with open('data/members.json', 'rb') as f:
            context.bot.send_document(
                chat_id=chat_id,
                document=f,
                filename="members.json",
                caption="نسخة الأعضاء 🗂"
            )
    
    elif data == "Openstengs":
        # إرسال نسخة الإعدادات
        with open('data/carlos.json', 'rb') as f:
            context.bot.send_document(
                chat_id=chat_id,
                document=f,
                filename="carlos.json",
                caption="نسخة الإعدادات 🗂"
            )
    
    elif data == "AddAdmin":
        if str(user_id) == str(DEVELOPER_ID):
            context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="أرسل أيدي المطور الجديد"
            )
            context.user_data['waiting_for_sudo'] = True
        else:
            query.answer("❌ فقط المطور الأساسي يمكنه نقل الملكية!", show_alert=True)
    
    elif data == "All_Ch":
        keyboard = [
            [InlineKeyboardButton("اضف قناة أولى", callback_data="AddCh1")],
            [InlineKeyboardButton("اضف قناة ثانية", callback_data="AddCh2")],
            [InlineKeyboardButton("عرض القنوات", callback_data="ALLCH")],
            [InlineKeyboardButton("رجوع", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="🖇 أهلاً بك في قسم الاشتراك الإجباري",
            reply_markup=reply_markup
        )
    
    elif data == "AddCh1":
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="أرسل معرف القناة الأولى مع @"
        )
        context.user_data['waiting_for_ch1'] = True
    
    elif data == "AddCh2":
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="أرسل معرف القناة الثانية مع @"
        )
        context.user_data['waiting_for_ch2'] = True
    
    elif data == "ALLCH":
        ch1 = carlos.get("ch1", "غير مضبوطة")
        ch2 = carlos.get("ch2", "غير مضبوطة")
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"قنوات الاشتراك الإجباري:\nالقناة الأولى: {ch1}\nالقناة الثانية: {ch2}"
        )
    
    else:
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"زر: {data}\nهذه الخاصية قيد التطوير ⚠️"
        )

# معالجة الرسائل العادية
def handle_message(update: Update, context: CallbackContext) -> None:
    if update.message:
        message = update.message
        chat_id = message.chat_id
        text = message.text
        from_id = message.from_user.id
        
        if carlos["bot"] == "❎" and str(from_id) != str(DEVELOPER_ID):
            message.reply_text("⚙- عذراً عزيزي حاليًا البوت معطل لتحديثات جديدة")
            return
        
        if str(from_id) in carlos.get("ban", []):
            message.reply_text("⚠️- عذراً عزيزي لقد قام المطور بحظرك من هذا البوت")
            return
        
        # معالجة تحديث رسالة start
        if 'waiting_for_start' in context.user_data and context.user_data['waiting_for_start']:
            new_start = message.text
            carlos["start"] = new_start
            save_data('carlos.json', carlos)
            context.user_data['waiting_for_start'] = False
            message.reply_text("✅ تم تحديث رسالة start بنجاح")
            return
        
        # معالجة إضافة أدمن
        if 'waiting_for_admin' in context.user_data and context.user_data['waiting_for_admin']:
            new_admin = message.text
            if new_admin not in carlos.get("admin", []):
                carlos["admin"].append(new_admin)
                save_data('carlos.json', carlos)
                message.reply_text(f"✅ تم إضافة الأدمن {new_admin}")
            else:
                message.reply_text("❌ هذا الأدمن موجود مسبقاً")
            context.user_data['waiting_for_admin'] = False
            return
        
        # معالجة نقل الملكية
        if 'waiting_for_sudo' in context.user_data and context.user_data['waiting_for_sudo']:
            new_sudo = message.text
            carlos["sudo"] = new_sudo
            save_data('carlos.json', carlos)
            context.user_data['waiting_for_sudo'] = False
            message.reply_text(f"✅ تم نقل الملكية للمطور {new_sudo}")
            return
        
        # معالجة الحظر
        if 'waiting_for_ban' in context.user_data and context.user_data['waiting_for_ban']:
            user_to_ban = message.text
            if user_to_ban not in carlos.get("ban", []):
                carlos["ban"].append(user_to_ban)
                save_data('carlos.json', carlos)
                message.reply_text(f"✅ تم حظر العضو {user_to_ban}")
            else:
                message.reply_text("❌ هذا العضو محظور مسبقاً")
            context.user_data['waiting_for_ban'] = False
            return
        
        # معالجة إلغاء الحظر
        if 'waiting_for_unban' in context.user_data and context.user_data['waiting_for_unban']:
            user_to_unban = message.text
            if user_to_unban in carlos.get("ban", []):
                carlos["ban"].remove(user_to_unban)
                save_data('carlos.json', carlos)
                message.reply_text(f"✅ تم إلغاء حظر العضو {user_to_unban}")
            else:
                message.reply_text("❌ هذا العضو غير محظور")
            context.user_data['waiting_for_unban'] = False
            return
        
        # معالجة إضافة القنوات
        if 'waiting_for_ch1' in context.user_data and context.user_data['waiting_for_ch1']:
            carlos["ch1"] = message.text
            save_data('carlos.json', carlos)
            context.user_data['waiting_for_ch1'] = False
            message.reply_text(f"✅ تم إضافة القناة الأولى: {message.text}")
            return
        
        if 'waiting_for_ch2' in context.user_data and context.user_data['waiting_for_ch2']:
            carlos["ch2"] = message.text
            save_data('carlos.json', carlos)
            context.user_data['waiting_for_ch2'] = False
            message.reply_text(f"✅ تم إضافة القناة الثانية: {message.text}")
            return
        
        # معالجة البث
        if 'broadcast_type' in context.user_data:
            broadcast_type = context.user_data['broadcast_type']
            success_count = 0
            
            if 'text' in broadcast_type:
                # بث نصي
                if 'all' in broadcast_type:
                    targets = meca["members"] + meca["group"]
                elif 'private' in broadcast_type:
                    targets = meca["members"]
                else:  # groups
                    targets = meca["group"]
                
                for target in targets:
                    try:
                        context.bot.send_message(target, text)
                        success_count += 1
                    except:
                        continue
            
            elif 'forward' in broadcast_type:
                # بث بتوجيه
                if 'all' in broadcast_type:
                    targets = meca["members"] + meca["group"]
                elif 'private' in broadcast_type:
                    targets = meca["members"]
                else:  # groups
                    targets = meca["group"]
                
                for target in targets:
                    try:
                        context.bot.forward_message(
                            chat_id=target,
                            from_chat_id=chat_id,
                            message_id=message.message_id
                        )
                        success_count += 1
                    except:
                        continue
            
            message.reply_text(f"✅ تم إرسال الرسالة لـ {success_count} مستخدم")
            del context.user_data['broadcast_type']
            return
        
        # إعادة توجيه الرسائل للمطور
        if (text and text != "/start" and str(from_id) != str(DEVELOPER_ID) and 
            carlos["d7"] == "✅" and str(from_id) not in carlos.get("ban", [])):
            context.bot.forward_message(
                chat_id=DEVELOPER_ID,
                from_chat_id=chat_id,
                message_id=message.message_id
            )
            message.reply_text("✅ تم إرسال رسالتك للمطور")

# معالجة الردود من المطور
def handle_reply(update: Update, context: CallbackContext) -> None:
    message = update.message
    if message.reply_to_message and message.reply_to_message.forward_from:
        target_user = message.reply_to_message.forward_from.id
        
        if message.text:
            context.bot.send_message(target_user, message.text)
        elif message.voice:
            context.bot.send_voice(target_user, message.voice.file_id)
        elif message.photo:
            context.bot.send_photo(target_user, message.photo[-1].file_id)
        elif message.document:
            context.bot.send_document(target_user, message.document.file_id)
        elif message.sticker:
            context.bot.send_sticker(target_user, message.sticker.file_id)
        elif message.video:
            context.bot.send_video(target_user, message.video.file_id)
        elif message.audio:
            context.bot.send_audio(target_user, message.audio.file_id)

# الدالة الرئيسية
def main() -> None:
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dispatcher.add_handler(MessageHandler(Filters.all & Filters.reply, handle_reply))
    dispatcher.add_handler(CallbackQueryHandler(button_handler))
    
    print("✅ البوت يعمل... 🚀")
    print("✅ جميع الأزرار جاهزة!")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()