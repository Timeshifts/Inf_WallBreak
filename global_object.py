import pygame, global_var

class Button(pygame.sprite.Sprite):

    button_events = []

    def __init__(self, pos=(0, 0), button_type='plus', click_func=None, click_args=None, size=25):
        pygame.sprite.Sprite.__init__(self)
        self.click_func = click_func
        self.click_args = click_args
        try:
            self.image = pygame.image.load(f'images/button/button_{button_type}.png')
        except FileNotFoundError:
            self.image = pygame.image.load(f'images/button/button_base.png')
        self.image = pygame.transform.scale(self.image, (size, size) if type(size) is int else size)
        self.rect = self.image.get_rect()
        (self.rect.x, self.rect.y) = pos
        Button.button_events.append({'rect':self.rect, 'func':self.click_func, 'args':self.click_args})

class Bar(pygame.sprite.Sprite):

    def __init__(self, value=0, max_value=0, pos=(0, 0), color=pygame.Color(0, 148, 220), size=(180, 30)):
        pygame.sprite.Sprite.__init__(self)
        self.value = value
        self.max_value = max_value
        self.pos = pos
        self.color = color
        self.surface = pygame.Surface((180, 30))
        self.surface.fill((255, 255, 255))
        self.size = size
        self.render_self()

    def render_self(self, value=None, max_value=None, pos=None):
        if value is not None: self.value = value
        if max_value is not None: self.max_value = max_value
        if pos is None: pos = self.pos
        pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(0, 0, self.size[0], self.size[1]))
        if self.value >= 0: pygame.draw.rect(self.surface, self.color, pygame.Rect(0, 0, self.size[0]*self.value/self.max_value, self.size[1]))
        pygame.draw.line(self.surface, (0, 0, 0), (0, 0), (self.size[0], 0))
        pygame.draw.line(self.surface, (0, 0, 0), (0, 0), (0, self.size[1]))
        pygame.draw.line(self.surface, (0, 0, 0), (0, 29), (self.size[0], self.size[1]-1))
        pygame.draw.line(self.surface, (0, 0, 0), (179, 0), (self.size[0]-1, self.size[1]))
        return self.surface, pos

class Window(pygame.sprite.Sprite):

    windows = []

    def __init__(self, pos=(0, 0), size=(600, 400), color=(0, 0, 255, 64), name='창'):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.size = size
        self.color = color
        self.name = name
        self.font = global_var.font_bold
        self.surface = pygame.Surface(self.size, flags=pygame.SRCALPHA)
        self.surface.fill(self.color)
        self.is_dragging = False
        self.offset = None
        self.drag_area = pygame.rect.Rect(pos[0], pos[1], size[0]-30, 30)
        pygame.draw.rect(self.surface, (32, 32, 32), (0, 0, size[0], 30))
        self.close_button = Button((self.pos[0]+self.size[0]-30, self.pos[1]), 'close', self.close_window, size=30)
        self.renders = []
        Window.windows.append(self)
        self.render_self()

    def close_window(self):
        Button.button_events.remove({'rect':self.close_button.rect, 'func':self.close_button.click_func, 'args':self.close_button.click_args})
        Window.windows.remove(self)

    def render_self(self):
        self.renders = []
        self.renders.append((self.surface, self.pos))
        (self.close_button.rect.x, self.close_button.rect.y) = (self.pos[0]+self.size[0]-30, self.pos[1])
        self.renders.append((self.close_button.image, self.close_button.rect))
        self.renders.append((self.font.render(self.name, True, 'white'), (self.pos[0]+2.5, self.pos[1]+2.5)))
        self.drag_area = pygame.rect.Rect(self.pos[0], self.pos[1], self.size[0] - 30, 30)