import pygame

pygame.init()
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Tetris')

vel = 5
width = 40
height = 60
posX = 0
posY = 500 - height
jump = 10
isJump = False

run = True

while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and posX > vel:
        posX -= vel

    if keys[pygame.K_RIGHT] and posX < 500 - vel - width:
        posX += vel

    if not isJump:
        if keys[pygame.K_UP] and posY > vel:
            posY -= vel

        if keys[pygame.K_DOWN] and posY < 500 - vel - height:
            posY += vel

        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        pass

    window.fill((0, 0, 0))
    pygame.draw.rect(window, (255, 0, 0), (posX, posY, width, height))
    pygame.display.update()

pygame.quit()
