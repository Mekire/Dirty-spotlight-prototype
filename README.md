 
#Spotlight Prototype using Dirty Rects

This is an attempt to get better performance out of my spotlights.  They use additive blending which is extremely slow in pygame.  If the blending is turned off they have no issues maintaining 60fps.

In this repo I attempt to return them to 60 fps using dirty rects (and any other technique that works), while not sacrificing the blending effect.