import pygame, os

class textures:
    def __init__(self):
        self.imgPath = os.getcwd() + '/assets/images/'
        self.lib = {}

    def grab(self, image):
        image = self.imgPath + image
        if not image in self.lib:
            new_image = pygame.image.load(image).convert_alpha()
            self.lib[image] = new_image
            print('Adding %s to library' %  image)
        return(self.lib[image])
