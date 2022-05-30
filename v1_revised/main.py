import pygame as pg
import gas_simulation
import config

TIMEEVENT = pg.USEREVENT + 1

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
                if event.key == pg.K_SPACE:
                    pause = True
        while pause:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    # close the window
                    running = False
                    pause = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        pause = False
                
        
        pg.display.flip()


if __name__ == '__main__':
    # LM: sorry, had to. Nice job so far!
    main()
