import pygame, main

if __name__ == '__main__':
    if pygame.version.vernum < (2, 1, 3):
        print('[경고] Pygame 2.1.3.dev8 이상을 권장합니다.')
    main.main()