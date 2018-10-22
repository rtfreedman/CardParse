import json
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

RED = '\033[0;31m'
GREEN = '\033[0;32m'
NC = '\033[0m'

with open('wizbolt.json', 'r') as f:
    items = json.loads(f.read())['items']
have_name = all(['Name' in i for i in items])
have_cost = all(['Cost' in i for i in items])
have_description = all(['Description' in i for i in items])
have_length = all([len(i) == 3 for i in items])
print(f'- All items have name : {[RED, GREEN][have_name]}{have_name}{NC}')
print(f'- All items have cost : {[RED, GREEN][have_cost]}{have_cost}{NC}')
print(f'- All items have description : {[RED, GREEN][have_description]}{have_description}{NC}')
print(f'- All items only have 3 keys : {[RED, GREEN][have_length]}{have_length}{NC}')
if not all([have_name, have_cost, have_description, have_cost]):
    print(f'{RED}JSON input error.{NC}')
    exit(0)

titleFont = ImageFont.truetype('Thempo New St.ttf', 48)
restFont = ImageFont.truetype('monofonto.ttf', 24)
max_title_line_length = 33
max_line_length = 58
try:
    os.mkdir("cards")
except OSError:
    pass

print(f'Making {len(items)} cards...')
for i in range(len(items)):
    item = items[i]
    cardFront = Image.open('Cardfront.png')
    draw = ImageDraw.Draw(cardFront)
    vertical_offset = 0
    if len(item['Name']) > max_title_line_length:
        words = item['Name'].split(' ')
        words[-2] += '\n'
        item['Name'] = ' '.join(words)
        vertical_offset = 50
    draw.text((25, 25), item['Name'], (55, 55, 55), font=titleFont)
    draw.text((25, 100 + vertical_offset), item['Cost'], (155, 135, 0), font=restFont)
    new_description = []
    for line in item['Description'].split('\n'):
        if len(line) <= max_line_length:
            new_description.append(line)
        else:
            prev = 0
            while prev < len(line) - max_line_length:
                end = prev + line[prev:prev + max_line_length].rfind(' ')
                if end <= prev:
                    end = prev + max_line_length
                new_description.append(line[prev:end])
                prev = end
            new_description.append(line[prev:])
    item['Description'] = '\n'.join(new_description)
    draw.text((30, 150 + vertical_offset), item['Description'], (0, 0, 0), font=restFont)
    cardFront.save(f'cards/{i}.png')
