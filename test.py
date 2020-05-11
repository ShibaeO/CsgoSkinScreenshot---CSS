from PIL import ImageGrab, Image, ImageOps
"""
img = Image.open("1_playside.png")
#img1 = Image.open("final2.png")
#img2 = Image.open("final22.png")
#img3 = Image.open("sep.png")

border = (283, 382, 321, 291) # left, up, right, bottom
cropped = ImageOps.crop(img, border)
cropped.save("cropped_ar_play.png", "png")

def get_concat_v(im1, im2, im3):
    dst = Image.new('RGB', (im1.width, im1.height + im3.height + im2.height))
    dst.paste(im2, (0, 0))
    dst.paste(im3, (0, im2.height))
    dst.paste(im1, (0, im2.height + im3.height))

    return dst

#get_concat_v(img1, img2, img3).save("img3.png", "png")

# crop ar play side : border = (283, 382, 321, 291)
# crop ar back side : border = (321, 382, 283, 291)
"""

from steam.client import SteamClient
from csgo.client import CSGOClient

client = SteamClient()
cs = CSGOClient(client)

@client.on('logged_on')
def start_csgo():
    cs.launch()

@cs.on('ready')
def gc_ready():
    # send messages to gc
    pass

client.cli_login()
client.run_forever()
cs.request_player_profile(cs.account_id)
response, = cs.wait_event('player_profile')
