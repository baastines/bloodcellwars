from pip import main
import pygame

from models import TKillerCell, Virus
from utils import load_sprite, get_random_position, print_text

class BloodCellWars:

    MIN_VIRUS_DISTANCE = 300
  
    def __init__(self):

        self._init_pygame()
        self.font = pygame.font.Font("bloodcellwars/assets/fonts/reglisse.ttf", 96)
        self.message = ""
        self.screen = pygame.display.set_mode((1280, 720))
        self.background = load_sprite("vessel", False)
        self.clock = pygame.time.Clock()
        self.viruses = []
        self.bullets = []
        self.whitecell = TKillerCell((640, 360), self.bullets.append)

        for _ in range(10):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.whitecell.position)
                    > self.MIN_VIRUS_DISTANCE
                ):
                    break

            self.viruses.append(Virus(position, self.viruses.append))
        
    def main_loop(self):

        while True:

            self._handle_input()

            self._process_game_logic()

            self._draw()

    def _init_pygame(self):

        pygame.init()

        pygame.display.set_caption("Blood Cell Wars")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            if self.whitecell == None and (
                event.type == pygame.KEYDOWN and event.key == pygame.K_r):
                
                main()
            
            if (
            self.whitecell
            and event.type == pygame.MOUSEBUTTONDOWN
            ):
                self.whitecell.shoot()
                
        is_key_pressed = pygame.key.get_pressed()

        if self.whitecell:

            if is_key_pressed[pygame.K_1]:
                self.whitecell.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_3]:
                self.whitecell.rotate(clockwise=False)
            if is_key_pressed[pygame.K_w]:
                self.whitecell.accelerate()
            if is_key_pressed[pygame.K_s]:
                self.whitecell.deaccelerate()
            if is_key_pressed[pygame.K_a]:
                self.whitecell.accelerateleftward()
            if is_key_pressed[pygame.K_d]:
                self.whitecell.acceleraterightward()

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.whitecell:
            for virus in self.viruses:
                if virus.collides_with(self.whitecell):
                    self.whitecell = None
                    self.message = "You lose!"
                    break
        if not self.viruses and self.whitecell:
            self.message = "You win!"

        for bullet in self.bullets[:]:
            for virus in self.viruses[:]:
                if virus.collides_with(bullet):
                    self.viruses.remove(virus)
                    self.bullets.remove(bullet)
                    virus.split()
                    break

        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

    def _get_game_objects(self):
        game_objects = [*self.bullets, *self.viruses]

        if self.whitecell:
            game_objects.append(self.whitecell)
        
        return game_objects

    def _draw(self):

        self.screen.blit(self.background, (0, 0))

        if self.message:
            print_text(self.screen, self.message, self.font)

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        mouse_pos = pygame.mouse.get_pos()
        #print(mouse_pos)
        pygame.display.flip()
        self.clock.tick(20)