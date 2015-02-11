import splash

class Menu:
    '''
    Display the initial menu waiting for play to get ready
    and pick universities.
    '''
    def __init__(self, game):
        self.game = game

    def run(self):
        # Show game menu
        # Perhaps something that await two player input
        # while display "Insert coins..."
        print('Insert [c]oins...')
        i = raw_input()

        if i == 'c':
            self.start_game()

    def start_game(self):
        self.game.state = splash.Splash(self.game)

