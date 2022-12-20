import pygame, math
import numpy as np

pygame.init()

font = pygame.font.SysFont('나눔고딕' if '나눔고딕' in pygame.font.get_fonts() else None, 24)
font_small = pygame.font.SysFont('나눔고딕' if '나눔고딕' in pygame.font.get_fonts() else None, 18)
font_shop = pygame.font.SysFont('나눔고딕' if '나눔고딕' in pygame.font.get_fonts() else None, 20)
font_bold = pygame.font.SysFont('나눔고딕' if '나눔고딕' in pygame.font.get_fonts() else None, 24)
font_bold.set_bold(True)

# 항하사(10^52)부터는 여러 글자이므로 지수로 표기
number_word = ['', '만', '억', '조', '경', '해', '자', '양', '구', '간', '정', '재', '극']
def conv_num(number=0, threshold=52):
    if number < 10 ** 4:
        return f'{number}'
    elif number < 10 ** threshold:
        power = int(math.log10(number) / 4)
        word = number_word[power], number_word[power-1]
        big_number = int(number / 10 ** (power*4))
        small_number = int((number - big_number * 10 ** (power*4)) / 10 ** (power*4-4))
        return f'{big_number}{word[0]} {small_number}{word[1]}' if small_number >= 1 else f'{big_number}{word[0]}'
    return np.format_float_scientific(number, precision=3)

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