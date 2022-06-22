import pygame as pg
import gas_simulation
import config

TIMEEVENT = pg.USEREVENT + 1

# Properties import from config file
def main():
    # window caption
    pg.display.set_caption(config.caption)
    # display window
    screen = pg.display.set_mode(size=(config.width, config.height))
    # set environment parameters
    env = gas_simulation.Environment(config.width, config.height)

    # add some particles
    env.addParticles(config.n)

    running = True
    pause = False

    pg.time.set_timer(TIMEEVENT, config.time_step)
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # close the window
                running = False
            if event.type == TIMEEVENT:
                screen.fill(env.color)
                env.update()
                env.draw(screen)
            if event.type == pg.KEYDOWN:
                # space pause the simulation
                if event.key == pg.K_SPACE:
                    # negate state of pause
                    pause = not pause
                    # pause the timer of a simulation
                    pg.time.set_timer(TIMEEVENT, config.time_step if not pause else 0)
                
        # pygame display
        pg.display.flip()

if __name__ == '__main__':
    main()
