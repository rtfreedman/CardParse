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

title_font = ImageFont.truetype('Thempo New St.ttf', 48)
rest_font = ImageFont.truetype('monofonto.ttf', 24)
max_title_line_length = 20  # 20 for mini, 33 for regular
max_line_length = 40  # 40 for mini, 58 for regular
try:
    os.mkdir("cards")
except OSError:
    pass


# returns length of the split string s (plus the whitespace when joined back together)
# assumes a trailing whitespace
def sumplus(s):
    acc = 0
    for i in s:
        acc += len(i) + 1
    return acc


print(f'Making {len(items)} cards...')
for i in range(len(items)):
    item = items[i]
    filename = item['Name'].replace(' ', '_').replace('\'', '').lower()
    cardFront = Image.open('CardfrontDarkMini.png')
    draw = ImageDraw.Draw(cardFront)
    vertical_offset = 0
    if len(item['Name']) > max_title_line_length:
        subset = item['Name'].split(' ')
        words = item['Name'].split(' ')
        while sumplus(subset) > max_title_line_length:
            subset.pop()
        words[len(subset)] = '\n' + words[len(subset)]
        item['Name'] = ' '.join(words)
        vertical_offset = 50
    draw.text((25, 25), item['Name'], (155, 155, 155), font=title_font)
    draw.text((25, 100 + vertical_offset), item['Cost'], (155, 135, 0), font=rest_font)
    new_description = []
    line_length = max_line_length
    desc_font = rest_font
    if len(item['Description']) > 750 or (len(item['Description']) > 600 and vertical_offset):
        line_length = 58
        desc_font = ImageFont.truetype('monofonto.ttf', 16)
    for line in item['Description'].split('\n'):
        if len(line) <= line_length:
            new_description.append(line)
        else:
            prev = 0
            while prev < len(line) - line_length:
                end = prev + line[prev:prev + line_length].rfind(' ')
                if end <= prev:
                    break
                new_description.append(line[prev:end])
                prev = end
            new_description.append(line[prev:])
    item['Description'] = '\n'.join(new_description)
    draw.text((30, 150 + vertical_offset), item['Description'], (255, 255, 255), font=desc_font)
    cardFront.save(f'cards/{filename}.png')
