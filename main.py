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
                       "red": (255, 0, 255),
                       "blue": (0, 0, 255),
                       "dark": (3, 54, 73),
                       "green": (0, 204, 0)}
        self.tile_color = self.colors["green"]
        self.text_color = self.colors["white"]
        self.bg_color = self.colors["dark"]
        self.display_surface = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Pick A Number')
        self.font = pygame.font.Font('GatsbyFLF-Bold.ttf', self.font_size)

    def make_text(self, text, color, bg_color, center):
        textSurf = self.font.render(text, True, color, bg_color)
        textRect = textSurf.get_rect()
        textRect.center = center
        return (textSurf, textRect)

    def draw_tile(self, number, index):
        size = 40
        space = 1
        position = (self.x_margin+(size+space)*index, self.y_margin*2)
        pygame.draw.rect(self.display_surface, self.tile_color, (position[0], position[1], size, size))
        text_sur = self.font.render(str(number), True, self.text_color)
        text_rect = text_sur.get_rect()
        text_rect.center = (position[0]+size/2, position[1]+size/2)
        self.display_surface.blit(text_sur, text_rect)

    def draw(self, state):
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
                                                                               self.colors["dark"],
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
                                                                                   self.colors["dark"],
                                                                                   (self.window_width/2,
                                                                                    self.window_height/2-180+i*30))
                    self.display_surface.blit(self.instructions_sur, self.instructions_rect)
                else:
                    instructions = sys.stdin.readline()
                    self.instructions_sur, self.instructions_rect = self.make_text(instructions, self.text_color
                                                                                   ,self.colors["dark"],
                                                                                   (self.window_width/2,
                                                                                    self.window_height/2-120+i*30))
                    self.display_surface.blit(self.instructions_sur, self.instructions_rect)
            self.back_sur, self.back_rect = self.make_text("Back", self.text_color, self.tile_color,
                                                           (self.window_width-60, self.window_height-650))
            self.display_surface.blit(self.back_sur, self.back_rect)
        elif state == "settings":
            self.back_sur, self.back_rect = self.make_text("Back", self.text_color, self.tile_color,
                                                           (self.window_width-60, self.window_height-650))
            self.display_surface.blit(self.back_sur, self.back_rect)
            pygame.draw.line(self.display_surface, self.colors["white"],
                             (self.window_width/4, self.window_height/2),
                             (self.window_width*3/4, self.window_height/2), 5)
            pygame.draw.circle(self.display_surface, self.colors["red"],
                               (self.window_width/2, self.window_height/2), 15)
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
        self.first_removed = 0
        self.last_removed = -1
        random.shuffle(self.list_of_numbers)
        self.list_of_numbers_for_draw = self.list_of_numbers[:]

    def start_again(self):
        self.list_of_numbers = range(1, 26)
        self.first_removed = 0
        self.last_removed = -1
        random.shuffle(self.list_of_numbers)
        self.list_of_numbers_for_draw = self.list_of_numbers[:]

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
        self.already_count_win = False
        self.already_over = False
        self.player = 0
        self.computer = 0
        self.current_player = 0

    def track_win(self, player):
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
                    self._sound.stop_music()
                    if self._game_gui.new_rect.collidepoint(event.pos):
                        self._game_state.set_state("new game")
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
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self._sound.play_beep()
                    self.quit()


def key_for_min(pick):
    return pick[1][1]


def choose_a_pick(numbers_left):
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
                computer_choice = choose_a_pick(game_logic.get_numbers_left())
                game_state.increment_score(1, computer_choice[1])
                game_logic.pick_number(computer_choice[0])
                game_state.set_current_player(0)
            else:
                if not game_state.get_already_over():
                    game_state.set_state("game over")
                    game_state.set_already_over(True)
        pygame.display.update()
