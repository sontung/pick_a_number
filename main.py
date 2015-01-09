import random
import pygame
import sys
import sound
from pygame.locals import *
from sound.background_sound import music_funcs as music


class GameGUI:
    def __init__(self, _game_logic, _game_state):
        pygame.init()
        self.state = _game_state
        self.logic = _game_logic
        self.fps_clock = pygame.time.Clock()
        self.window_width = 1180
        self.window_height = 700
        self.font_size = 30
        self.x_margin = 78
        self.y_margin = 150
        self.colors = {"white": (255, 255, 255),
                       "navy": (0, 0, 128),
                       "red": (139, 0, 0),
                       "blue": (0, 0, 255),
                       "dark": (3, 54, 73),
                       "green": (0, 128, 0),
                       "light green": (118, 238, 0),
                       "turquoise": (0, 229, 238)}
        self.tile_color_for_numbers = self.colors["light green"]
        self.text_color = self.colors["navy"]
        self.bg_color = self.colors["turquoise"]
        self.tile_color = self.bg_color
        self.display_surface = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Pick A Number')
        self.font = pygame.font.Font('GatsbyFLF-Bold.ttf', self.font_size)
        self.pos = (self.window_width/2, self.window_height/2) # for configuring game difficulty

    def make_text(self, text, color, bg_color, center):
        """
        Make a text object for drawing
        """
        textSurf = self.font.render(text, True, color, bg_color)
        textRect = textSurf.get_rect()
        textRect.center = center
        return (textSurf, textRect)

    def draw_tile(self, number, index):
        """
        Draw the number tiles
        """
        size = 40
        space = 1
        position = (self.x_margin+(size+space)*index, self.y_margin*2)
        self.logic.update_fl()
        print self.logic.first_last
        if index in self.logic.first_last:
            pygame.draw.rect(self.display_surface, self.colors["green"], (position[0], position[1], size, size))
        else:
            pygame.draw.rect(self.display_surface, self.tile_color_for_numbers, (position[0], position[1], size, size))
        text_sur = self.font.render(str(number), True, self.text_color)
        text_rect = text_sur.get_rect()
        text_rect.center = (position[0]+size/2, position[1]+size/2)
        self.display_surface.blit(text_sur, text_rect)

    def configure_difficulty(self, pos):
        """
        Changing position of the circle indicating new difficulty
        """
        self.pos = pos

    def draw(self, state):
        """
        Draw the scene
        """
        self.display_surface.fill(self.bg_color)
        if state == "welcome":
            self.setting_sur, self.setting_rect = self.make_text('Settings', self.text_color, self.tile_color,
                                                                 (self.window_width/2, self.window_height/2))
            self.new_sur, self.new_rect = self.make_text('New Game', self.text_color, self.tile_color,
                                                         (self.window_width/2, self.window_height/2-60))
            self.quit_sur, self.quit_rect = self.make_text('Quit', self.text_color, self.tile_color,
                                                           (self.window_width/2, self.window_height/2+180))
            self.help_sur, self.help_rect = self.make_text('How to play', self.text_color, self.tile_color,
                                                           (self.window_width/2, self.window_height/2+60))
            self.author_sur, self.author_rect = self.make_text('About the author', self.text_color, self.tile_color,
                                                               (self.window_width/2, self.window_height/2+120))
            self.display_surface.blit(self.setting_sur, self.setting_rect)
            self.display_surface.blit(self.new_sur, self.new_rect)
            self.display_surface.blit(self.quit_sur, self.quit_rect)
            self.display_surface.blit(self.help_sur, self.help_rect)
            self.display_surface.blit(self.author_sur, self.author_rect)
        elif state == "help":
            sys.stdin = open("instruction.txt")
            for i in range(9):
                instructions = sys.stdin.readline()
                self.instructions_sur, self.instructions_rect = self.make_text(instructions, self.text_color,
                                                                               self.tile_color,
                                                                               (self.window_width/2,
                                                                                self.window_height/2-120+i*30))
                self.display_surface.blit(self.instructions_sur, self.instructions_rect)
            self.back_sur, self.back_rect = self.make_text("Back", self.text_color, self.tile_color,
                                                           (self.window_width-60, self.window_height-650))
            self.display_surface.blit(self.back_sur, self.back_rect)
        elif state == "author":
            sys.stdin = open("author.txt")
            for i in range(8):
                if i == 0:
                    instructions = sys.stdin.readline()
                    self.instructions_sur, self.instructions_rect = self.make_text(instructions, self.colors["red"],
                                                                                   self.tile_color,
                                                                                   (self.window_width/2,
                                                                                    self.window_height/2-180+i*30))
                    self.display_surface.blit(self.instructions_sur, self.instructions_rect)
                else:
                    instructions = sys.stdin.readline()
                    self.instructions_sur, self.instructions_rect = self.make_text(instructions, self.text_color
                                                                                   ,self.tile_color,
                                                                                   (self.window_width/2,
                                                                                    self.window_height/2-120+i*30))
                    self.display_surface.blit(self.instructions_sur, self.instructions_rect)
            self.back_sur, self.back_rect = self.make_text("Back", self.text_color, self.tile_color,
                                                           (self.window_width-60, self.window_height-650))
            self.display_surface.blit(self.back_sur, self.back_rect)
        elif state == "settings":
            self.difficulty_sur, self.difficilty_rect = self.make_text("Difficulty: %s%%" %
                                                                       str(self.state.get_difficulty()*100)[0:2],
                                                                       self.text_color, self.tile_color,
                                                                       (self.window_width/2, self.window_height/2-100))
            self.back_sur, self.back_rect = self.make_text("Back", self.text_color, self.tile_color,
                                                           (self.window_width-60, self.window_height-650))
            self.display_surface.blit(self.back_sur, self.back_rect)
            self.display_surface.blit(self.difficulty_sur, self.difficilty_rect)
            self.difficulty_line = pygame.draw.line(self.display_surface, self.colors["white"],
                                                    (self.window_width/4, self.window_height/2),
                                                    (self.window_width*3/4, self.window_height/2), 5)
            pygame.draw.circle(self.display_surface, self.colors["red"],
                               tuple(self.pos), 15)
        elif state == "new game":
            scores = [self.state.get_player_score(), self.state.get_computer_score()]
            self.numbers = self.logic.get_numbers_for_draw()
            for index in range(len(self.numbers)):
                self.draw_tile(self.numbers[index], index)
            self.total_win_sur, self.total_win_rect = self.make_text("You %d : %d Com" %
                                                                     (self.state.get_player_win(),
                                                                      self.state.get_com_win()),
                                                                     self.text_color, self.tile_color,
                                                                     (self.window_width/2, self.y_margin))
            self.player_score_sur, self.player_score_rect = self.make_text("You: %d" % scores[0],
                                                                           self.text_color, self.tile_color,
                                                                           (self.x_margin, self.y_margin))
            self.computer_score_sur, self.computer_score_rect = self.make_text("Computer: %d" % scores[1],
                                                                               self.text_color, self.tile_color,
                                                                               (self.window_width-self.x_margin, self.y_margin))
            self.first_sur, self.first_rect = self.make_text("first", self.text_color, self.tile_color,
                                                             (self.x_margin, self.window_height-self.y_margin))
            self.last_sur, self.last_rect = self.make_text("last", self.text_color, self.tile_color,
                                                           (self.window_width-self.x_margin, self.window_height-self.y_margin))
            self.display_surface.blit(self.total_win_sur, self.total_win_rect)
            self.display_surface.blit(self.first_sur, self.first_rect)
            self.display_surface.blit(self.last_sur, self.last_rect)
            self.display_surface.blit(self.player_score_sur, self.player_score_rect)
            self.display_surface.blit(self.computer_score_sur, self.computer_score_rect)
        elif state == "game over":
            scores = [self.state.get_player_score(), self.state.get_computer_score()]
            if scores[0] > scores[1]:
                self.state.track_win(0)
                self.result_sur, self.result_rect = self.make_text("Congratulations, you've beaten the computer with %d over %d" % (scores[0], scores[1]),
                                                                   self.text_color, self.tile_color,
                                                                   (self.window_width/2, self.window_height/2))
            elif scores[0] < scores[1]:
                self.state.track_win(1)
                self.result_sur, self.result_rect = self.make_text("Oops, you've lost to the computer with %d over %d. Try again!" % (scores[1], scores[0])
                                                                   ,self.text_color, self.tile_color,
                                                                   (self.window_width/2, self.window_height/2))
            else:
                self.result_sur, self.result_rect = self.make_text("Good try, you've made a draw to the computer with %d and %d" % (scores[0], scores[1]),
                                                                   self.text_color, self.tile_color,
                                                                   (self.window_width/2, self.window_height/2))
            self.play_again_sur, self.play_again_rect = self.make_text("Play again", self.text_color, self.tile_color,
                                                                       (self.x_margin, self.window_height-self.y_margin))
            self.quit_sur, self.quit_rect = self.make_text("Quit", self.text_color, self.tile_color,
                                                           (self.window_width-self.x_margin,
                                                            self.window_height-self.y_margin))
            self.new_game_sur, self.new_game_rect = self.make_text("New game", self.text_color, self.tile_color,
                                                                   (self.window_width/2, self.window_height-self.y_margin))
            self.display_surface.blit(self.result_sur, self.result_rect)
            self.display_surface.blit(self.play_again_sur, self.play_again_rect)
            self.display_surface.blit(self.quit_sur, self.quit_rect)
            self.display_surface.blit(self.new_game_sur, self.new_game_rect)


class GameLogic:
    def __init__(self):
        self.list_of_numbers = range(1, 26)
        self.first_removed = 0  # for drawing
        self.last_removed = len(self.list_of_numbers)-1  # we can keep track of which numbers have been removed
        self.first_last = [self.first_removed, self.last_removed]  # to highlight the tiles to choose
        random.shuffle(self.list_of_numbers)
        self.list_of_numbers_for_draw = self.list_of_numbers[:]

    def start_again(self):
        """
        Reset the game
        """
        self.list_of_numbers = range(1, 26)
        self.first_removed = 0
        self.last_removed = len(self.list_of_numbers)-1
        random.shuffle(self.list_of_numbers)
        self.list_of_numbers_for_draw = self.list_of_numbers[:]

    def update_fl(self):
        """
        Update the first_last list according to first_removed and last_removed,
        so we can highlight the tiles to be chosen
        """
        self.first_last = [self.first_removed, self.last_removed]

    def pick_number(self, index):
        target = self.list_of_numbers[index]
        del self.list_of_numbers[index]
        if index == 0:
            self.list_of_numbers_for_draw[self.first_removed] = ""
            self.first_removed += 1
        elif index == -1:
            self.list_of_numbers_for_draw[self.last_removed] = ""
            self.last_removed -= 1
        return target

    def get_numbers_left(self):
        return self.list_of_numbers

    def get_numbers_for_draw(self):
        return self.list_of_numbers_for_draw


class GameState:
    """
    The pick a number game state
    """
    def __init__(self):
        self.state = "welcome"
        self.already_count_win = False
        self.already_over = False
        self.difficulty = 0.5
        self.player = 0
        self.computer = 0
        self.player_win = 0
        self.com_win = 0
        self.current_player = 0 # 0 for human, 1 for computer

    def new_game(self):
        """
        Reset the game states for new round
        :return:
        """
        self.already_count_win = False
        self.already_over = False
        self.player = 0
        self.computer = 0
        self.current_player = 0

    def track_win(self, player):
        """
        Track the win of player and computer
        :param player:
        :return:
        """
        if not self.already_count_win:
            self.already_count_win = True
            if player == 0:
                self.player_win += 1
            else:
                self.com_win += 1

    def get_com_win(self):
        return self.com_win

    def get_player_win(self):
        return self.player_win

    def start_again(self):
        """
        Reset for a new game
        :return:
        """
        self.already_count_win = False
        self.state = "welcome"
        self.already_over = False
        self.difficulty = 0.5
        self.player = 0
        self.computer = 0
        self.player_win = 0
        self.com_win = 0
        self.current_player = 0 # 0 for human, 1 for computer

    def get_already_over(self):
        return self.already_over

    def set_already_over(self, val):
        self.already_over = val

    def get_difficulty(self):
        return self.difficulty

    def set_difficulty(self, val):
        self.difficulty = val

    def increment_score(self, player, number):
        if player == 0:
            self.player += number
        else:
            self.computer += number

    def set_current_player(self, player):
        self.current_player = player

    def get_current_player(self):
        return self.current_player

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def get_player_score(self):
        return self.player

    def get_computer_score(self):
        return self.computer


class Sound:
    def __init__(self):
        self.music = music

    def play_music(self):
        self.music[0]("sound/background1.mid", "bg_music")

    def stop_music(self):
        self.music[1]()

    def play_beep(self):
        self.music[0]("sound/beep1.ogg", "click")


class EventLogic:
    def __init__(self, _game_state, _game_gui, _game_logic, _sound):
        self._game_state = _game_state
        self._game_gui = _game_gui
        self._game_logic = _game_logic
        self._sound = _sound

    def quit(self):
        pygame.quit()
        sys.exit()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if self._game_state.get_state() == "welcome":
                    if self._game_gui.new_rect.collidepoint(event.pos):
                        self._game_state.set_state("new game")
                        self._sound.stop_music()
                    elif self._game_gui.setting_rect.collidepoint(event.pos):
                        self._game_state.set_state("settings")
                    elif self._game_gui.quit_rect.collidepoint(event.pos):
                        self.quit()
                    elif self._game_gui.help_rect.collidepoint(event.pos):
                        self._game_state.set_state("help")
                    elif self._game_gui.author_rect.collidepoint(event.pos):
                        self._game_state.set_state("author")
                elif self._game_state.get_state() == "settings":
                    if self._game_gui.back_rect.collidepoint(event.pos):
                        self._game_state.set_state("welcome")
                    elif self._game_gui.difficulty_line.collidepoint(event.pos):
                        self._game_gui.configure_difficulty(event.pos)
                        self._game_state.set_difficulty((event.pos[0]-self._game_gui.window_width/4)*2/float(self._game_gui.window_width))
                        print self._game_state.get_difficulty()
                elif self._game_state.get_state() == "help":
                    if self._game_gui.back_rect.collidepoint(event.pos):
                        self._game_state.set_state("welcome")
                elif self._game_state.get_state() == "author":
                    if self._game_gui.back_rect.collidepoint(event.pos):
                        self._game_state.set_state("welcome")
                elif self._game_state.get_state() == "new game":
                    if self._game_state.get_current_player() == 0:
                        if self._game_gui.first_rect.collidepoint(event.pos):
                            self._sound.play_beep()
                            self._game_state.increment_score(0, self._game_logic.pick_number(0))
                            self._game_state.set_current_player(1)
                        elif self._game_gui.last_rect.collidepoint(event.pos):
                            self._sound.play_beep()
                            self._game_state.increment_score(0, self._game_logic.pick_number(-1))
                            self._game_state.set_current_player(1)
                elif self._game_state.get_state() == "game over":
                    if self._game_gui.new_game_rect.collidepoint(event.pos):
                        self._sound.play_beep()
                        self._game_state.set_state("welcome")
                        self._sound.play_music()
                        self._game_logic.start_again()
                        self._game_state.start_again()
                    elif self._game_gui.quit_rect.collidepoint(event.pos):
                        self._sound.play_beep()
                        self.quit()
                    elif self._game_gui.play_again_rect.collidepoint(event.pos):
                        self._sound.play_beep()
                        self._game_state.new_game()
                        self._game_logic.start_again()
                        self._game_state.set_state("new game")
            elif event.type == pygame.QUIT:
                self.quit()
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self._sound.play_beep()
                    self.quit()


def key_for_min(pick):
    """
    Helper function for choose_a_pick
    :param pick:
    :return:
    """
    return pick[1][1]


def choose_a_pick(numbers_left):
    """
    AI for choosing a number
    :param numbers_left:
    :return:
    """
    if len(numbers_left) <= 3:
        if numbers_left[0] > numbers_left[-1]:
            return 0, numbers_left[0]
        elif numbers_left[-1] > numbers_left[0]:
            return -1, numbers_left[-1]
        else:
            return 0, numbers_left[0]
    else:
        possible_picks = []
        for move in [0, -1]:
            if move == 0:
                possible_picks.append([0, choose_a_pick(numbers_left[1:])])
            else:
                possible_picks.append([-1, choose_a_pick(numbers_left[:-1])])
        best_pick = min(possible_picks, key=key_for_min)
        return best_pick[0], numbers_left[best_pick[0]]


def choose_a_pick_naive(numbers_left):
    """
    Choose any larger number
    :param numbers_left:
    :return:
    """
    if numbers_left[0] > numbers_left[-1]:
        return 0, numbers_left[0]
    elif numbers_left[-1] > numbers_left[0]:
        return -1, numbers_left[-1]
    else:
        return 0, numbers_left[0]


if __name__ == "__main__":
    sound_game = Sound()
    game_logic = GameLogic()
    game_state = GameState()
    game_gui = GameGUI(game_logic, game_state)
    game_event_handler = EventLogic(game_state, game_gui, game_logic, sound_game)
    sound_game.play_music()
    while True:
        game_gui.draw(game_state.get_state())
        game_event_handler.event_handler()
        pygame.display.update()
        if game_state.get_current_player() == 1:
            if len(game_logic.get_numbers_left()) > 0:
                if random.random() > game_state.get_difficulty():
                    computer_choice = choose_a_pick_naive(game_logic.get_numbers_left())
                else:
                    computer_choice = choose_a_pick(game_logic.get_numbers_left())
                game_state.increment_score(1, computer_choice[1])
                game_logic.pick_number(computer_choice[0])
                game_state.set_current_player(0)
            else:
                if not game_state.get_already_over():
                    game_state.set_state("game over")
                    game_state.set_already_over(True)
        pygame.display.update()
