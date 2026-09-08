import os
import logging
from flask import Flask, request
import telebot
from telebot import types

# إعداد التسجيل لمتابعة الأخطاء
logging.basicConfig(level=logging.INFO)

# التوكن والآيدي الخاص بك
TOKEN = "8874439054:AAEM1I97sqGvWQzH4BDAQsSDbGCQu4c9cpu"
ADMIN_CHAT_ID = "-5457819425"


bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# تخزين مؤقت لحالة طلبات الزبائن
pending_orders = {}

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    # ضع هنا رابط الـ Web Service الخاص بك في Render لاحقاً أو اتركه ليتعاطى أوتوماتيكياً
    # bot.set_webhook(url='https://اسم-مشروعك.onrender.com/' + TOKEN)
    return "DZ Star Store Bot is running!", 200

# القائمة الرئيسية للمتجر المتطور
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🔥 شحن فري فاير", callback_data="service_ff"),
        types.InlineKeyboardButton("🇺🇸 حسابات گوگل أمريكية جاهزة", callback_data="service_google"),
        types.InlineKeyboardButton("💳 تعبئة رصيد وبطاقات دفع", callback_data="service_cards"),
        types.InlineKeyboardButton("📞 التواصل مع الدعم", callback_data="support")
    )
    bot.send_message(
        message.chat.id,
        "مرحباً بك في *DZ Star Store* 🌟\nمتجرك المتطور للخدمات الرقمية وشحن الألعاب.\n\nاختر الخدمة المطلوبة من القائمة أسفله:",
        parse_mode="Markdown",
        reply_markup=markup
    )

# استقبال اختيار الخدمات
@bot.callback_query_handler(func=lambda call: call.data.startswith('service_'))
def handle_services(call):
    chat_id = call.message.chat.id
    if call.data == "service_ff":
        msg = bot.send_message(chat_id, "أرسل لي الآيدي (ID) الخاص بك في لعبة فري فاير مع تفاصيل العرض المطلوب:")
        bot.register_next_step_handler(msg, process_order_request)
    elif call.data == "service_google":
        msg = bot.send_message(chat_id, "أرسل لي البريد الإلكتروني أو التفاصيل الخاصة بطلب حساب گوگل الأمريكي المطلوب:")
        bot.register_next_step_handler(msg, process_order_request)
    elif call.data == "service_cards":
        msg = bot.send_message(chat_id, "حدد نوع البطاقة أو الخدمة المالية المطلوبة وقيمتها:")
        bot.register_next_step_handler(msg, process_order_request)

# معالجة الطلب وإرساله للإدارة قبل الدفع
def process_order_request(message):

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = message.from_user.username
    user_username = f"@{username}" if username else "بدون معرف"
    order_text = message.text    
     


    

    # حفظ تفاصيل الطلب مؤقتاً
    pending_orders[user_id] = order_text

    # إشعار الزبون بأن طلبه قيد المعالجة
    bot.send_message(
        message.chat.id,
        "⏳ تم استلام طلبك بنجاح وهو الآن قيد المراجعة والتحقق من التوفر لدى الإدارة. انتظر قليلاً من فضلك."
    )

    # إرسال إشعار للأدمن مع أزرار القبول أو الرفض
    admin_markup = types.InlineKeyboardMarkup(row_width=2)
    admin_markup.add(
        types.InlineKeyboardButton("✅ قبول الطلب", callback_data=f"accept_{user_id}"),
        types.InlineKeyboardButton("❌ رفض الطلب", callback_data=f"reject_{user_id}")
    )

    admin_msg = (
        f"🚨 *طلب جديد قيد الدراسة!*\n\n"
        f"👤 *الزبون:* {user_name} ({user_username})\n"
        f"🆔 *معرف المستخدم:* `{user_id}`\n\n"
        f"📦 *تفاصيل الطلب:* \n{order_text}"
    )
    
    bot.send_message(ADMIN_CHAT_ID, admin_msg, parse_mode="Markdown", reply_markup=admin_markup)

# التعامل مع قرارات الأدمن (قبول أو رفض)
@bot.callback_query_handler(func=lambda call: call.data.startswith('accept_') or call.data.startswith('reject_'))
def handle_admin_decision(call):
    data_parts = call.data.split('_')
    action = data_parts[0]
    user_id = int(data_parts[1])

    if action == "accept":
        # إعلام الأدمن
        bot.answer_callback_query(call.id, "تم قبول الطلب بنجاح!")
        bot.edit_message_text(
            f"{call.message.text}\n\n🟢 *الحالة:* تم قبول الطلب من طرف الإدارة.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="Markdown"
        )
        # إعلام الزبون وتوجيهه لمرحلة الدفع
        pay_markup = types.InlineKeyboardMarkup()
        pay_markup.add(types.InlineKeyboardButton("📤 إرسال وصل الدفع", callback_data="send_receipt"))
        bot.send_message(
            user_id,
            "🎉 *مبروك! لقد تم قبول طلبك وتأكيد توفره.*\n\nيرجى إتمام عملية الدفع وإرسال صورة الوصل لتسليمك الخدمة في أسرع وقت.",
            parse_mode="Markdown",
            reply_markup=pay_markup
        )

    elif action == "reject":
        # إعلام الأدمن
        bot.answer_callback_query(call.id, "تم رفض الطلب.")
        bot.edit_message_text(
            f"{call.message.text}\n\n🔴 *الحالة:* تم رفض الطلب أو الخدمة غير متوفرة حالياً.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="Markdown"
        )
        # إعلام الزبون بالرفض
        bot.send_message(
            user_id,
            "⚠️ نأسف، طلبك غير متوفر حالياً أو تم رفضه من قبل الإدارة. يمكنك المحاولة لاحقاً أو اختيار خدمة أخرى عبر /start"
        )

if __name__ == "__main__":
    app.host = "0.0.0.0"
    app.port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=app.port)
