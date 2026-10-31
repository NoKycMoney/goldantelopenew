import os
import asyncio
import requests
import json
import threading

def _get_token():
    return os.environ.get('TELEGRAM_BOT_TOKEN', '').strip()

def get_webapp_url():
    # 1. Explicit override
    explicit = os.environ.get('WEBAPP_URL', '').strip()
    if explicit:
        return explicit.rstrip('/')
    # 2. Replit published domain (production)
    domains = os.environ.get('REPLIT_DOMAINS', '')
    if domains:
        return f"https://{domains.split(',')[0]}"
    # 3. Replit dev domain
    dev_domain = os.environ.get('REPLIT_DEV_DOMAIN', '')
    if dev_domain:
        return f"https://{dev_domain}"
    # 4. Railway auto-domain
    railway = os.environ.get('RAILWAY_PUBLIC_DOMAIN', '').strip()
    if railway:
        return f"https://{railway}"
    return "https://goldantelope-asia.replit.app"

def send_message(chat_id, text, reply_markup=None):
    url = f'https://api.telegram.org/bot{_get_token()}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    if reply_markup:
        data['reply_markup'] = json.dumps(reply_markup)
    try:
        return requests.post(url, data=data, timeout=10).json()
    except Exception:
        return {}

def set_bot_description():
    token = _get_token()
    desc = (
        "Визаран Вьетнам — быстрые поездки на границу из Нячанга, Дананга и Хошимина.\n"
        "Также в приложении:\n"
        "• Аренда жилья во Вьетнаме\n"
        "• Обмен денег (USDT/VND)\n"
        "• Развлечения и экскурсии"
    )
    requests.post(
        f'https://api.telegram.org/bot{token}/setMyDescription',
        json={'description': desc},
        timeout=10
    )
    requests.post(
        f'https://api.telegram.org/bot{token}/setMyShortDescription',
        json={'short_description': 'Визаран, аренда жилья, обмен денег и развлечения во Вьетнаме'},
        timeout=10
    )

def set_bot_commands():
    url = f'https://api.telegram.org/bot{_get_token()}/setMyCommands'
    commands = [
        {"command": "start",    "description": "Запустить бота: меню и услуги во Вьетнаме"},
        {"command": "visarun",  "description": "Визаран Вьетнам: запись и актуальные цены"},
        {"command": "rent",     "description": "Аренда жилья: Нячанг, Дананг, Хошимин"},
        {"command": "exchange", "description": "Обмен денег: наличные и USDT (VND)"},
        {"command": "tours",    "description": "Развлечения: экскурсии, дайвинг, билеты"},
        {"command": "crypto",   "description": "Трейдинг: сигналы и личный кабинет"},
    ]
    data = {'commands': json.dumps(commands)}
    return requests.post(url, data=data).json()

def set_menu_button():
    url = f'https://api.telegram.org/bot{_get_token()}/setChatMenuButton'
    webapp_url = SITE_URL
    menu_button = {
        "type": "web_app",
        "text": "Open",
        "web_app": {"url": webapp_url}
    }
    data = {'menu_button': json.dumps(menu_button)}
    return requests.post(url, data=data).json()

SITE_URL = 'https://goldantelopeasia.com'

LANGUAGE_LABELS = {
    'ru': '🇷🇺 Русский',
    'en': '🇬🇧 English',
    'vi': '🇻🇳 Tiếng Việt',
    'th': '🇹🇭 ไทย',
}

WELCOME_TEXT = {
    'ru': (
        '👋 <b>Добро пожаловать в Goldantelope ASIA!</b>\n\n'
        'Сервисы и объявления Юго-Восточной Азии в одном месте:\n'
        '• аренда жилья и недвижимость\n'
        '• транспорт и байки\n'
        '• развлечения, рестораны и туры\n'
        '• обмен валюты и P2P\n\n'
        'Выберите язык ниже или откройте приложение.\n\n'
        '🌐 Сайт: <a href="https://goldantelopeasia.com">goldantelopeasia.com</a>'
    ),
    'en': (
        '👋 <b>Welcome to Goldantelope ASIA!</b>\n\n'
        'Services and listings across Southeast Asia in one place:\n'
        '• rentals and real estate\n'
        '• transport and bikes\n'
        '• entertainment, restaurants and tours\n'
        '• currency exchange and P2P\n\n'
        'Choose your language below or open the app.\n\n'
        '🌐 Website: <a href="https://goldantelopeasia.com">goldantelopeasia.com</a>'
    ),
    'vi': (
        '👋 <b>Chào mừng bạn đến với Goldantelope ASIA!</b>\n\n'
        'Dịch vụ và tin đăng Đông Nam Á trong một nơi:\n'
        '• cho thuê nhà và bất động sản\n'
        '• phương tiện và xe máy\n'
        '• giải trí, nhà hàng và tour\n'
        '• đổi tiền và P2P\n\n'
        'Chọn ngôn ngữ bên dưới hoặc mở ứng dụng.\n\n'
        '🌐 Website: <a href="https://goldantelopeasia.com">goldantelopeasia.com</a>'
    ),
    'th': (
        '👋 <b>ยินดีต้อนรับสู่ Goldantelope ASIA!</b>\n\n'
        'บริการและประกาศต่าง ๆ ในเอเชียตะวันออกเฉียงใต้:\n'
        '• เช่าที่พักและอสังหาริมทรัพย์\n'
        '• การเดินทางและรถจักรยานยนต์\n'
        '• ความบันเทิง ร้านอาหาร และทัวร์\n'
        '• แลกเปลี่ยนเงินและ P2P\n\n'
        'เลือกภาษาด้านล่างหรือเปิดแอปพลิเคชัน\n\n'
        '🌐 เว็บไซต์: <a href="https://goldantelopeasia.com">goldantelopeasia.com</a>'
    ),
}

def _language_keyboard():
    return {
        'keyboard': [
            [
                {'text': LANGUAGE_LABELS['ru']},
                {'text': LANGUAGE_LABELS['en']},
            ],
            [
                {'text': LANGUAGE_LABELS['vi']},
                {'text': LANGUAGE_LABELS['th']},
            ],
            [
                {'text': '🌐 Открыть приложение', 'web_app': {'url': SITE_URL}},
            ],
        ],
        'resize_keyboard': True,
        'is_persistent': True,
        'input_field_placeholder': 'Выберите язык / Choose language',
    }

def handle_start(chat_id, user_name, language='ru'):
    language = language if language in WELCOME_TEXT else 'ru'
    fallback_names = {'ru': 'друг', 'en': 'friend', 'vi': 'bạn', 'th': 'เพื่อน'}
    name = user_name or fallback_names[language]
    text = WELCOME_TEXT[language]
    if language == 'ru':
        text = text.replace('Добро пожаловать в Goldantelope ASIA!', f'Добро пожаловать, {name}, в Goldantelope ASIA!')
    elif language == 'en':
        text = text.replace('Welcome to Goldantelope ASIA!', f'Welcome to Goldantelope ASIA, {name}!')
    elif language == 'vi':
        text = text.replace('Chào mừng bạn đến với Goldantelope ASIA!', f'Chào mừng {name} đến với Goldantelope ASIA!')
    elif language == 'th':
        text = text.replace('ยินดีต้อนรับสู่ Goldantelope ASIA!', f'ยินดีต้อนรับ {name} สู่ Goldantelope ASIA!')
    keyboard = _language_keyboard()

    # Отправляем сообщение СРАЗУ — не блокируемся
    result = send_message(chat_id, text, keyboard)

    # Открепляем старые сообщения в фоне — не задерживает ответ
    def _unpin():
        try:
            requests.post(
                f'https://api.telegram.org/bot{_get_token()}/unpinAllChatMessages',
                json={'chat_id': chat_id},
                timeout=5
            )
        except Exception:
            pass
    threading.Thread(target=_unpin, daemon=True).start()

    return result

def handle_app(chat_id):
    site_url = "https://goldantelopeasia.com"
    
    text = "🚀 Нажмите кнопку, чтобы открыть приложение:"
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "🌐 Открыть Goldantelope ASIA", "url": site_url}]
        ]
    }
    
    return send_message(chat_id, text, keyboard)

def setup_bot():
    print("Setting up bot...")

    set_bot_description()
    print("Description: set")

    result1 = set_bot_commands()
    print(f"Commands: {result1}")

    result2 = set_menu_button()
    print(f"Menu button: {result2}")

    print(f"Web App URL: {get_webapp_url()}")
    print("Bot setup complete!")

if __name__ == "__main__":
    setup_bot()
