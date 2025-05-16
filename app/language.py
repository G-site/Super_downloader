translations = {
    "en": {
        "start": "👋 Welcome to the bot!\n🤖 This bot can download videos from YouTube, TikTok, and other popular platforms!\nJust send the video link and the bot will do everything for you!",
        "language_selected": "✅ You have selected English.",
        "btn_profile": "👤 My Profile",
        "btn_help": "🔊 Help",
        "btn_use_help": "📰 Our Telegram Channel",
        "btn_creator": "📲 Contact Us",
        "btn_index": "↩ Back to Main",
        "help": "❗ Help Menu:\n🔰 If you have any questions, contact the creator!\n‼🔰 You can also visit our Telegram channel for news and answers to all your questions!",
        "profile": "👤 Welcome, {name}!\n⏭Your downloads: {balance}\n🙋‍♂️ Your language: {lang}\n‼Status: {status}",
        "lets_go": "▶ Start",
        "lets_go_txt": "💭 Send me the video link!",
        "inicilization": "🔄 Initializing ...",
        "incorect_link": "⚠️ Invalid link",
        "system_error": "⚠️ System error",
        "download": "⏬ Downloading ...",
        "send": "✅ Sending ...",
        "choose": "🎞 Choose quality:",
        "search": "🔍 Searching for video ...",
        "admin_status": "❌ You are not an administrator!",
        "subscribe": "<b>📢 Support the project!</b>\nSubscribe to our Telegram channel to stay updated with news and useful tips!\nThank you for being with us 💙",
        "share": "<b>📢 Support the project!</b>\nShare the bot with your friends — it helps us grow and improve! 💙",
        "update": "<b>🔧 Important Announcement</b>\n\nDear users! 🚀\n\n<u>Super Downloader Bot</u> will be temporarily unavailable due to <b>technical maintenance</b>.\n\n📌 What does it mean?\nDuring this time, the bot <i>will not be able to process requests</i> or download videos.\n\nThank you for your understanding!\nWe are working to make the service even better 💙",
        "btn_subscribe": "✔ Subscribe",
        "btn_share": "✔ Share"
    },
    "ru": {
        "start": "👋 Добро пожаловать в бот!\n🤖Этот бот может скачивать видео с Youtube, TikTok и других популярных платформ!\nСкинь ссылку на видео и бот сделает все за тебя!",
        "language_selected": "✅ Вы выбрали Руский язык.",
        "btn_profile": "👤 Мой профиль",
        "btn_help": "🔊 Помощь",
        "btn_use_help": "📰 Наш Телеграм канал",
        "btn_creator": "📲 Связаться с нами",
        "btn_index": "↩На главную",
        "help": "❗ Меню помощи:\n🔰 Если возникли какие-то вопросы напиши создателю!\n🔰 акже можешь зайти в наш Телеграм канал, там есть новости иответы на любые вопросы!",
        "profile": "👤 Добро пожаловать, {name}!\n⏭Ваши скачивания: {balance}\n🙋‍♂️ Ваш язык: {lang}\n‼Cтатус: {status}",
        "lets_go": "▶ Начать",
        "lets_go_txt": "💭 Скиньте мне ссылку на видео!", #
        "inicilization": "🔄 Инициализация ...",
        "incorect_link": "⚠️ Некоректная ссылка",
        "system_error": "⚠️ Системная ошибка",
        "download": "⏬ Скачиваю ...",
        "send": "✅ Отправляю ...",
        "choose": "🎞 Выбери качество:",
        "search": "🔍 Ищу видео ...",
        "admin_status": "❌ Вы не являетесь администратором!",
        "subscribe": "<b>📢 Поддержи проект!</b>\nПодпишись на наш Telegram-канал, чтобы не пропустить обновления, новости и полезные советы!\nСпасибо, что ты с нами 💙",
        "share": "<b>📢 Поддержи проект!</b>\nПоделись ботом с друзьями — это поможет нам расти и становиться лучше! 💙",
        "update": "<b>🔧 Важное объявление</b>\n\nДорогие пользователи! 🚀\n\nВ ближайшее время <u>Super Downloader Бот</u> будет временно недоступен в связи с <b>техническим обслуживанием</b>.\n\n📌 Что это значит?\nВ это время бот <i>не сможет обрабатывать запросы</i> и скачивать видео.\n\n Благодарим за понимание!\nМы работаем над тем, чтобы сделать сервис ещё лучше 💙",
        "btn_subscribe": "✔ Подписаться",
        "btn_share": "✔ Поделиться",
    }
}


def get_text(lang, key):
    return translations.get(lang, translations["ru"]).get(key, key)
