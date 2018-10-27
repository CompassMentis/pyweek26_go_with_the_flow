import pygame


class DrawText:
    myfont = None

    def draw(self, screen, x, y, text, colour=(0, 0, 0)):
        # Need to initialise pygame first, so use lazy-initialisation
        if self.myfont is None:
            self.myfont = pygame.font.SysFont('monospace', 20, bold=True)

        label = self.myfont.render(text, 1, colour)
        screen.blit(label, (x, y))


draw_text = DrawText()
