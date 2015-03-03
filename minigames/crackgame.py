import minigame
import pygame
import input_map
import random


class CrackGame(minigame.Minigame):
    game_type = minigame.MULTIPLAYER
    name = 'Jump over the cracks'
    IMAGES = []
    for i in range(3):
        IMAGES.append(pygame.image.load('./res/img/crackgame/run'+str(i)+'.png'))
    JUMP_IMAGE = pygame.image.load('./res/img/crackgame/jump.png')
    DEAD_IMAGE = pygame.image.load('./res/img/crackgame/dead.png')

    CRACK_PATTERNS = [
        [[150, 150, 150, 150, 150], [300, 150, 300, 150]],  # Difficulty 0
        [[], []],  # Difficulty 1
        [[], []],  # Difficulty 2
        [[], []],  # Difficulty 3
        [[], []]  # Difficulty >4
    ]

    def __init__(self, game):
        minigame.Minigame.__init__(self, game)
        if self.difficulty > 4:
            self.difficulty = 4
        self.max_duration = 6000 - self.difficulty*1000
        self.width, self.height = self.screen.get_size()
        self.cracks = random.choice(CrackGame.CRACK_PATTERNS[self.difficulty])
        self.sidewalk_height = 100
        self.sidewalk_y = 200
        self.current_frame = 0
        self.positions = [[50, self.sidewalk_y+self.sidewalk_height/2], [50, self.sidewalk_y+self.sidewalk_height/2 + 2*self.sidewalk_height]]
        self.animation_counter = 0
        self.animation = 50
        self.jumps = [0, 0]
        self.dead = [False, False]
        for i in range(3):
            CrackGame.IMAGES[i] = CrackGame.IMAGES[i].convert_alpha()
        CrackGame.JUMP_IMAGE = CrackGame.JUMP_IMAGE.convert_alpha()
        CrackGame.DEAD_IMAGE = CrackGame.DEAD_IMAGE.convert_alpha()

    def tick(self):
        self.update()
        self.draw()

    def get_results(self):
        return [not self.dead[0], not self.dead[1]]

    def draw(self):
        self.screen.fill((0, 100, 0))
        pygame.draw.rect(self.screen, (135, 206, 235), pygame.Rect(0, 0, self.width, 100))
        for i in range(2):
            if self.dead[i]:
                img = CrackGame.DEAD_IMAGE
            elif self.jumps[i] == 0:
                img = CrackGame.IMAGES[self.current_frame]
            else:
                img = CrackGame.JUMP_IMAGE

            pygame.draw.rect(self.screen, (200, 200, 200), pygame.Rect(0, self.sidewalk_y + i*2*self.sidewalk_height, self.width, self.sidewalk_height))
            pygame.draw.rect(self.screen, (150, 150, 150), pygame.Rect(0, self.sidewalk_y+self.sidewalk_height + i*2*self.sidewalk_height, self.width, self.sidewalk_height/5))
            p = 0
            for crack in self.cracks:
                pygame.draw.aaline(self.screen, (0, 0, 0), (p + crack - 10, self.sidewalk_y+self.sidewalk_height + i*2*self.sidewalk_height), (p + crack + 10, self.sidewalk_y + i*2*self.sidewalk_height))
                pygame.draw.aaline(self.screen, (0, 0, 0), (p + crack - 10, self.sidewalk_y+self.sidewalk_height + i*2*self.sidewalk_height), (p + crack - 10, self.sidewalk_y+self.sidewalk_height + i*2*self.sidewalk_height + self.sidewalk_height/5))
                p += crack
                if self.jumps[i] == 0:
                    if self.positions[i][0] - img.get_rect().width/4 < p < self.positions[i][0] + img.get_rect().width/4:
                        self.dead[i] = True

            if not self.dead[i]:
                width = img.get_rect().width - ((self.sidewalk_y+self.sidewalk_height/2 + 2*i*self.sidewalk_height - self.positions[i][1]) / 8)
                pygame.draw.ellipse(self.screen, (180, 180, 180), pygame.Rect(self.positions[i][0] - img.get_rect().width/2, self.sidewalk_y + i*2*self.sidewalk_height + 60, width, 20))
            self.screen.blit(img, pygame.Rect(self.positions[i][0] - img.get_rect().width/2, self.positions[i][1] - 0.75*img.get_rect().height, img.get_rect().width, img.get_rect().height))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                for i in range(2):
                    if event.key == input_map.PLAYERS_MAPPING[i][input_map.ACTION]:
                        if self.jumps[i] == 0:
                            self.jumps[i] = -1

        for i in range(2):
            if not self.dead[i]:
                self.positions[i][0] += 2*float(self.width)/self.max_duration
                self.positions[i][1] += self.jumps[i]
                if self.jumps[i] == 0:
                    self.jumps[i] = 0.05 + 0.05-self.max_duration * 1e-05
                else:
                    self.jumps[i] += 0.005 + 0.005 - self.max_duration * 1e-06

                if self.positions[i][1] >= self.sidewalk_y+self.sidewalk_height/2 + 2*i*self.sidewalk_height and self.jumps[i] >= 0:
                    self.jumps[i] = 0
                    self.positions[i][1] = self.sidewalk_y+self.sidewalk_height/2 + 2*i*self.sidewalk_height

        self.animation_counter += 1
        if self.animation_counter >= self.animation:
            self.current_frame += 1
            if self.current_frame == len(CrackGame.IMAGES):
                self.current_frame = 0
            self.animation_counter = 0