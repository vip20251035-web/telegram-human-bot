import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# 直接写死在代码里（先方便测试，后续你可以改成环境变量）
BOT_TOKEN = "8459427184:AAHUXVkLgXUmU6VMkcIRl2G0gVX9Rb2vlAE"
ADMIN_ID = 8282360229  # 你的 Telegram 用户 ID

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("你好，我是表妹的机器人！发送任何消息我会转发给表妹。")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text or ""
    if chat_id == ADMIN_ID:
        await update.message.reply_text("管理员提示：要回复用户请使用：/reply <user_chat_id> <message>")
        return
    forward_text = f"来自用户 {chat_id}：\n{text}"
    await context.bot.send_message(chat_id=ADMIN_ID, text=forward_text)
    await update.message.reply_text("你的消息已发送给表妹，她会回复你。")

async def reply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ADMIN_ID:
        return
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("用法：/reply <user_chat_id> <message>")
        return
    try:
        target = int(args[0])
    except ValueError:
        await update.message.reply_text("错误：第一个参数必须是用户的 chat_id（数字）。")
        return
    text = " ".join(args[1:])
    await context.bot.send_message(chat_id=target, text=f"管理员回复：{text}")
    await update.message.reply_text("已发送给用户。")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reply", reply_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
