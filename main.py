import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# إعداد التسجيل لمتابعة الأخطاء
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# الآي دي الخاص بك لتلقي الإشعارات
ADMIN_CHAT_ID = "6846578647"

# مراحل المحادثة
CHOOSING_SERVICE, FREEFIRE_PACKAGES, GETTING_DETAILS, CONFIRMING = range(4)

# التوكن الخاص بـ DZ Star Store
TOKEN = "8874439054:AAEM1I97sqGvWQzH4BDAQsSdBGcQU4c9cpU"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  keyboard = [
      [
          InlineKeyboardButton(
              "🔥 شحن ألعاب (Free Fire)", callback_data="service_freefire"
          )
      ],
      [
          InlineKeyboardButton(
              "💵 عملات رقمية (USDT)", callback_data="service_usdt"
          )
      ],
      [
          InlineKeyboardButton(
              "📱 خدمات فليكسي (Flexy)", callback_data="service_flexy"
          )
      ],
      [
          InlineKeyboardButton(
              "💳 طرق الدفع ومعلومات الحسابات", callback_data="payment_methods"
          )
      ],
      [
          InlineKeyboardButton(
              "ℹ️ معلومات عن المتجر", callback_data="about_store"
          )
      ],
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)

  welcome_text = (
      "🌟 **مرحباً بك في متجر DZ Star Store** 🌟\n\n"
      "وجهتك الأولى والأوثق للخدمات الرقمية في الجزائر 🇩🇿.\n\n"
      "📌 **ما توفره خدماتنا في المتجر:**\n"
      "1️⃣ **شحن ألعاب (Free Fire):** شحن سريع وآمن عبر الـ Player ID.\n"
      "2️⃣ **عملات رقمية (USDT):** بيع وشراء USDT بطرق موثوقة.\n"
      "3️⃣ **خدمات فليكسي (Flexy):** تحويلات لجميع الشبكات.\n\n"
      "👇 **اختر الخدمة أو اطلع على طرق الدفع من الأزرار أدناه:**"
  )

  if update.message:
    await update.message.reply_text(
        welcome_text, reply_markup=reply_markup, parse_mode="Markdown"
    )
  elif update.callback_query:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        welcome_text, reply_markup=reply_markup, parse_mode="Markdown"
    )
  return CHOOSING_SERVICE


async def payment_methods(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()

  keyboard = [
      [InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="back_home")]
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)

  text = (
      "💳 **معلومات وطرق الدفع في متجر DZ Star Store:**\n\n"
      "يمكنك الدفع عبر الوسائل التالية المتوفرة لدينا:\n\n"
      "1️⃣ **CCP (بريدي):**\n"
      "• **رقم الحساب:** `00799999004305443758`\n"
      "• **الاسم:** `Adem Mousli`\n\n"
      "2️⃣ **Binance (باينانس):**\n"
      "• **الرقم التعريفي:** `954361593`\n\n"
      "3️⃣ **Flexy (فليكسي / هاتف):**\n"
      "• **رقم الهاتف:** `0796152180`\n\n"
      "⚠️ *ملاحظة:* بعد عملية الدفع، قم بإرسال وصل الاستلام مع تفاصيل طلبك للإدارة لتأكيده فوراً."
  )
  await query.edit_message_text(
      text, reply_markup=reply_markup, parse_mode="Markdown"
  )
  return CHOOSING_SERVICE


async def about_store(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()

  keyboard = [
      [InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="back_home")]
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)

  text = (
      "ℹ️ **حول متجر DZ Star Store:**\n\n"
      "نحن نسعى لتقديم أفضل الخدمات الرقمية بأسرع وقت وأفضل الأسعار.\n"
      "لدينا نظام طلبات آلي ومباشر ليصل طلبك للإدارة في ثوانٍ معدودة وتنفيذه بدقة عالية.\n\n"
      "خدمة العملاء في خدمتكم دائماً!"
  )
  await query.edit_message_text(
      text, reply_markup=reply_markup, parse_mode="Markdown"
  )
  return CHOOSING_SERVICE


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()
  choice = query.data

  if choice == "payment_methods":
    return await payment_methods(update, context)

  if choice == "about_store":
    return await about_store(update, context)

  if choice == "back_home":
    return await start(update, context)

  # إذا اختار شحن فري فاير، نخرجلو قائمة العروض (الجواهر)
  if choice == "service_freefire":
    context.user_data["service_name"] = "شحن ألعاب (Free Fire) 🔥"
    keyboard = [
        [
            InlineKeyboardButton(
                "💎 100 جوهرة (أساسية)", callback_data="ff_100"
            )
        ],
        [
            InlineKeyboardButton(
                "💎 310 جوهرة (الأكثر طلباً)", callback_data="ff_310"
            )
        ],
        [InlineKeyboardButton("💎 520 جوهرة", callback_data="ff_520")],
        [
            InlineKeyboardButton(
                "💎 1060 جوهرة (عروض خاصة)", callback_data="ff_1060"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 العودة للقائمة الرئيسية", callback_data="back_home"
            )
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "🎮 **اختر عرض شحن Free Fire المطلوب:**",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )
    return FREEFIRE_PACKAGES

  # باقي الخدمات (USDT و Flexy) يروحو دايركت يطلبوا التفاصيل
  context.user_data["service_choice"] = choice

  if choice == "service_usdt":
    context.user_data["service_name"] = "عملات رقمية (USDT) 💵"
    prompt_text = (
        "💵 **خدمة: عملات رقمية (USDT)**\n\n"
        "الرجاء إرسال التفاصيل التالية في رسالة واحدة:\n"
        "• **المبلغ المراد (USDT):**\n"
        "• **رقم محفظتك أو منصتك:**\n"
        "• **طريقة الدفع (CCP / فليكسي):**\n\n"
        "*(أكتب معلوماتك بوضوح وأرسلها الآن)*"
    )
  elif choice == "service_flexy":
    context.user_data["service_name"] = "خدمات فليكسي (Flexy) 📱"
    prompt_text = (
        "📱 **خدمة: خدمات فليكسي (Flexy)**\n\n"
        "الرجاء إرسال التفاصيل التالية في رسالة واحدة:\n"
        "• **رقم الهاتف المراد التحويل إليه:**\n"
        "• **نوع الشبكة (موبيليس / جيزي / أوريدو) والمبلغ:**\n"
        "• **طريقة الدفع (CCP / بريدي):**\n\n"
        "*(أكتب معلوماتك بوضوح وأرسلها الآن)*"
    )

  keyboard = [
      [InlineKeyboardButton("❌ إلغاء والعودة", callback_data="back_home")]
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)

  await query.edit_message_text(
      prompt_text, reply_markup=reply_markup, parse_mode="Markdown"
  )
  return GETTING_DETAILS


async def freefire_package_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
  query = update.callback_query
  await query.answer()
  choice = query.data

  if choice == "back_home":
    return await start(update, context)

  # تحديد الباقة لي اخترها الزبون
  packages_dict = {
      "ff_100": "100 جوهرة 💎",
      "ff_310": "310 جوهرة 💎",
      "ff_520": "520 جوهرة 💎",
      "ff_1060": "1060 جوهرة 💎",
  }

  selected_pkg = packages_dict.get(choice, "عرض فري فاير")
  context.user_data["selected_package"] = selected_pkg

  prompt_text = (
      f"🎮 **لقد اخترت: {selected_pkg}**\n\n"
      "الآن، الرجاء إرسال **Player ID (معرف اللاعب الخاص بك)** في رسالة واحدة:\n"
      "• **Player ID:**\n"
      "• **طريقة الدفع المختارة (CCP / باينانس / فليكسي):**\n\n"
      "*(أكتب معلوماتك بوضوح وأرسلها الآن)*"
  )

  keyboard = [
      [InlineKeyboardButton("❌ إلغاء والعودة", callback_data="back_home")]
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)

  await query.edit_message_text(
      prompt_text, reply_markup=reply_markup, parse_mode="Markdown"
  )
  return GETTING_DETAILS


async def receive_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_input = update.message.text
  context.user_data["user_details"] = user_input

  service_name = context.user_data.get("service_name")
  pkg = context.user_data.get("selected_package", "")
  full_service_name = (
      f"{service_name} ({pkg})" if pkg else service_name
  )

  summary_text = (
      f"📋 **ملخص طلبك (يرجى المراجعة قبل التأكيد):**\n\n"
      f"▫️ **الخدمة المختارة:** {full_service_name}\n"
      f"▫️ **التفاصيل والمعلومات المدخلة:**\n`{user_input}`\n\n"
      "هل أنت متأكد من صحة المعلومات وترغب في إرسال الطلب نهائياً للإدارة؟"
  )

  keyboard = [
      [
          InlineKeyboardButton("✅ تأكيد وإرسال الطلب", callback_data="confirm_yes"),
          InlineKeyboardButton("🔄 تعديل / إلغاء", callback_data="back_home"),
      ]
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)

  await update.message.reply_text(
      summary_text, reply_markup=reply_markup, parse_mode="Markdown"
  )
  return CONFIRMING


async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()

  if query.data == "back_home":
    return await start(update, context)

  service_name = context.user_data.get("service_name")
  pkg = context.user_data.get("selected_package", "")
  full_service_name = (
      f"{service_name} ({pkg})" if pkg else service_name
  )
  user_details = context.user_data.get("user_details")
  user = update.effective_user

  admin_message = (
      f"🚨 **تنبيه: طلب جديد مؤكد في المتجر!** 🚨\n\n"
      f"🛍 **الخدمة:** {full_service_name}\n"
      f"👤 **معلومات الزبون:**\n"
      f"• الاسم: {user.first_name}\n"
      f"• اليوزر: @{user.username or 'لا يوجد'}\n"
      f"• الايدي: `{user.id}`\n\n"
      f"📝 **تفاصيل الطلب والدفع المدخلة:**\n`{user_details}`"
  )

  try:
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID, text=admin_message, parse_mode="Markdown"
    )
  except Exception as e:
    print(f"خطأ في إرسال الإشعار للإدارة: {e}")

  success_text = (
      "✅ **تم إرسال طلبك بنجاح تام إلى الإدارة!**\n\n"
      "شكراً لثقتك في **DZ Star Store** 🌟\n"
      "يرجى إرسال إثبات الدفع (إن وجد) أو الانتظار ليتم التواصل معك قريباً.\n\n"
      "لإجراء طلب جديد، اضغط على /start"
  )

  await query.edit_message_text(success_text, parse_mode="Markdown")
  return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if update.message:
    await update.message.reply_text("تم إلغاء العملية. أرسل /start للبدء من جديد.")
  return ConversationHandler.END


def main():
  app = ApplicationBuilder().token(TOKEN).build()

  conv_handler = ConversationHandler(
      entry_points=[
          CommandHandler("start", start),
          CallbackQueryHandler(start, pattern="^back_home$"),
      ],
      states={
          CHOOSING_SERVICE: [
              CallbackQueryHandler(
                  button_handler,
                  pattern="^(service_|payment_methods|about_store|back_home)",
              )
          ],
          FREEFIRE_PACKAGES: [
              CallbackQueryHandler(
                  package_handler_router,
                  pattern="^(ff_|back_home)",
              )
          ],
          GETTING_DETAILS: [
              MessageHandler(
                  filters.TEXT & ~filters.COMMAND, receive_details
              ),
              CallbackQueryHandler(button_handler, pattern="^back_home$"),
          ],
          CONFIRMING: [
              CallbackQueryHandler(
                  confirm_order, pattern="^(confirm_yes|back_home)$"
              )
          ],
      },
      fallbacks=[CommandHandler("cancel", cancel)],
  )

  app.add_handler(conv_handler)

  print("🤖 بوت DZ Star Store يعمل الآن باحترافية تامة...")
  app.run_polling()


# دالة وسيطة لتوجيه اختيار الباقات
async def package_handler_router(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
  query = update.callback_query
  if query.data == "back_home":
    return await start(update, context)
  else:
    return await freefire_package_handler(update, context)


if __name__ == "__main__":
  main()
