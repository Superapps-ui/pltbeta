#!/data/data/com.termux/files/usr/bin/python3
# pltFull v2.0
# Author: superapps-ui
# Contact: @rne_ghosty

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

VERSION = "2.0"
PROGRAM_NAME = "pltFull"
CONTACT = "@rne_ghosty"

DISCLAIMER = f"""
{Fore.YELLOW}╔══════════════════════════════════════════════════════════╗
║{Fore.WHITE}  Используя данную программу вы соглашаетесь что она      {Fore.YELLOW}║
║{Fore.WHITE}  создана в развлекательных целях и не несет вреда        {Fore.YELLOW}║
╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""

BANNER = f"""
{Fore.CYAN}██████╗ ██╗  ████████╗███████╗██╗   ██╗██╗     ██╗
{Fore.BLUE}██╔══██╗██║  ╚══██╔══╝██╔════╝██║   ██║██║     ██║
{Fore.MAGENTA}██████╔╝██║     ██║   █████╗  ██║   ██║██║     ██║
{Fore.YELLOW}██╔═══╝ ██║     ██║   ██╔══╝  ██║   ██║██║     ██║
{Fore.GREEN}██║     ███████╗██║   ██║     ╚██████╔╝███████╗███████╗
{Fore.RED}╚═╝     ╚══════╝╚═╝   ╚═╝      ╚═════╝ ╚══════╝╚══════╝
{Style.RESET_ALL}
{Fore.WHITE}                    v{VERSION}{Style.RESET_ALL}
"""

ACCESS_LEVELS = {
    'FREE': {'level': 0, 'quota': 9, 'price': '0 ₽', 'color': Fore.GREEN},
    'VIP': {'level': 1, 'quota': 20, 'price': '5 ₽', 'color': Fore.CYAN},
    'AUTHED': {'level': 2, 'quota': 90, 'price': '10 ₽', 'color': Fore.BLUE},
    'UNLIMITED': {'level': 3, 'quota': 999999, 'price': '15 ₽', 'color': Fore.MAGENTA},
    'ADMIN': {'level': 9, 'quota': 999999, 'price': '70 ₽', 'color': Fore.RED}
}

ACCESS_CODES = {
    'V7XXA': {'level': 'VIP', 'used': False},
    'V7XXB': {'level': 'VIP', 'used': False},
    'V7XXC': {'level': 'VIP', 'used': False},
    'RE10BB': {'level': 'UNLIMITED', 'used': False},
    'RE10BC': {'level': 'UNLIMITED', 'used': False},
    'RE10BD': {'level': 'UNLIMITED', 'used': False},
    'Qertyy4cUw15': {'level': 'ADMIN', 'used': False},
    'Qertyy4cUw16': {'level': 'ADMIN', 'used': False},
    'Qertyy4cUw17': {'level': 'ADMIN', 'used': False},
}

ADMIN_CREDENTIALS = {
    'superapps': hashlib.sha256('ghosty2024!'.encode()).hexdigest()
}

class PltFull:
    def __init__(self):
        self.show_disclaimer()
        self.user_data = self.load_user_data()
        self.today = datetime.now().date().isoformat()
        self.load_codes()
        self.is_admin = False
        self.reset_quota()
    
    def show_disclaimer(self):
        os.system('clear')
        print(DISCLAIMER)
        input(f"{Fore.CYAN}Нажми Enter...{Style.RESET_ALL}")
        os.system('clear')
        print(BANNER)
        time.sleep(1)
    
    def load_user_data(self):
        if os.path.exists('pltfull_user.dat'):
            try:
                with open('pltfull_user.dat', 'rb') as f:
                    return pickle.load(f)
            except:
                return self.default_user()
        return self.default_user()
    
    def default_user(self):
        return {
            'level': 'FREE',
            'quota_used': 0,
            'last_reset': datetime.now().date().isoformat(),
            'used_codes': [],
            'total_searches': 0,
            'registered': datetime.now().isoformat()
        }
    
    def load_codes(self):
        if os.path.exists('pltfull_codes.dat'):
            try:
                with open('pltfull_codes.dat', 'rb') as f:
                    used = pickle.load(f)
                    for code in used:
                        if code in ACCESS_CODES:
                            ACCESS_CODES[code]['used'] = True
            except:
                pass
    
    def save_codes(self):
        used = [code for code, data in ACCESS_CODES.items() if data['used']]
        with open('pltfull_codes.dat', 'wb') as f:
            pickle.dump(used, f)
    
    def save_user(self):
        with open('pltfull_user.dat', 'wb') as f:
            pickle.dump(self.user_data, f)
    
    def reset_quota(self):
        if self.user_data['last_reset'] != self.today:
            self.user_data['quota_used'] = 0
            self.user_data['last_reset'] = self.today
            self.save_user()
    
    def get_quota_left(self):
        level = self.user_data['level']
        if level in ['UNLIMITED', 'ADMIN']:
            return '∞'
        max_q = ACCESS_LEVELS[level]['quota']
        left = max_q - self.user_data['quota_used']
        return max(0, left)
    
    def use_search(self):
        if self.user_data['level'] in ['UNLIMITED', 'ADMIN']:
            self.user_data['total_searches'] += 1
            self.save_user()
            return True
        
        max_q = ACCESS_LEVELS[self.user_data['level']]['quota']
        if self.user_data['quota_used'] < max_q:
            self.user_data['quota_used'] += 1
            self.user_data['total_searches'] += 1
            self.save_user()
            return True
        return False
    
    def activate_level(self, level):
        if level in ACCESS_LEVELS:
            self.user_data['level'] = level
            self.user_data['quota_used'] = 0
            self.save_user()
            return True
        return False
    
    def check_code(self, code):
        code = code.strip().upper()
        if code in ACCESS_CODES:
            if ACCESS_CODES[code]['used']:
                return False, f"{Fore.RED}❌ Код уже использован{Style.RESET_ALL}"
            
            level = ACCESS_CODES[code]['level']
            self.activate_level(level)
            ACCESS_CODES[code]['used'] = True
            self.user_data['used_codes'].append(code)
            self.save_user()
            self.save_codes()
            return True, f"{Fore.GREEN}✅ Уровень {level} активирован{Style.RESET_ALL}"
        
        return False, f"{Fore.RED}❌ Неверный код{Style.RESET_ALL}"
    
    def show_status(self):
        level = self.user_data['level']
        color = ACCESS_LEVELS[level]['color']
        quota = self.get_quota_left()
        
        print(f"""
{Fore.CYAN}╔══════════════════════════════════════════╗
║              ТВОЙ СТАТУС                ║
╠══════════════════════════════════════════╣
║  Уровень: {color}{level}{Style.RESET_ALL}
║  Осталось: {quota}/{ACCESS_LEVELS[level]['quota']}
║  Всего поисков: {self.user_data['total_searches']}
║  Дата регистрации: {self.user_data['registered'][:10]}
╚══════════════════════════════════════════╝{Style.RESET_ALL}
""")
    
    def show_menu(self):
        print(f"""
{Fore.CYAN}╔══════════════════════════════════════════╗
║              ГЛАВНОЕ МЕНЮ                ║
╠══════════════════════════════════════════╣
║{Fore.GREEN}  1. {Fore.WHITE}Базовый поиск                    {Fore.CYAN}║
║{Fore.CYAN}  2. {Fore.WHITE}Telegram                          {Fore.CYAN}║
║{Fore.BLUE}  3. {Fore.WHITE}GitHub                            {Fore.CYAN}║
║{Fore.MAGENTA}  4. {Fore.WHITE}Форумы                            {Fore.CYAN}║
║{Fore.RED}  5. {Fore.WHITE}Master Scan                       {Fore.CYAN}║
║{Fore.YELLOW}  6. {Fore.WHITE}Ввести код                        {Fore.CYAN}║
║{Fore.RED}  7. {Fore.WHITE}Админка                           {Fore.CYAN}║
║{Fore.CYAN}  8. {Fore.WHITE}Статус                             {Fore.CYAN}║
║{Fore.RED}  9. {Fore.WHITE}Выход                              {Fore.CYAN}║
╚══════════════════════════════════════════╝{Style.RESET_ALL}
""")
    
    def search(self, search_type, username):
        print(f"\n{Fore.GREEN}🔍 Ищу: {username}{Style.RESET_ALL}")
        
        if search_type == '1':
            print(f"{Fore.WHITE}Google: https://www.google.com/search?q={username}{Style.RESET_ALL}")
        elif search_type == '2':
            print(f"{Fore.CYAN}Telegram: https://t.me/{username}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Telegram channel: https://t.me/s/{username}{Style.RESET_ALL}")
        elif search_type == '3':
            print(f"{Fore.BLUE}GitHub: https://github.com/{username}{Style.RESET_ALL}")
        elif search_type == '4':
            print(f"{Fore.MAGENTA}Reddit: https://reddit.com/user/{username}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}Habr: https://habr.com/users/{username}{Style.RESET_ALL}")
        elif search_type == '5':
            print(f"{Fore.RED}Telegram: https://t.me/{username}{Style.RESET_ALL}")
            print(f"{Fore.RED}GitHub: https://github.com/{username}{Style.RESET_ALL}")
            print(f"{Fore.RED}Reddit: https://reddit.com/user/{username}{Style.RESET_ALL}")
            print(f"{Fore.RED}Google: https://www.google.com/search?q={username}{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Готово!{Style.RESET_ALL}")
    
    def admin_login(self):
        print(f"\n{Fore.RED}🔐 Вход в админку{Style.RESET_ALL}")
        login = input(f"{Fore.YELLOW}Логин: {Style.RESET_ALL}")
        pwd = input(f"{Fore.YELLOW}Пароль: {Style.RESET_ALL}")
        
        if login in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[login] == hashlib.sha256(pwd.encode()).hexdigest():
            self.is_admin = True
            return True
        return False
    
    def admin_panel(self):
        if not self.is_admin:
            print(f"{Fore.RED}Доступ запрещен{Style.RESET_ALL}")
            return
        
        while True:
            os.system('clear')
            print(f"""
{Fore.RED}╔══════════════════════════════════════════╗
║              АДМИН ПАНЕЛЬ               ║
╠══════════════════════════════════════════╣
║{Fore.WHITE}  1. Все коды                          {Fore.RED}║
║{Fore.WHITE}  2. Создать код                       {Fore.RED}║
║{Fore.WHITE}  3. Статистика                        {Fore.RED}║
║{Fore.WHITE}  4. Сбросить лимиты                   {Fore.RED}║
║{Fore.WHITE}  5. Выдать уровень                    {Fore.RED}║
║{Fore.WHITE}  6. Выход                             {Fore.RED}║
╚══════════════════════════════════════════╝{Style.RESET_ALL}
""")
            choice = input(f"{Fore.RED}admin> {Style.RESET_ALL}")
            
            if choice == '1':
                for code, data in ACCESS_CODES.items():
                    status = "✅" if data['used'] else "❌"
                    print(f"{ACCESS_LEVELS[data['level']]['color']}{code}{Style.RESET_ALL} - {data['level']} {status}")
            
            elif choice == '2':
                lvl = input(f"{Fore.YELLOW}Уровень (VIP/AUTHED/UNLIMITED/ADMIN): {Style.RESET_ALL}").upper()
                if lvl in ACCESS_LEVELS and lvl != 'FREE':
                    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                    ACCESS_CODES[code] = {'level': lvl, 'used': False}
                    self.save_codes()
                    print(f"{Fore.GREEN}Код {code} создан{Style.RESET_ALL}")
            
            elif choice == '3':
                total = len(ACCESS_CODES)
                used = sum(1 for d in ACCESS_CODES.values() if d['used'])
                print(f"Всего кодов: {total}")
                print(f"Использовано: {used}")
                print(f"Свободно: {total - used}")
                print(f"Твои поиски: {self.user_data['total_searches']}")
            
            elif choice == '4':
                self.user_data['quota_used'] = 0
                self.save_user()
                print(f"{Fore.GREEN}Лимиты сброшены{Style.RESET_ALL}")
            
            elif choice == '5':
                lvl = input(f"{Fore.YELLOW}Уровень: {Style.RESET_ALL}").upper()
                if lvl in ACCESS_LEVELS:
                    self.activate_level(lvl)
                    print(f"{Fore.GREEN}Уровень {lvl} выдан{Style.RESET_ALL}")
            
            elif choice == '6':
                self.is_admin = False
                break
            
            input(f"\n{Fore.YELLOW}Enter...{Style.RESET_ALL}")
    
    def run(self):
        while True:
            os.system('clear')
            print(BANNER)
            self.show_menu()
            
            choice = input(f"{Fore.YELLOW}Выбери [1-9]: {Style.RESET_ALL}")
            
            if choice in ['1','2','3','4','5']:
                if not self.use_search():
                    print(f"{Fore.RED}❌ Лимит на сегодня исчерпан!{Style.RESET_ALL}")
                    time.sleep(1.5)
                    continue
                
                username = input(f"{Fore.YELLOW}Ник: {Style.RESET_ALL}")
                self.search(choice, username)
                
            elif choice == '6':
                code = input(f"{Fore.CYAN}Введи код: {Style.RESET_ALL}")
                if code:
                    success, msg = self.check_code(code)
                    print(msg)
                    time.sleep(1.5)
            
            elif choice == '7':
                if self.user_data['level'] == 'ADMIN':
                    if self.admin_login():
                        self.admin_panel()
                else:
                    print(f"{Fore.RED}❌ Только для ADMIN{Style.RESET_ALL}")
                    time.sleep(1.5)
            
            elif choice == '8':
                self.show_status()
                input(f"{Fore.YELLOW}Enter...{Style.RESET_ALL}")
            
            elif choice == '9':
                print(f"{Fore.GREEN}Пока!{Style.RESET_ALL}")
                break
            
            if choice in ['1','2','3','4','5']:
                input(f"{Fore.YELLOW}Enter...{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        app = PltFull()
        app.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Пока!{Style.RESET_ALL}")
        sys.exit(0)
