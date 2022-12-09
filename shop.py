import global_object, pygame, global_var, status, wall

shop_item = {
    1: {
        'Name': '레벨 초기화',
        'Lore': '구매 시 레벨이 1, 경험치가 0으로 초기화됩니다.\nSP는 유지됩니다.',
        'Price': 100,
        'Max_Buy': -1,
        'Inc_Dim': 2,
        'Inc_Value': 10,
        'Func': status.obj.reset_level
        },
    2: {
        'Name': '벽에 금내기',
        'Lore': '벽의 체력이 크게 감소합니다.',
        'Price': 200,
        'Max_Buy': 19,
        'Inc_Dim': 3,
        'Inc_Value': (4, 1.03),
        'Func': wall.Wall.set_difficulty
        },
    3: {
        'Name': 'SP++;',
        'Lore': '레벨 상승 시 얻는 SP가 1 증가합니다.',
        'Price': 10000,
        'Max_Buy': -1,
        'Inc_Dim': 2,
        'Inc_Value': 5,
        'Func': lambda: None
        }
}

class ShopItem:

    def __init__(self, id, item_data):
        self.name = item_data['Name']
        self.lore = item_data['Lore']
        self.price = item_data['Price']
        self.id = id
        self.buy = 0
        self.money_icon = pygame.image.load('images/money_icon.png')
        try:
            self.icon = pygame.transform.scale(pygame.image.load(f'images/shop_icon/{self.id}.png'), (128, 128))
        except FileNotFoundError:
            self.icon = pygame.transform.scale(pygame.image.load('images/shop_icon/base.png'), (128, 128))
        self.font_small = global_var.font_small
        self.font_shop = global_var.font_shop
        self.font_shop.set_bold(True)
        self.font = global_var.font
        self.font_bold = global_var.font_bold
        self.max_buy = item_data['Max_Buy']
        self.inc_dim = item_data['Inc_Dim']
        self.inc_value = item_data['Inc_Value']
        self.surface = pygame.surface.Surface((180, 350), pygame.SRCALPHA)
        self.buy_button = global_object.Button((26, 26), 'invisible', self.buy_item, {'item_id':self.id}, size=128)

    def buy_item(self, item_id):
        if Shop.shop_obj is None: return
        if self.calc_price() <= status.money_obj.money and (self.max_buy == -1 or self.buy < self.max_buy):
            status.money_obj.set_money(status.money_obj.money - self.calc_price())
            self.buy += 1
            shop_item[item_id]['Func']()
            Shop.shop_obj.render_self()

    def render_self(self):
        self.surface.fill((220, 220, 220, 220))
        self.surface.blit(self.icon, (26, 26))
        self.surface.blit(self.font_bold.render(self.name, True, 'black'), (90 - self.font_bold.size(self.name)[0] / 2, 165))
        self.surface.blit(self.money_icon, (4, 310))
        price_text = global_var.conv_num(self.calc_price()) if (self.max_buy > self.buy or self.max_buy == -1) else 'MAX'
        self.surface.blit(self.font_shop.render(price_text, True, 'black'), (173 - self.font_shop.size(price_text)[0], 315))
        global_var.blit_text(self.surface, self.lore, (10, 200), self.font_small)
        return self.surface

    def calc_price(self):
        if self.inc_dim == 0:
            return self.price
        elif self.inc_dim == 1:
            return self.price + self.buy * self.inc_value
        elif self.inc_dim == 2:
            return int(self.price * (self.inc_value ** self.buy))
        elif self.inc_dim == 3:
            return int(self.price * (self.inc_value[0] ** self.buy) ** (self.inc_value[1] ** self.buy))
        else:
            raise ValueError

class Shop(global_object.Window):

    items = [ShopItem(key, value) for key, value in shop_item.items()]
    shop_obj = None

    def __init__(self):
        super().__init__((100, 100), (600, 400), name='상점 - 아이콘을 클릭해서 구매합니다.')
        if Shop.shop_obj is not None:
            Shop.shop_obj.close_window()
        Shop.shop_obj = self

    def close_window(self):
        super().close_window()
        Shop.shop_obj = None

    def render_self(self):
        super().render_self()
        x = 10
        for item in Shop.items:
            self.renders.append((item.render_self(), (self.pos[0]+x, self.pos[1]+40)))
            item.buy_button.rect.x, item.buy_button.rect.y = self.pos[0]+x+26, self.pos[1]+26
            x += 200