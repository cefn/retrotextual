def hue_to_rgb(h):
    return hsb_to_rgb(h, 1.0, 1.0)


def hsb_to_rgb(h, s, b):
    if s == 0.0: return b, b, b
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = b * (1.0 - s)
    q = b * (1.0 - s * f)
    t = b * (1.0 - s * (1.0 - f))
    if i % 6 == 0: rgb = b, t, p
    if i == 1: rgb = q, b, p
    if i == 2: rgb = p, b, t
    if i == 3: rgb = p, q, b
    if i == 4: rgb = t, p, b
    if i == 5: rgb = b, p, q
    return [int(color * 255) for color in rgb]


def setBrightness(color, brightness):
    return [int(primary * brightness) for primary in color]

MAX=127

red = [MAX, 0, 0]
green = [0, MAX, 0]
blue = [0, 0, MAX]

yellow = [MAX, MAX, 0]
purple = [MAX, 0, MAX]
teal = [0, MAX, MAX]

orange = [MAX, MAX//2, 0]
pink = [MAX, MAX//4, MAX//4]

white = [MAX, MAX, MAX]
black = [0, 0, 0]
