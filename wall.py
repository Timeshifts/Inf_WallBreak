import global_var, pygame, math

from global_object import Bar
import status

class WallArrow(pygame.sprite.Sprite):

    def __init__(self, pos=(250, 300)):
        pygame.sprite.Sprite.__init__(self)
        self.value = 0
        self.max_value = 1
        self.pos = pos
        self.font = global_var.font_bold
        self.image = pygame.image.load('images/wall_arrow.png')
        self.image = pygame.transform.scale(self.image, (240, 120))
        self.image_line = pygame.image.load('images/wall_arrow_line.png')
        self.image_line = pygame.transform.scale(self.image_line, (240, 120))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.renders = []
        self.render_self()

    def render_self(self, value=None, max_value=None):
        if value is not None: self.value = value
        if max_value is not None: self.max_value = max_value
        self.renders = []
        (self.rect.x, self.rect.y) = self.pos
        self.renders.append((self.image, self.rect))
        surface = pygame.Surface((240, 120), flags=pygame.SRCALPHA)
        surface.fill((0, 255, 0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        mask = pygame.mask.Mask((max(0, 26+194*(1-self.value/self.max_value)), 120), fill=True)
        self.mask.erase(mask, (0, 0))
        self.mask.to_surface(surface, setcolor=(255, 255, 255), unsetcolor=None)
        self.renders.append((surface, self.rect))
        self.renders.append((self.image_line, self.rect))
        self.renders.append((self.font.render(f'{global_var.conv_num(self.value)} M', True, 'black'),
        (self.pos[0] + 120 - self.font.size(f'{global_var.conv_num(self.value)} M')[0] / 2,
         self.pos[1] + 50)))

class Wall(pygame.sprite.Sprite):
    count = 0
    EVENT_WALL_ARRIVED = pygame.event.custom_type()
    WALL_BASE_DIFF = 120
    wall_difficulty = WALL_BASE_DIFF

    def __init__(self, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        Wall.count += 1
        self.moving = True
        self.pos = list(pos)
        self.image = self.rect = None
        self.wall_state = 0
        self.wall_image = -1
        self.hp = self.base_hp = self.max_hp = 100
        self.hp_bar = Bar(self.hp, self.max_hp, (self.pos[0], self.pos[1]-60))
        self.wall_arrow = WallArrow()
        self.font = global_var.font_bold
        self.renders = []
        self.render_self()
        self.scale_wall(False)

    @staticmethod
    def set_difficulty():
        import shop
        Wall.wall_difficulty = Wall.WALL_BASE_DIFF - shop.Shop.items[1].buy/2
        wall_obj.scale_wall()

    def scale_wall(self, stay=True):
        self.base_hp = int(100 * (Wall.WALL_BASE_DIFF / 100) ** Wall.count)
        self.hp = int(100 * (Wall.wall_difficulty / 100) ** Wall.count)
        self.max_hp = self.hp
        if not stay: self.pos[0] += math.log(int(100 * 1.2 ** Wall.count)) * 100
        self.hp_bar = Bar(self.hp, self.max_hp, (self.pos[0], self.pos[1] - 60))
        if not stay: self.wall_arrow.render_self(int((self.pos[0] - 400) / 50), int((self.pos[0] - 400) / 50))

    def render_self(self):
        self.renders = []
        self.wall_state = min(5, int((self.max_hp-self.hp)/self.max_hp*6))
        if self.wall_state != self.wall_image:
            try:
                self.image = pygame.image.load(f'images/wall_{self.wall_state}.png')
            except FileNotFoundError:
                self.image = pygame.image.load(f'images/wall_0.png')
            self.image = pygame.transform.scale(self.image, (192, 384))
            self.wall_image = self.wall_state
        self.rect = self.image.get_rect()
        (self.rect.x, self.rect.y) = self.pos
        self.renders.append((self.image, self.rect))
        self.renders.append(self.hp_bar.render_self(self.hp, self.max_hp, (self.pos[0], self.pos[1]-60)))
        self.renders.append((self.font.render(global_var.conv_num(self.hp), True, 'black'),
                             (self.pos[0] + 90 - self.font.size(global_var.conv_num(self.hp))[0] / 2, self.pos[1] - 57.5)))
        self.wall_arrow.render_self(int((self.pos[0]-400)/50))
        if self.pos[0] > 400:
            for render in self.wall_arrow.renders: self.renders.append(render)

    # Return: 벽이 이 피해로 부서졌는가?
    def damage(self, damage=1.0):
        if self.moving: return
        if self.hp <= 0: return
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.render_self()
            return self.break_wall()
        else:
            self.render_self()
            return False

    def move_wall(self):
        if not self.moving: return
        self.pos[0] -= (math.log(status.Stat.stat['SPD'], 10) + 1) * 7
        if self.pos[0] < 400 and self.hp > 0:
            self.pos[0] = 400
            self.moving = False
            pygame.event.post(pygame.event.Event(Wall.EVENT_WALL_ARRIVED))
        self.render_self()

    def break_wall(self):
        status.money_obj.set_money(status.Money.money + int(math.log(self.base_hp, 2) * status.Stat.stat['CLT']))
        status.obj.add_exp(self.base_hp * status.Stat.stat['OBS'])
        self.moving = True
        return True

wall_obj = Wall((600, 200))