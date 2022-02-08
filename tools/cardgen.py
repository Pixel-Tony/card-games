from PIL import Image
HEADLEN = 8
SPADE, HEART, CLUB, DIAMOND = '♠♥♣♦'
SUITS = [SPADE, HEART, CLUB, DIAMOND]
ORDER = [*range(2, 11), *'JQKA'] # 2-3-4-5-6-7-8-9-10-J-K-Q-A
DECK = [(index, suit) for suit in SUITS for index in ORDER]



samples = Image.open("gfx/cards/samples.png")

values = {value : samples.crop((lambda a: (a * 9, 11, a * 9 + 8, 11 + 12))(ORDER.index(value))) for value in ORDER}

suits = {
    [HEART, DIAMOND, SPADE, CLUB][value] : {
        'big' : samples.crop((value*33, 24, value*33 + 32, 24 + 40)),
        'middle' : samples.crop((value*17, 65, value*17 + 16, 65 + 20)),
        'small' : samples.crop((value*9, 0, value*9 + 8, 10))
    } for value in [0, 1, 2, 3]
}
images = {
    "J" : samples.crop((0, 86, 50, 136)),
    "Q" : samples.crop((51, 86, 101, 136)),
    'K' : samples.crop((102, 86, 151, 136))
}

canvas = Image.open("gfx/cards/card.png")

def create(card: tuple[int | str, str]):
    card_img = canvas.copy()
    value, suit = card
    number = DECK.index(card)
    value_image = values[value]


    def contour():
        [card_img.putpixel((x, 1), (10, 10, 10)) for x in range(1, 79)]
        [card_img.putpixel((1, y), (10,)*3) for y in range(1, 129)]
        card_img.paste(value_image, (4, 4))
        card_img.paste(suits[suit]['small'], (4, 19))

    contour()
    card_img = card_img.rotate(180)
    contour()


    if value in [2, 3]:
        card_img.paste(suits[suit]['middle'], (32, 9))
        card_img = card_img.rotate(180)
        card_img.paste(suits[suit]['middle'], (32, 9))

    if value in [3, 5]:
        card_img.paste(suits[suit]['middle'], (32, 55))

    if value in range(4, 11):
        card_img.paste(suits[suit]['middle'], (14, 9))
        card_img.paste(suits[suit]['middle'], (80 - 14 - 16, 9))
        card_img = card_img.rotate(180)
        card_img.paste(suits[suit]['middle'], (14, 9))
        card_img.paste(suits[suit]['middle'], (80 - 14 - 16, 9))

    if value in [6, 7]:
        card_img.paste(suits[suit]['middle'], (14, 55))
        card_img.paste(suits[suit]['middle'], (80 - 14 - 16, 55))

    elif value in range(8, 11):
        card_img.paste(suits[suit]['middle'], (14, 9 + 16 + 13))
        card_img.paste(suits[suit]['middle'], (80 - 14 - 16, 9 + 16 + 13))
        card_img = card_img.rotate(180)
        card_img.paste(suits[suit]['middle'], (14, 9 + 16 + 13))
        card_img.paste(suits[suit]['middle'], (80 - 14 - 16, 9 + 16 + 13))

    if value == 7:
        card_img.paste(suits[suit]['middle'], (32, 9 + 16 + 10))

    elif value in [9, 10]:
        card_img.paste(suits[suit]['middle'], (32, 25))
        if value == 10:
            card_img = card_img.rotate(180)
            card_img.paste(suits[suit]['middle'], (32, 25))


    elif value in ["J", "Q", "K"]:
        [card_img.putpixel((14, y), (10, 10, 10)) for y in range(13, 130 - 13)]
        [card_img.putpixel((x, 13), (10, 10, 10)) for x in range(14, 80 - 14)]
        [card_img.putpixel((x, 65), (10, 10, 10)) for x in range(14, 80 - 14)]
        card_img.paste(images[value], (15, 14))
        card_img = card_img.rotate(180)
        [card_img.putpixel((14, y), (10, 10, 10)) for y in range(13, 130 - 13)]
        [card_img.putpixel((x, 13), (10, 10, 10)) for x in range(14, 80 - 14)]
        [card_img.putpixel((x, 65), (10, 10, 10)) for x in range(14, 80 - 14)]
        card_img.paste(images[value], (15, 14))

    elif value == 'A':
        card_img.paste(suits[suit]['big'], (24, 45))

    card_img.save(f'gfx/cards2/{number}.png')
    # card_img = card_img.resize((64, 102))
    # card_img.save(f'gfx/cards2/{number}_small.png')


for i in range(52):
    create(DECK[i])


N = 40

def create_shirt():
    card_img = canvas.copy() # 80x130

    blue = (0, 0, 255)
    white = (255,) * 3
    c = 50

    def get_destr(x, y):
        def normalize(x, y):
            return x - 40, y - 65
        x, y = normalize(x, y)
        res = 0
        if (x + y) % 3:
            res += 1
        if (x - y) % 5:
            res += 1
        return [blue, white][res % 2]

    [card_img.putpixel((x, y), get_destr(x, y)) for x in range(6, 80 - 6) for y in range(6, 130 - 6)]

    def horz(): [card_img.putpixel((x, y), blue) for x in range(6, 80 - 6) for y in [1, 3, 5]]
    def vert(): [card_img.putpixel((x, y), blue) for x in [1, 3, 5] for y in range(6, 130 - 6)]
    def corner(): card_img.paste(Image.open('gfx/cards/corner.png'), (0, 0))
    horz()
    vert()
    corner()
    card_img = card_img.transpose(Image.FLIP_LEFT_RIGHT)
    corner()
    card_img = card_img.transpose(Image.FLIP_TOP_BOTTOM)
    horz()
    vert()
    corner()
    card_img = card_img.transpose(Image.FLIP_LEFT_RIGHT)
    corner()



    # card_img.save('gfx/cards/shirt.png')
    plate = Image.new('RGB', (100, 100), (255, 255, 255))
    card_img = card_img.resize((32, 52))
    # card_img = card_img.rotate(45)
    plate.paste(card_img, (20, 20))
    plate.paste(card_img, (20 + 16, 20 + 3))
    # for i in [1, 2, 3]:
    #     plate.rotate(45*i).save(rf'gfx/cards/test00{i}.png')
    plate.rotate(60).save(rf'gfx/cards/cards_down.png')
    plate.rotate(120).save(rf'gfx/cards/cards_up.png')

create_shirt()