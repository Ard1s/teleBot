from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Команды бота
START, MENU = range(2)

# Функция для старта бота
def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text(
        f"Привет, {user.first_name}! Я бот. Чем могу помочь?",
        reply_markup=main_menu_markup(),
    )
    return MENU

# Функция для обработки нажатий на кнопки меню
def main_menu(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Что вы хотите сделать?",
        reply_markup=main_menu_markup(),
    )
    return MENU

# Функция для создания меню
def main_menu_markup() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("Играть в игры", callback_data='games'),
            InlineKeyboardButton("Выбрать фильм", callback_data='film'),
        ],
        [
            InlineKeyboardButton("Расшифровать голосовое", callback_data='voice'),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

# Функция для обработки выбора игры
def games(update: Update, context: CallbackContext) -> None:
    update.callback_query.answer()
    update.callback_query.edit_message_text(text="Игры скоро будут доступны!")

# Функция для обработки выбора фильма
def film(update: Update, context: CallbackContext) -> None:
    update.callback_query.answer()
    update.callback_query.edit_message_text(text="Пока что выбор фильма недоступен!")

# Функция для обработки выбора расшифровки голосового
def voice(update: Update, context: CallbackContext) -> None:
    update.callback_query.answer()
    update.callback_query.edit_message_text(text="Расшифровка голосового в процессе разработки...")

def main() -> None:
    updater = Updater("")

    # Добавляем обработчики команд и сообщений
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [
                CallbackQueryHandler(main_menu, pattern='^' + 'main_menu' + '$'),
                CallbackQueryHandler(games, pattern='^' + 'games' + '$'),
                CallbackQueryHandler(film, pattern='^' + 'film' + '$'),
                CallbackQueryHandler(voice, pattern='^' + 'voice' + '$'),
            ],
        },
        fallbacks=[],
    )
    dispatcher.add_handler(conv_handler)

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
