import logging
import telebot
from telebot import types

# إعدادات التسجيل والمراقبة
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# توكن البوت (استبدله بتوكن بوتك الجديد من BotFather)
TOKEN = "8874439054:AAEM1I97sqGvWQzH4BDAQsSdBGcQU4c9cpU"

# اسم المستخدم الخاص بالإدارة لتلقي الطلبات (يمكنك تعديله لاحقاً)
ADMIN_USERNAME = "@YourUsername"

bot = telebot.TeleBot(TOKEN)

# تخزين مؤقت لبيانات طلبات المستخدمين
user_orders = {}


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
  user_name = message.from_user.first_name
  markup = types.InlineKeyboardMarkup(row_width=2)

  # أزرار القائمة الرئيسية المتقدمة
  btn_games = types.InlineKeyboardButton(
      "🔥 شحن الألعاب والشدات", callback_data="games_topup"
  )
  btn_buy_usdt = types.InlineKeyboardButton(
      "💱 شراء عملات الرقمية USDT", callback_data="buy_usdt"
  )
  btn_sell_usdt = types.InlineKeyboardButton(
      "💳 بيع العملات الرقمية USDT", callback_data="sell_usdt"
  )
  btn_cards = types.InlineKeyboardButton(
      "🎫 البطاقات الرقمية وتعبئة الحسابات", callback_data="cards_recharge"
  )
  btn_accounts = types.InlineKeyboardButton(
      "🌐 تفعيل المنصات والنتفليكس", callback_data="accounts_service"
  )
  btn_trust = types.InlineKeyboardButton(
      "⭐ ضماناتنا وآراء الزبائن", callback_data="trust_section"
  )
  btn_support = types.InlineKeyboardButton(
      "💬 التواصل المباشر مع الإدارة", callback_data="support_direct"
  )

  markup.add(
      btn_games, btn_buy_usdt, btn_sell_usdt, btn_cards, btn_accounts
  )
  markup.add(btn_trust, btn_support)

  welcome_msg = (
      f"🌟 **أهلاً بك يا أخي {user_name} في البوابة الرسمية لـ DZ Star Store** 🌟\n\n"
      "💎 *متجرك الأقوى والأكثر موثوقية للخدمات الرقمية، شحن الألعاب، وتجارة العملات الرقمية في الجزائر.*\n\n"
      "🚀 **لماذا تختارنا؟**\n"
      "• سرعة فائقة في تنفيذ الطلبات (فوري).\n"
      "• أسعار تنافسية ومصداقية تامة في المعاملات.\n"
      "• دعم فني متواصل لمساعدتك في كل خطوة.\n\n"
      "👇 *اختر الخدمة التي تناسبك وابدأ طلبك الآن:*"
  )

  bot.send_message(
      message.chat.id,
      welcome_msg,
      reply_markup=markup,
      parse_mode="Markdown",
  )


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
  chat_id = call.message.chat.id
  user_id = call.from_user.id

  if call.data == "games_topup":
    user_orders[user_id] = {"category": "شحن الألعاب"}
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("فري فاير (Free Fire)", callback_data="ff"),
        types.InlineKeyboardButton("ببجي موبايل (PUBG)", callback_data="pubg"),
        types.InlineKeyboardButton("ألعاب أخرى", callback_data="other_game"),
        types.InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu")
    )
    bot.edit_message_text(
        "🎮 **قسم شحن الألعاب:**\nاختر اللعبة المراد شحنها:",
        chat_id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown",
    )

  elif call.data in ["ff", "pubg", "other_game"]:
    game_name = (
        "فري فاير"
        if call.data == "ff"
        else "ببجي موبايل"
        if call.data == "pubg"
        else "لعبة أخرى"
    )
    user_orders[user_id]["game"] = game_name
    msg = bot.send_message(
        chat_id,
        f"🎯 لقد اخترت شحن **{game_name}**.\n\n"
        "الرجاء كتابة تفاصيل طلبك بدقة:\n"
        "*(أدخل الآيدي الخاص بك ID، الكمية المطلوبة، أو الباقة المراد شراؤها)*",
        parse_mode="Markdown",
    )
    bot.register_next_step_handler(msg, process_order_input)

  elif call.data == "buy_usdt":
    user_orders[user_id] = {"category": "شراء USDT"}
    msg = bot.send_message(
        chat_id,
        "💱 **شراء العملات الرقمية USDT:**\n\n"
        "الرجاء كتابة تفاصيل طلبك:\n"
        "*(مثال: كمية الـ USDT المطلوبة + طريقة الدفع المفضلة لديك CCP أو فليكسي)*",
        parse_mode="Markdown",
    )
    bot.register_next_step_handler(msg, process_order_input)

  elif call.data == "sell_usdt":
    user_orders[user_id] = {"category": "بيع USDT"}
    msg = bot.send_message(
        chat_id,
        "💳 **بيع العملات الرقمية USDT:**\n\n"
        "الرجاء كتابة تفاصيل طلبك:\n"
        "*(مثال: الكمية التي تريد بيعها ورقم حساب الاستلام الخاص بك)*",
        parse_mode="Markdown",
    )
    bot.register_next_step_handler(msg, process_order_input)

  elif call.data == "cards_recharge":
    user_orders[user_id] = {"category": "بطاقات رقمية"}
    msg = bot.send_message(
        chat_id,
        "🎫 **شحن البطاقات الرقمية:**\n\n"
        "الرجاء كتابة اسم البطاقة والقيمة المطلوبة:\n"
        "*(مثل: بايونير، ريزير غولد، غوغل بلاي، بطاقات أخرى...)*",
        parse_mode="Markdown",
    )
    bot.register_next_step_handler(msg, process_order_input)

  elif call.data == "accounts_service":
    user_orders[user_id] = {"category": "تفعيل حسابات ومنصات"}
    msg = bot.send_message(
        chat_id,
        "🌐 **تفعيل المنصات الرقمية:**\n\n"
        "الرجاء كتابة اسم المنصة المطلوبة:\n"
        "*(مثل: نتفليكس، شات جي بي تي بلس، سبوتيفاي، إلخ...)*",
        parse_mode="Markdown",
    )
    bot.register_next_step_handler(msg, process_order_input)

  elif call.data == "trust_section":
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 عودة للقائمة", callback_data="main_menu"))
    trust_text = (
        "⭐ **ضمانات DZ Star Store:**\n\n"
        "✔ نحن نعمل بمصداقية كاملة ومعاملات قانونية وآمنة.\n"
        "✔ تم تنفيذ مئات الطلبات الناجحة لزبائننا الكرام عبر الوطن.\n"
        "✔ نضمن لك حقك كاملًا وسرعة التنفيذ فور تأكيد الدفع.\n"
        "ثقتكم هي رأس مالنا الحقيقي 🤝"
    )
    bot.edit_message_text(
        trust_text,
        chat_id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown",
    )

  elif call.data == "support_direct":
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "📩 اضغط هنا للتحدث مع الإدارة مباشرة",
            url=f"https://t.me/{ADMIN_USERNAME.replace('@', '')}",
        )
    )
    markup.add(types.InlineKeyboardButton("🔙 عودة للقائمة", callback_data="main_menu"))
    bot.edit_message_text(
        "💬 **الدعم الفني المباشر:**\n\n"
        "للاستفسار أو تأكيد الطلبات، يمكنك التواصل معنا مباشرة عبر معرف الإدارة الرسمي:",
        chat_id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown",
    )

  elif call.data == "main_menu":
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🔥 شحن الألعاب والشدات", callback_data="games_topup"),
        types.InlineKeyboardButton("💱 شراء عملات الرقمية USDT", callback_data="buy_usdt"),
        types.InlineKeyboardButton("💳 بيع العملات الرقمية USDT", callback_data="sell_usdt"),
        types.InlineKeyboardButton("🎫 البطاقات الرقمية وتعبئة الحسابات", callback_data="cards_recharge"),
        types.InlineKeyboardButton("🌐 تفعيل المنصات والنتفليكس", callback_data="accounts_service"),
        types.InlineKeyboardButton("⭐ ضماناتنا وآراء الزبائن", callback_data="trust_section"),
        types.InlineKeyboardButton("💬 التواصل المباشر مع الإدارة", callback_data="support_direct")
    )
    bot.edit_message_text(
        "🌟 **القائمة الرئيسية - DZ Star Store** 🌟\n\nاختر الخدمة المطلوبة:",
        chat_id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown",
    )


def process_order_input(message):
  chat_id = message.chat.id
  user_id = message.from_user.id
  user_text = message.text

  if user_id in user_orders:
    user_orders[user_id]["details"] = user_text
    category = user_orders[user_id].get("category", "خدمة رقمية")
  else:
    category = "خدمة عامة"

  markup = types.InlineKeyboardMarkup(row_width=1)
  contact_btn = types.InlineKeyboardButton(
      "🚀 التواصل مع الإدارة",
      url=f"https://t.me/{ADMIN_USERNAME.replace('@', '')}",
  )
  menu_btn = types.InlineKeyboardButton("🏠 العودة للرئيسية", callback_data="main_menu")
  markup.add(contact_btn, menu_btn)

  success_msg = (
      "✅ **تم تجهيز طلبك بنجاح واحترافية تامة!**\n\n"
      f"📌 **نوع الخدمة:** {category}\n"
      f"📝 **تفاصيل طلبك:** {user_text}\n\n"
      "━━━━━━━━━━━━━━━\n"
      f"📩 **يرجى ارسال طلبك للحساب التالي لي يتم تأكيد طلبك:** {ADMIN_USERNAME}"
  )

  bot.send_message(chat_id, success_msg, reply_markup=markup, parse_mode="Markdown")


if __name__ == "__main__":
  print("DZ Star Store Advanced Bot is online and running successfully...")
  bot.infinity_polling()
