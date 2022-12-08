import global_var, pygame
from global_object import Button

class Stat:
    # 순서대로 파괴력, 이동력, 수집력, 관찰력, 적응력
    stat = {'BRK': 1, 'SPD': 1, 'CLT': 1, 'OBS': 1, 'ADP': 1 }
    exp = 0
    level = 1
    max = level ** 2 + 7 * level + 15
    SP = 1

    def __init__(self):
        self.renders = None
        self.font = global_var.font
        self.renew_text()
        self.render_self()
        self.text = ''

    def renew_text(self):
        self.text = (f'파괴력: {Stat.stat["BRK"]}',
            f'이동력: {Stat.stat["SPD"]}',
            f'수집력: {Stat.stat["CLT"]}',
            f'관찰력: {Stat.stat["OBS"]}',
            f'적응력: {Stat.stat["ADP"]}',
            '',
            f'레벨: {Stat.level} ({Stat.exp/Stat.max*100:.2f}%)',
            f'남은 SP: {Stat.SP}')

    # sum 1tok n^2+7n+15 = k^3/3+4k^2+56k/3
    @staticmethod
    def sum_exp(level=1):
        return 1/3 * level ** 3 + 4 * level ** 2 + 56/3 * level

    # 레벨 하나마다 필요 경험치를 계산하면 경험치 10^20 즈음에서 게임이 멈춰버립니다.
    # 경험치가 충분히 많은 경우에, 한번에 2^n 레벨이 증가하도록 하였습니다.
    def levelup(self, render=True):
        count = 0
        total_xp = 0
        check_lvl = 1
        while Stat.exp >= total_xp:
            total_xp = self.sum_exp(Stat.level + check_lvl) - self.sum_exp(Stat.level - 1)
            check_lvl *= 2
        import shop
        while check_lvl >= 1:
            total_xp = self.sum_exp(Stat.level + check_lvl - 1) - self.sum_exp(Stat.level - 1)
            if Stat.exp >= total_xp:
                Stat.exp -= self.sum_exp(Stat.level + check_lvl -1) - self.sum_exp(Stat.level-1)
                Stat.level += check_lvl
                Stat.SP += check_lvl + shop.Shop.items[2].buy
                count += check_lvl
                Stat.max = Stat.level ** 2 + 7 * Stat.level + 15
            check_lvl //= 2
        if render:
            self.renew_text()
            self.render_self()

    def reset_level(self):
        Stat.level = 1
        self.add_exp(-1*self.exp)

    def add_exp(self, amount):
        Stat.exp += amount
        if Stat.exp >= Stat.max:
            self.levelup(False)
        self.renew_text()
        self.render_self()

    def buy_stat(self, stat):
        amount = min(Stat.stat['ADP'], Stat.SP)
        Stat.SP -= amount
        self.set_stat(stat, Stat.stat[stat]+amount)

    def set_stat(self, stat, amount):
        Stat.stat[stat] = amount
        self.renew_text()
        self.render_self()

    def render_self(self):
        y = 0
        self.renders = []
        for text in self.text:
            y += 30
            self.renders.append((self.font.render(text, True, 'black'), (40, y)))
        y = 0
        for stat, amount in self.stat.items():
            y += 30
            button = Button((10, y), 'plus', self.buy_stat, {'stat': stat})
            self.renders.append((button.image, button.rect))

obj = Stat()

class Money:
    money = 0
    font = global_var.font

    def __init__(self):
        self.text = '0'
        self.renders = []
        self.image = pygame.image.load('images/money_icon.png')
        self.render_self()

    def render_self(self):
        self.renders = []
        self.text = f'{Money.money}'
        self.renders.append((Money.font.render(self.text, True, 'black'), (40, 2)))
        self.renders.append((self.image, (7, 0)))

    def set_money(self, amount):
        Money.money = amount
        Money.text = f'{Money.money}'
        self.render_self()

money_obj = Money()