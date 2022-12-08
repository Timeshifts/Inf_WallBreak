import sys, time

if __name__ == '__main__':
    print('start.py를 실행해 주세요! (10초 뒤 자동으로 꺼집니다.)')
    time.sleep(10)
    sys.exit()

import pygame, random, save

import global_object
from global_object import Button
import status, global_var, wall, shop

class Character(pygame.sprite.Sprite):
    ACT = pygame.event.custom_type()

    def __init__(self, pos=(300, 200), size=(160, 116)):
        pygame.sprite.Sprite.__init__(self)
        self.state = 'run'
        self.size = size
        self.render = self.image = pygame.transform.scale(pygame.image.load('images/character/idle_0.png'), self.size)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.frame = 0
        pygame.time.set_timer(Character.ACT, 100)

    def next_image(self):
        try:
            self.render = self.image = pygame.transform.scale(pygame.image.load(f'images/character/{self.state}_{self.frame}.png'), self.size)
        except FileNotFoundError:
            self.frame = 0
            self.next_image()

EVENT_AUTOSAVE = pygame.event.custom_type()

def main():

    # 맨 위 초기 설정 부분은 0번 참고 자료를 기반으로 만들었습니다.
    pygame.init()

    size = width, height = 800, 600

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    pygame.display.set_caption('무한 벽 부수기')
    pygame.display.set_icon(pygame.image.load('images/money_icon.png'))

    done = False
    old_wall = None
    char_obj = Character((340, 470))
    save.load()
    background = pygame.transform.scale(pygame.image.load('images/background.png'), size)
    pygame.time.set_timer(EVENT_AUTOSAVE, 60000)
    shop_button = global_object.Button((width - 190, -2), 'shop', shop.Shop, None, (192, 64))

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                save.save()
                pygame.quit()
                sys.exit()

            #MouseEvent
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for window in global_object.Window.windows:
                        if window.drag_area.collidepoint(pygame.mouse.get_pos()):
                            window.is_dragging = True
                            window.offset = (event.pos[0]-window.pos[0], event.pos[1]-window.pos[1])
                            break
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for window in global_object.Window.windows:
                        window.is_dragging = False
                    for button in Button.button_events:
                        if button['rect'].collidepoint(pygame.mouse.get_pos()):
                            if button['args'] is not None: button['func'](**button['args'])
                            else: button['func']()
                            break
            elif event.type == pygame.MOUSEMOTION:
                for window in global_object.Window.windows:
                    if window.is_dragging:
                        window.pos = [event.pos[0] - window.offset[0], event.pos[1] - window.offset[1]]
                        if window.pos[0] < -1*window.size[0]+60: window.pos[0] = -1*window.size[0]+60
                        if window.pos[0] > width-30: window.pos[0] = width-30
                        if window.pos[1] < 0: window.pos[1] = 0
                        if window.pos[1] > height-30: window.pos[1] = height-30
                        window.render_self()

            #CustomEvent
            elif event.type == wall.Wall.EVENT_WALL_ARRIVED:
                char_obj.state = 'attack'
            elif event.type == Character.ACT:
                char_obj.frame += 1
                char_obj.next_image()
                if wall.wall_obj.damage(status.Stat.stat['BRK'] * random.randint(3, 10)):
                    old_wall = wall.wall_obj
                    wall.wall_obj = wall.Wall((800, 200))
                    char_obj.state = 'run'
            elif event.type == EVENT_AUTOSAVE:
                save.save()
                print('[정보] 자동 저장 완료')

        screen.blit(background, (0, 0))
        if old_wall is not None: old_wall.move_wall()
        wall.wall_obj.move_wall()
        if old_wall is not None:
            for render in old_wall.renders:
                screen.blit(render[0], render[1])
        for render in wall.wall_obj.renders:
            screen.blit(render[0], render[1])
        screen.blit(char_obj.render, char_obj.pos)
        screen.blit(shop_button.image, shop_button.rect)
        for render in status.money_obj.renders:
            screen.blit(render[0], render[1])
        for render in status.obj.renders:
            screen.blit(render[0], render[1])
        pygame.draw.rect(screen, (102, 37, 0), pygame.Rect(0, 570, width, 30))  # 땅
        screen.blit(global_var.font.render(f'{wall.Wall.count}번째 벽', True, 'black'),
                    ((width - global_var.font.size(f'{wall.Wall.count}번째 벽')[0]) / 2, 10))
        for window in global_object.Window.windows:
            for render in window.renders:
                screen.blit(render[0], render[1])
        pygame.display.flip()

        clock.tick(60)