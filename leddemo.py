import ledshim
def led():
    for col in ((255, 0, 0), (0, 255, 0), (0, 0, 255)):
        r, g, b = col
        for x in range(ledshim.DISPLAY_WIDTH):
            ledshim.clear()
            ledshim.set_pixel(x, r, g, b)
            ledshim.show()


if __name__ == '__main__':
    led()

