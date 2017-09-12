import pygame
from pygame.locals import *

if pygame.version.vernum < (1,5):
    print( 'Warning, older version of pygame %s' % pygame.version.ver )

from core.startState import StartState
from core.gameState  import GameState
from core.pauseState import PauseState
from core.gui import GUI
