from pathlib import Path
from PIL import Image
from IPython.display import display
import os
import random
import json
import requests

bg = ["sad", "happy"]
bg_weights = [50, 50]

goblin = ["green", "yellow"]
goblin_weights = [50, 50]

cloth = ["red", "blue"]
cloth_weights = [50, 50]


bg_files = {
    "sad": "sad",
    "happy": "happy",
}

goblin_files = {
    "green": "green",
    "yellow": "yellow",
}

cloth_files = {
    "red": "red",
    "blue": "blue",
}


TOTAL_IMAGES = 8

all_images = []


def create_new_image():

    new_image = {}

    new_image["Bg"] = random.choices(bg, bg_weights)[0]
    new_image["Goblin"] = random.choices(goblin, goblin_weights)[0]
    new_image["Cloth"] = random.choices(cloth, cloth_weights)[0]

    if new_image in all_images:
        return create_new_image()
    else:
        return new_image


for i in range(TOTAL_IMAGES):

    new_trait_image = create_new_image()

    all_images.append(new_trait_image)


def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)


print("Are all images unique?", all_images_unique(all_images))


i = 0
for item in all_images:
    item["tokenId"] = i
    i = i + 1


print(all_images)


bg_count = {}
for item in bg:
    bg_count[item] = 0

goblin_count = {}
for item in goblin:
    goblin_count[item] = 0

cloth_count = {}
for item in cloth:
    cloth_count[item] = 0

for image in all_images:
    bg_count[image["Bg"]] += 1
    goblin_count[image["Goblin"]] += 1
    cloth_count[image["Cloth"]] += 1

print(bg_count)
print(goblin_count)
print(cloth_count)


METADATA_FILE_NAME = './utils/data/all-traits.json'
with open(METADATA_FILE_NAME, 'w') as outfile:
    json.dump(all_images, outfile, indent=4)


for item in all_images:

    im0 = Image.open(
        f'./trait-layers/bg/{bg_files[item["Bg"]]}.png').convert('RGBA')
    im1 = Image.open(
        f'./trait-layers/goblins/{goblin_files[item["Goblin"]]}.png').convert('RGBA')
    im2 = Image.open(
        f'./trait-layers/clothes/{cloth_files[item["Cloth"]]}.png').convert('RGBA')

    com0 = Image.alpha_composite(im0, im1)
    com1 = Image.alpha_composite(com0, im2)

    rgb_im = com1
    file_name = str(item["tokenId"]) + ".png"
    rgb_im.save("./public/images/" + file_name)


f = open(METADATA_FILE_NAME,)
data = json.load(f)

PROJECT_NAME = "Lucky guy"


def upload_to_pinata(file_path, filename):
    PINATA_BASE_URL = 'https://api.pinata.cloud/'
    endpoint = 'pinning/pinFileToIPFS'
    headers = {'pinata_api_key': os.getenv('PINATA_API_KEY'),
               'pinata_secret_api_key': os.getenv('PINATA_API_SECRET')}
    with Path(file_path).open('rb') as fp:
        binary = fp.read()
        response = requests.post(PINATA_BASE_URL + endpoint,
                                 files={"file": (filename, binary)},
                                 headers=headers)
        return response.json()['IpfsHash']
    return None


def getAttribute(key, value):
    return {
        "trait_type": key,
        "value": value
    }


hashes_to_unpin = []

for i in data:
    token_id = i['tokenId']

    bg = i["Bg"]
    goblin = i["Goblin"]
    cloth = i["Cloth"]

    token = {
        "name": PROJECT_NAME + ' #' + str(token_id),
        "description": "{} {} {}".format(goblin.title(), cloth, bg),
        "attributes": []
    }
    token["attributes"].append(getAttribute("Bg", bg))
    token["attributes"].append(getAttribute("Goblin", goblin))
    token["attributes"].append(getAttribute("Cloth", cloth))

    file_path = "./public/images/{}.png".format(token_id)
    filename = file_path.split("/")[-1:][0]

    image_to_upload = upload_to_pinata(file_path, filename)
    hashes_to_unpin.append(image_to_upload)
    token["image"] = 'ipfs://' + image_to_upload

    print(token)

    metadata_file_path = './public/metadata/{}.json'.format(str(token_id))
    with open(metadata_file_path, 'w') as outfile:
        json.dump(token, outfile, indent=4)

with open("./utils/data/hashes_to_unpin.json", "w") as outfile:
    json.dump(hashes_to_unpin, outfile, indent=4)

f.close()
