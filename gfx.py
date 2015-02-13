WHITE = (255,255,255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Gfx:
    """Helper class to easily print text and draw stuff"""

    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def print_msg(self, msg, topleft=None, topright=None, midtop=None, color=WHITE):
        msg_sf = self.font.render(msg, 0, color)
        rect = msg_sf.get_rect()
        if topleft is not None:
            rect.topleft = topleft
        elif topright is not None:
            rect.topright = topright
        elif midtop is not None:
            rect.midtop = midtop

        self.screen.blit(msg_sf, rect)

