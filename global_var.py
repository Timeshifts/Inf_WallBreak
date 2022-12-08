import pygame
import numpy as np

pygame.init()

font = pygame.font.SysFont('나눔고딕' if '나눔고딕' in pygame.font.get_fonts() else None, 24)
font_small = pygame.font.SysFont('나눔고딕' if '나눔고딕' in pygame.font.get_fonts() else None, 18)
font_bold = pygame.font.SysFont('나눔고딕' if '나눔고딕' in pygame.font.get_fonts() else None, 24)
font_bold.set_bold(True)

def conv_num(number=0, threshold=8):
    if number < 10 ** threshold: return f'{number}'
    return np.format_float_scientific(number, precision=3)

# 참고 자료 7에서 가져와 단어 단위에서 글자 단위로 바꾼 함수입니다.
def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    letters = [list(word) for word in text.splitlines()]  # 2D array where each row is a list of letters.
    max_width, max_height = surface.get_size()
    x, y = pos
    letter_height = 0
    for line in letters:
        for letter in line:
            letter_surface = font.render(letter, True, color)
            letter_width, letter_height = letter_surface.get_size()
            if x + letter_width >= max_width:
                if letter == ' ': continue # 줄바꿈 다음의 공백 무시
                x = pos[0]  # Reset the x.
                y += letter_height  # Start on new row.
            surface.blit(letter_surface, (x, y))
            x += letter_width
        x = pos[0]  # Reset the x.
        y += letter_height  # Start on new row.