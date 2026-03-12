#!/data/data/com.termux/files/usr/bin/python3
# Perxilitt - ЧИСТО ДЛЯ ПОНТА! (исправленная версия)

import os
import sys
import time
import pickle
import hashlib
import random
import string
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

# ===================== ДИСКЛЕЙМЕР =====================
DISCLAIMER = f"""
{Fore.YELLOW}╔══════════════════════════════════════════════════════════╗
║{Fore.WHITE}  ⚠️  ВНИМАНИЕ! ЮРИДИЧЕСКАЯ ИНФОРМАЦИЯ                  {Fore.YELLOW}║
╠══════════════════════════════════════════════════════════╣
║{Fore.WHITE}                                                          {Fore.YELLOW}║
║{Fore.WHITE}  Используя данное программное обеспечение, вы          {Fore.YELLOW}║
║{Fore.WHITE}  соглашаетесь с тем, что оно создано ИСКЛЮЧИТЕЛЬНО    {Fore.YELLOW}║
║{Fore.WHITE}  В РАЗВЛЕКАТЕЛЬНЫХ ЦЕЛЯХ.                              {Fore.YELLOW}║
║{Fore.WHITE}                                                          {Fore.YELLOW}║
║{Fore.WHITE}  • Все персонажи вымышлены                             {Fore.YELLOW}║
║{Fore.WHITE}  • Любые совпадения случайны                           {Fore.YELLOW}║
║{Fore.WHITE}  • Роли существуют только для красоты                  {Fore.YELLOW}║
║{Fore.WHITE}  • Коды ничего не открывают (кроме понтов)             {Fore.YELLOW}║
║{Fore.WHITE}  • Админка существует только в воображении             {Fore.YELLOW}║
║{Fore.WHITE}                                                          {Fore.YELLOW}║
║{Fore.WHITE}  Нажимая "Enter", вы подтверждаете, что вам           {Fore.YELLOW}║
║{Fore.WHITE}  есть 18 лет (или просто нажимаете кнопку)             {Fore.YELLOW}║
╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""

# ===================== ТАРИФЫ (ТОЛЬКО ДЛЯ РОЛЕЙ) =====================
PLANS = {
    'FREE': {
        'name': 'FREE',
        'quota': 999999,
        'price': '0 ₽',
        'color': Fore.GREEN,
        'features': ['ALL']
    },
    'VIP': {
        'name': 'VIP',
        'quota': 999999,
        'price': '0 ₽',
        'color': Fore.CYAN,
        'features': ['ALL']
    },
    'AUTHED': {
        'name': 'AUTHED',
        'quota': 999999,
        'price': '0 ₽',
        'color': Fore.BLUE,
        'features': ['ALL']
    },
    'UNLIMITED': {
        'name': 'UNLIMITED',
        'quota': 999999,
        'price': '0 ₽',
        'color': Fore.MAGENTA,
        'features': ['ALL']
    },
    'ADMIN': {
        'name': 'ADMIN',
        'quota': 999999,
        'price': '0 ₽',
        'color': Fore.RED,
        'features': ['ALL', 'admin_panel']
    }
}

# ===================== СЕКРЕТНЫЕ КОДЫ =====================
SECRET_CODES = {
    'V7XXA': {'plan': 'VIP', 'used': False, 'creator': 'superapps', 'created': '2024-01-01'},
    'V7XXB': {'plan': 'VIP', 'used': False, 'creator': 'superapps', 'created': '2024-01-01'},
    'V7XXC': {'plan': 'VIP', 'used': False, 'creator': 'superapps', 'created': '2024-01-01'},
    'RE10BB': {'plan': 'UNLIMITED', 'used': False, 'creator': 'superapps', 'created': '2024-01-01'},
    'RE10BC': {'plan': 'UNLIMITED', 'used': False, 'creator': 'superapps', 'created': '2024-01-01'},
    'RE10BD': {'plan': 'UNLIMITED', 'used': False, 'creator': 'superapps', 'created': '2024-01-01'},
    'Qertyy4cUw15': {'plan': 'ADMIN', 'used': False, 'creator': 'superapps', 'created': '2024-01-01'},
    'Qertyy4cUw16': {'plan': 'ADMIN', 'used': False, 'creator': 'superapps', 'created': '2024-01-01'},
    'Qertyy4cUw17': {'plan': 'ADMIN', 'used': False, 'creator': 'superapps', 'created': '2024-01-01'},
}

# ===================== АДМИНКА =====================
ADMIN_CREDENTIALS = {
    'superapps': hashlib.sha256('ghosty2024!'.encode()).hexdigest(),
    'rne_ghosty': hashlib.sha256('ghosty2024!'.encode()).hexdigest()
}

CONTACT = '@rne_ghosty'

class PerxilittShop:
    def __init__(self):
        self.show_disclaimer()
        self.user_data = self.load_user_data()
        self.today = datetime.now().date().isoformat()
        self.load_codes_status()
        self.is_admin = False

    def show_disclaimer(self):
        """Показывает дисклеймер при запуске"""
        os.system('clear')
        print(DISCLAIMER)
        input(f"\n{Fore.CYAN}Нажми Enter, если согласен (или закрой программу)...{Style.RESET_ALL}")
        os.system('clear')

    def load_user_data(self):
        if os.path.exists('perx_user.dat'):
            try:
                with open('perx_user.dat', 'rb') as f:
                    return pickle.load(f)
            except:
                return self.default_user()
        return self.default_user()

    def default_user(self):
        return {
            'plan': 'FREE',
            'used_codes': [],
            'total_searches': 0,
            'registered': datetime.now().isoformat(),
            'disclaimer_accepted': True
        }

    def load_codes_status(self):
        if os.path.exists('used_codes.dat'):
            try:
                with open('used_codes.dat', 'rb') as f:
                    used = pickle.load(f)
                    for code in used:
                        if code in SECRET_CODES:
                            SECRET_CODES[code]['used'] = True
            except:
                pass

    def save_codes_status(self):
        used = [code for code, data in SECRET_CODES.items() if data['used']]
        with open('used_codes.dat', 'wb') as f:
            pickle.dump(used, f)

    def save_user_data(self):
        with open('perx_user.dat', 'wb') as f:
            pickle.dump(self.user_data, f)

    def use_request(self):
        self.user_data['total_searches'] = self.user_data.get('total_searches', 0) + 1
        self.save_user_data()
        return True

    def activate_plan(self, plan_key):
        if plan_key in PLANS:
            self.user_data['plan'] = plan_key
            self.user_data['activated_date'] = datetime.now().isoformat()
            self.save_user_data()
            return True
        return False

    def check_code(self, code):
        code = code.strip().upper()
        if code in SECRET_CODES:
            if SECRET_CODES[code]['used']:
                return False, f"{Fore.RED}❌ Код уже использован!{Style.RESET_ALL}"
            plan = SECRET_CODES[code]['plan']
            self.activate_plan(plan)
            SECRET_CODES[code]['used'] = True
            SECRET_CODES[code]['used_by'] = 'user'
            SECRET_CODES[code]['used_date'] = datetime.now().isoformat()
            self.user_data['used_codes'].append(code)
            self.save_user_data()
            self.save_codes_status()
            return True, f"{Fore.GREEN}✅ Роль {plan} активирована! (чисто понты){Style.RESET_ALL}"
        return False, f"{Fore.RED}❌ Неверный код!{Style.RESET_ALL}"

    def show_banner(self):
        if self.user_data['plan'] == 'ADMIN':
            role_display = f"{Fore.RED}👑 АДМИН {Style.RESET_ALL}"
        elif self.user_data['plan'] == 'UNLIMITED':
            role_display = f"{Fore.MAGENTA}💎 UNLIMITED {Style.RESET_ALL}"
        elif self.user_data['plan'] == 'AUTHED':
            role_display = f"{Fore.BLUE}🔥 AUTHED {Style.RESET_ALL}"
        elif self.user_data['plan'] == 'VIP':
            role_display = f"{Fore.CYAN}⭐️ VIP {Style.RESET_ALL}"
        else:
            role_display = f"{Fore.GREEN}🆓 FREE {Style.RESET_ALL}"

        banner = f"""
{Fore.MAGENTA}██████╗ ███████╗██████╗ ██╗  ██╗██╗██╗     ██╗██╗  ██╗██╗████████╗
{Fore.CYAN}██╔══██╗██╔════╝██╔══██╗██║  ██║██║██║     ██║██║  ██║██║╚══██╔══╝
{Fore.BLUE}██████╔╝█████╗  ██████╔╝███████║██║██║     ██║███████║██║   ██║   
{Fore.YELLOW}██╔═══╝ ██╔══╝  ██╔══██╗██╔══██║██║██║     ██║██╔══██║██║   ██║   
{Fore.GREEN}██║     ███████╗██║  ██║██║  ██║██║███████╗██║██║  ██║██║   ██║   
{Fore.RED}╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚═╝╚═╝  ╚═╝╚═╝   ╚═╝   
{Style.RESET_ALL}

{Fore.WHITE}╔══════════════════════════════════════════════════════════╗
║{Fore.CYAN}              P E R X I L I T T   v 2 . 0                {Fore.WHITE}║
║{Fore.YELLOW}                    p l t _ b e t a                      {Fore.WHITE}║
║{Fore.GREEN}              by superapps-ui • ВСЕ БЕСПЛАТНО!            {Fore.WHITE}║
╠══════════════════════════════════════════════════════════╣
║{Fore.WHITE}  ⚠️  РАЗВЛЕКАТЕЛЬНОЕ ПО - ВСЕ ПОНТЫ                     {Fore.WHITE}║
╠══════════════════════════════════════════════════════════╣
║{Fore.YELLOW}  РОЛЬ: {role_display}{Fore.YELLOW}                                        {Fore.WHITE}║
╠══════════════════════════════════════════════════════════╣
║{Fore.YELLOW}  🎭 РОЛИ (ПРОСТО ДЛЯ ПОНТА):                           {Fore.WHITE}║
╠══════════════════════════════════════════════════════════╣
║{Fore.GREEN}  🆓 FREE      - по умолчанию (ничего не дает)          {Fore.WHITE}║
║{Fore.CYAN}  ⭐️ VIP       - красивый цвет                           {Fore.WHITE}║
║{Fore.BLUE}  🔥 AUTHED    - еще красивее                            {Fore.WHITE}║
║{Fore.MAGENTA}  👑 UNLIMITED - вообще пушка                            {Fore.WHITE}║
║{Fore.RED}  🛡 ADMIN     - для особо красивых                       {Fore.WHITE}║
╠══════════════════════════════════════════════════════════╣
║{Fore.CYAN}  🔐 ВВЕДИ КОД И ПОЛУЧИ КРАСИВУЮ РОЛЬ!                   {Fore.WHITE}║
╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(banner)
        
        # ИСПРАВЛЕНО: безопасное получение значения
        searches = self.user_data.get('total_searches', 0)
        print(f"{Fore.CYAN}📊 Статистика: сделано поисков: {searches} (просто цифра для красоты){Style.RESET_ALL}\n")

    def admin_login(self):
        print(f"\n{Fore.RED}🔐 АДМИН ПАНЕЛЬ PERXILITT (существует только в вашем воображении){Style.RESET_ALL}")
        username = input(f"{Fore.YELLOW}Логин: {Style.RESET_ALL}")
        password = input(f"{Fore.YELLOW}Пароль: {Style.RESET_ALL}")
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password_hash:
            self.is_admin = True
            return True
        return False

    def admin_panel(self):
        if not self.is_admin:
            print(f"{Fore.RED}Доступ запрещен! (но вы же понимаете, что это понты){Style.RESET_ALL}")
            return
        while True:
            os.system('clear')
            print(f"""
{Fore.RED}╔══════════════════════════════════════════╗
║    АДМИН ПАНЕЛЬ (ВЫДУМАННАЯ)            ║
╠══════════════════════════════════════════╣
║{Fore.WHITE}  1. Посмотреть коды (которые ничего не дают){Fore.RED}║
║{Fore.WHITE}  2. Создать код (еще один понт)           {Fore.RED}║
║{Fore.WHITE}  3. Удалить код (убрать понт)             {Fore.RED}║
║{Fore.WHITE}  4. Статистика (тоже понты)               {Fore.RED}║
║{Fore.WHITE}  5. Сбросить счетчик (обнулить понты)     {Fore.RED}║
║{Fore.WHITE}  6. Выдать роль (покрасить текст)         {Fore.RED}║
║{Fore.WHITE}  7. Использованные коды (кто повелся)     {Fore.RED}║
║{Fore.WHITE}  8. Выйти (надоело играть)                {Fore.RED}║
╚══════════════════════════════════════════╝{Style.RESET_ALL}
""")
            choice = input(f"{Fore.RED}admin@{Style.RESET_ALL} Выбор: ")
            if choice == '1':
                self.show_all_codes()
            elif choice == '2':
                self.create_code()
            elif choice == '3':
                self.delete_code()
            elif choice == '4':
                self.show_stats()
            elif choice == '5':
                self.reset_search_counter()
            elif choice == '6':
                self.give_plan()
            elif choice == '7':
                self.show_used_codes()
            elif choice == '8':
                self.is_admin = False
                break
            input(f"\n{Fore.YELLOW}Нажми Enter...{Style.RESET_ALL}")

    def show_all_codes(self):
        print(f"\n{Fore.CYAN}📋 ВСЕ КОДЫ (просто набор букв):{Style.RESET_ALL}\n")
        for code, data in SECRET_CODES.items():
            status = f"{Fore.GREEN}✅ Использован{Style.RESET_ALL}" if data['used'] else f"{Fore.YELLOW}🆓 Доступен{Style.RESET_ALL}"
            color = PLANS[data['plan']]['color']
            print(f"{color}{code}{Style.RESET_ALL} - {data['plan']} - {status}")
            if data.get('used') and 'used_by' in data:
                print(f"   Пользователь: {data['used_by']}")
                print(f"   Дата: {data.get('used_date', 'N/A')}")
            print()

    def create_code(self):
        print(f"\n{Fore.GREEN}✨ СОЗДАНИЕ НОВОГО ПОНТА{Style.RESET_ALL}\n")
        print(f"{Fore.CYAN}Доступные цвета ролей:{Style.RESET_ALL}")
        for plan in PLANS:
            if plan != 'FREE':
                print(f"{PLANS[plan]['color']}• {plan}{Style.RESET_ALL}")
        plan = input(f"\n{Fore.YELLOW}Роль: {Style.RESET_ALL}").upper()
        if plan not in PLANS or plan == 'FREE':
            print(f"{Fore.RED}Неверная роль!{Style.RESET_ALL}")
            return
        code = input(f"{Fore.YELLOW}Код (или Enter для генерации): {Style.RESET_ALL}")
        if not code:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        SECRET_CODES[code] = {
            'plan': plan,
            'used': False,
            'creator': 'superapps',
            'created': datetime.now().isoformat()
        }
        self.save_codes_status()
        print(f"{Fore.GREEN}✅ Код {code} для роли {plan} создан! (радуйтесь понту){Style.RESET_ALL}")

    def delete_code(self):
        code = input(f"{Fore.YELLOW}Код для удаления: {Style.RESET_ALL}").strip().upper()
        if code in SECRET_CODES:
            del SECRET_CODES[code]
            self.save_codes_status()
            print(f"{Fore.GREEN}✅ Код удален (понт пропал){Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Код не найден{Style.RESET_ALL}")

    def show_stats(self):
        total_codes = len(SECRET_CODES)
        used_codes = sum(1 for data in SECRET_CODES.values() if data['used'])
        free_codes = total_codes - used_codes
        searches = self.user_data.get('total_searches', 0)
        print(f"""
{Fore.CYAN}📊 СТАТИСТИКА (ВЫДУМАННАЯ):

{Fore.WHITE}Всего кодов: {total_codes} (просто цифры)
{Fore.GREEN}Использовано: {used_codes} (кто-то повелся)
{Fore.YELLOW}Свободно: {free_codes} (еще есть понты)
{Fore.CYAN}Твоя роль: {self.user_data['plan']} (красивый цвет)
{Fore.WHITE}Всего поисков: {searches} (ничего не значит)
{Fore.WHITE}Зарегистрирован: {self.user_data['registered']}
{Style.RESET_ALL}
""")

    def reset_search_counter(self):
        self.user_data['total_searches'] = 0
        self.save_user_data()
        print(f"{Fore.GREEN}✅ Счетчик поисков сброшен! (цифры обнулились){Style.RESET_ALL}")

    def give_plan(self):
        print(f"{Fore.CYAN}Доступные цвета ролей:{Style.RESET_ALL}")
        for plan in PLANS:
            print(f"{PLANS[plan]['color']}• {plan}{Style.RESET_ALL}")
        plan = input(f"\n{Fore.YELLOW}Роль: {Style.RESET_ALL}").upper()
        if plan in PLANS:
            self.activate_plan(plan)
            print(f"{Fore.GREEN}✅ Роль {plan} выдана! (теперь текст другого цвета){Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Неверная роль{Style.RESET_ALL}")

    def show_used_codes(self):
        print(f"\n{Fore.CYAN}🔐 ИСПОЛЬЗОВАННЫЕ КОДЫ (кто повелся на понты):{Style.RESET_ALL}\n")
        used = [(code, data) for code, data in SECRET_CODES.items() if data['used']]
        if not used:
            print(f"{Fore.YELLOW}Нет использованных кодов (все умные){Style.RESET_ALL}")
            return
        for code, data in used:
            color = PLANS[data['plan']]['color']
            print(f"{color}{code}{Style.RESET_ALL} - {data['plan']}")
            print(f"   Пользователь: {data.get('used_by', 'N/A')}")
            print(f"   Дата: {data.get('used_date', 'N/A')}")
            print()

    def main_menu(self):
        while True:
            os.system('clear')
            self.show_banner()
            print(f"""
{Fore.CYAN}╔══════════════════════════════════════════╗
║              ЧТО ДЕЛАЕМ?                ║
╠══════════════════════════════════════════╣
║{Fore.GREEN}  1. {Fore.WHITE}Поиск по нику (просто текст)         {Fore.CYAN}║
║{Fore.GREEN}  2. {Fore.WHITE}Telegram поиск (тоже текст)          {Fore.CYAN}║
║{Fore.GREEN}  3. {Fore.WHITE}GitHub поиск (и это текст)           {Fore.CYAN}║
║{Fore.GREEN}  4. {Fore.WHITE}Форумы (просто понты)                {Fore.CYAN}║
║{Fore.GREEN}  5. {Fore.WHITE}Master Scan (громкое название)       {Fore.CYAN}║
║{Fore.MAGENTA}  6. {Fore.WHITE}ПОЛУЧИТЬ РОЛЬ (ввести код)          {Fore.CYAN}║
║{Fore.RED}  7. {Fore.WHITE}АДМИНКА (для ADMIN)                  {Fore.CYAN}║
║{Fore.GREEN}  8. {Fore.WHITE}Статус (посмотреть цифры)            {Fore.CYAN}║
║{Fore.RED}  9. {Fore.WHITE}Выход                                 {Fore.CYAN}║
╚══════════════════════════════════════════╝{Style.RESET_ALL}
""")
            choice = input(f"{Fore.YELLOW}Выбери [1-9]: {Style.RESET_ALL}")

            if choice in ['1','2','3','4','5']:
                username = input(f"{Fore.YELLOW}Ник: {Style.RESET_ALL}")
                self.use_request()
                search_types = {
                    '1': 'Обычный поиск',
                    '2': 'Telegram поиск',
                    '3': 'GitHub поиск', 
                    '4': 'Поиск на форумах',
                    '5': 'MASTER SCAN'
                }
                searches = self.user_data.get('total_searches', 0)
                print(f"{Fore.GREEN}✅ {search_types[choice]} выполнен! (всего понтов: {searches}){Style.RESET_ALL}")
            elif choice == '6':
                code = input(f"{Fore.CYAN}🔐 ВВЕДИ КОД СЮДА (получи красивый цвет): {Style.RESET_ALL}")
                if code:
                    success, message = self.check_code(code)
                    print(message)
                    time.sleep(2)
            elif choice == '7':
                if self.user_data['plan'] == 'ADMIN':
                    if self.admin_login():
                        self.admin_panel()
                else:
                    print(f"{Fore.RED}❌ Только для ADMIN! (но это тоже понт){Style.RESET_ALL}")
                    time.sleep(2)
            elif choice == '8':
                searches = self.user_data.get('total_searches', 0)
                print(f"""
{Fore.CYAN}📊 ТВОЙ СТАТУС (НИЧЕГО НЕ ЗНАЧИТ):
    Роль: {PLANS[self.user_data['plan']]['color']}{self.user_data['plan']}{Style.RESET_ALL} (просто цвет)
    Всего поисков: {Fore.YELLOW}{searches}{Style.RESET_ALL} (просто цифра)
    Дата регистрации: {Fore.WHITE}{self.user_data['registered']}{Style.RESET_ALL}
{Style.RESET_ALL}
""")
                input(f"{Fore.YELLOW}Нажми Enter...{Style.RESET_ALL}")
            elif choice == '9':
                print(f"{Fore.GREEN}Пока! Заходи еще! (помни - это все понты){Style.RESET_ALL}")
                break
            time.sleep(1.5)

if __name__ == "__main__":
    app = PerxilittShop()
    try:
        app.main_menu()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Bye! (Ctrl+C тоже понт){Style.RESET_ALL}")
        sys.exit(0)ore.RED}Bye! (Ctrl+C тоже понт){Style.RESET_AL
