import os
import sys
import math
import pygame as pg


CAPTION = "Spotlight Prototype"
SCREEN_SIZE = (1000, 500)
BACKGROUND_COLOR = (5, 5, 15)


class Rotator(object):
    def __init__(self, center, origin, image_angle=0):
        self.cache = {}
        x_mag = center[0]-origin[0]
        y_mag = center[1]-origin[1]
        self.radius = math.hypot(x_mag,y_mag)
        self.start_angle = math.atan2(-y_mag,x_mag)-math.radians(image_angle)

    def __call__(self,angle,origin):
        if (angle, origin) in self.cache:
            return self.cache[angle, origin]
        new_angle = math.radians(angle)+self.start_angle
        new_x = origin[0] + self.radius*math.cos(new_angle)
        new_y = origin[1] - self.radius*math.sin(new_angle)
        self.cache[angle, origin] = (new_x, new_y)
        return (new_x, new_y)


class SpotLight(pg.sprite.DirtySprite):
    cache = {}

    def __init__(self, pos, period, arc, start=0, *groups):
        super(SpotLight, self).__init__(*groups)
        self.blendmode = pg.BLEND_RGB_ADD
        self.angle = 0
        self.raw_image = SPOTLIGHT
        self.rect = self.raw_image.get_rect(midbottom=pos)
        self.origin = self.rect.midbottom
        self.rotator = Rotator(self.rect.center, self.origin, self.angle)
        self.period = period
        self.elapsed = period*start
        self.arc = arc//2
        self.make_image()

    def make_image(self):
        if self.angle in SpotLight.cache:
            self.image = SpotLight.cache[self.angle]
        else:
            self.image = pg.transform.rotozoom(self.raw_image, self.angle, 1)
            SpotLight.cache[self.angle] = self.image
        new_center = self.rotator(self.angle, self.origin)
        self.rect = self.image.get_rect(center=new_center)

    def update(self, dt):
        self.elapsed += dt
        interp = math.sin(2*math.pi*(self.elapsed/float(self.period)))
        self.elapsed %= self.period
        angle = self.arc*interp
        if int(angle) != self.angle:
            self.angle = int(angle)
            self.make_image()
            self.dirty = 1


class Control(object):
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.done = False
        self.background = pg.Surface(self.screen_rect.size).convert()
        self.background.fill(BACKGROUND_COLOR)
        self.lights = self.make_lights()
        self.dirty_rects = []

    def make_lights(self):
        lights = pg.sprite.LayeredDirty()
        y = self.screen_rect.bottom+20
        for i in range(1,5):
            start = 1 if i%2 else 0.5
            SpotLight((i*self.screen_rect.w/5,y), 4, 140, start, lights)
        return lights

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

    def update(self, dt):
        self.lights.update(dt)

    def draw(self):
        self.lights.clear(self.screen, self.background)
        self.dirty_rects = self.lights.draw(self.screen)

    def display_fps(self):
        caption = "{} - FPS: {:.2f}".format(CAPTION, self.clock.get_fps())
        pg.display.set_caption(caption)

    def main_loop(self):
        self.screen.blit(self.background, (0,0))
        pg.display.update()
        delta = self.clock.tick(self.fps)/1000.0
        while not self.done:
            self.event_loop()
            self.update(delta)
            self.draw()
            pg.display.update(self.dirty_rects)
            self.display_fps()
            delta = self.clock.tick(self.fps)/1000.0


def main():
    global SPOTLIGHT
    pg.init()
    os.environ["SDL_VIDEO_CENTERED"] = "TRUE"
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)
    SPOTLIGHT = pg.image.load("spotlight.png").convert_alpha()
    Control().main_loop()
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
