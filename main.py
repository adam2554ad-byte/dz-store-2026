import logging
import os
from flask import Flask, request
import telebot
from telebot import types

# إعداد التسجيل لمتابعة الأخطاء
logging.basicConfig(level=logging.INFO)

# جلب التوكن والأيدي مباشرة وبأمان
TOKEN = "8874439054:AAEM1I97sqGvWQzH4BDAQsSDbGCQu4c9cpu"
ADMIN_CHAT_ID = "-5457819425"

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# تخزين مؤقت لحالة طلبات الزبائن
pending_orders = {}


@app.route("/" + TOKEN, methods=["POST"])
def getMessage():
  json_string = request.get_data().decode("utf-8")
  update = telebot.types.Update.de_json(json_string)
  bot.process_new_updates([update])
  return "!", 200


@app.route("/")
def webhook():
  bot.remove_webhook()
  # وضع رابط Web Service الخاص بك هنا يدويا إذا لزم الأمر:
  # bot.set_webhook(url='https://اسم-مشروعك.onrender.com/' + TOKEN)
  return "DZ Star Store Bot is running!", 200


# القائمة الرئيسية للمتجر عند /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
  markup = types.InlineKeyboardMarkup(row_width=1)
  markup.add(
      types.InlineKeyboardButton(
          "🔥 شحن فري فاير", callback_data="service_ff"
      ),
      types.InlineKeyboardButton(
          "🌐 حسابات غوغل أمريكية جاهزة", callback_data="service_google"
      ),
      types.InlineKeyboardButton(
          "💳 تعبئة بطاقات ودعم", callback_data="service_cards"
      ),
      types.InlineKeyboardButton(
          "📞 التواصل مع الدعم", callback_data="service_support"
      ),
  )

  bot.send_message(
      message.chat.id,
      "أهلاً بك في متجر **DZ Star Store** 🌟\nيرجى اختيار الخدمة المطلوبة من القائمة أسفله:",
      parse_mode="Markdown",
      reply_markup=markup,
  )


# استقبال اختيار الخدمات
@bot.callback_query_handler(
    func=lambda call: call.data.startswith("service_")
)
def handle_services(call):
  chat_id = call.message.chat.id
  if call.data == "service_ff":
    msg = bot.send_message(
        chat_id, "أرسل لي الآيدي (ID) الخاص بك في فري فاير:"
    )
    bot.register_next_step_handler(msg, process_order_request)
  elif call.data == "service_google":
    msg = bot.send_message(
        chat_id, "أرسل لي البريد أو الخدمة المطلوبة لحسابات غوغل:"
    )
    bot.register_next_step_handler(msg, process_order_request)
  elif call.data == "service_cards":
    msg = bot.send_message(
        chat_id, "أكتب لي البطاقة أو الخدمة المالية المطلوبة وقيمتها:"
    )
    bot.register_next_step_handler(msg, process_order_request)
  elif call.data == "service_support":
    bot.send_message(
        chat_id,
        "للتواصل المباشر مع الإدارة يرجى مراسلة: @Admin_Username\nنحن في خدمتك دائماً.",
    )


# معالجة الطلب وإرساله للإدارة قبل الدفع
def process_order_request(message):
  user_id = message.from_user.id
  user_name = message.from_user.first_name
  username = (
      f"@{message.from_user.username}"
      if message.from_user.username
      else "بدون معرف"
  )
  order_text = message.text

  # حفظ تفاصيل الطلب مؤقتاً
  pending_orders[user_id] = {
      "name": user_name,
      "username": username,
      "order": order_text,
  }

  # إرسال تفاصيل الطلب لقروب الإدارة مع أزرار التأكيد أو الرفض
  admin_markup = types.InlineKeyboardMarkup(row_width=2)
  admin_markup.add(
      types.InlineKeyboardButton(
          "✅ قبول الطلب", callback_data=f"accept_{user_id}"
      ),
      types.InlineKeyboardButton(
          "❌ رفض الطلب", callback_data=f"reject_{user_id}"
      ),
  )

  admin_message = (
      f"🚨 **طلب جديد وصل للمتجر!**\n\n"
      f"👤 **الزبون:** {user_name} ({username})\n"
      f"🆔 **أيدي الزبون:** `{user_id}`\n"
      f"📦 **تفاصيل الطلب:** {order_text}"
  )

  bot.send_message(ADMIN_CHAT_ID, admin_message, parse_mode="Markdown", reply_markup=admin_markup)
  bot.send_message(
      message.chat.id,
      "✅ تم إرسال طلبك بنجاح إلى الإدارة!\nسيتم مراجعته والتواصل معك قريباً.",
  )


# تفاعل الإدارة مع الطلبات (قبول أو رفض)
@bot.callback_query_handler(func=lambda call: call.data.startswith(("accept_", "reject_")))
def handle_admin_decision(call):
  action, target_user_id = call.data.split("_")
  target_user_id = int(target_user_id)

  if action == "accept":
    bot.send_message(
        target_user_id,
        "🎉 مبروك! تم قبول طلبك من طرف الإدارة. يرجى إتمام عملية الدفع لإستلام خدمتك.",
    )
    bot.answer_callback_query(call.id, "تم إرسال قبول الطلب للزبون.")
    bot.edit_message_text(
        f"{call.message.text}\n\n✅ **الحالة:** تم قبول الطلب",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="Markdown",
    )
  else:
    bot.send_message(
        target_user_id,
        "❌ نعتذر، تم رفض طلبك من طرف الإدارة أو نفذت الكمية. يجدر بك التواصل مع الدعم للمزيد من التفاصيل.",
    )
    bot.answer_callback_query(call.id, "تم إرسال رفض الطلب للزبون.")
    bot.edit_message_text(
        f"{call.message.text}\n\n❌ **الحالة:** تم رفض الطلب",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="Markdown",
    )


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000))) 
