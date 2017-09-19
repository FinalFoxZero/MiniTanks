import pygame, os

class Library:
    def __init__(self):
        self.imagePath = os.getcwd() + '/assets/images/'
        self.soundPath = os.getcwd() + '/assets/sounds/'
        self.library = {}

    def grab(self, file):
        load_success = False
        if not file in self.library:
            if file in os.listdir(self.imagePath):
                newImage = pygame.image.load(self.imagePath+file).convert_alpha()
                self.library[file] = newImage
                print('Adding [%s] to library' %  file)
                load_success = True
            elif file in os.listdir(self.soundPath):
                newSound = pygame.mixer.Sound(self.soundPath+file)
                self.library[file] = newSound
                print('Added [%s] to library' % file)
                load_success = True
            else:
                print('Failed to load [%s]' % file)
        elif file in self.library: load_success = True
        if load_success: return(self.library[file])
