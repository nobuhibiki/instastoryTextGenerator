import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import textwrap
import requests
from bs4 import BeautifulSoup
import os
import lxml

blurryness = 3
brightness = 0.3

font_size = 40
font_colour = (255,255,255)
line_height = 50
ratio = 1920

line_break = 53
margin = 100

lines = []
with open('to_print.txt') as f:
    for line in f:
        if line == "\n":
            lines += line
        else:
            lines += textwrap.wrap(line, line_break, break_long_words=False)

max_line_in_one_image = (ratio - (margin * 2))//line_height
pages = len(lines) // max_line_in_one_image

search_photos = str(sys.argv[1])
how_many_to_download = pages
print(pages)

def photo_downloader(url):
    request = requests.get(url,allow_redirects = True)
    data = BeautifulSoup(request.text,'lxml')
    all_image=data.find_all('figure',itemprop="image")
    count = 0
    for i in all_image:
        url=i.find('a',rel="nofollow")
        if url != None:
            i_url = url['href']
            photo_bytes = requests.get(i_url,allow_redirects=True)
            with open(f'img{count}.jpg','wb') as photo:
                photo.write(photo_bytes.content)
                if count == how_many_to_download:
                    break
                count += 1
                

    print("Done")

if __name__ == "__main__":
    photo_downloader("https://unsplash.com/s/photos/" + search_photos)


current_line = 0
current_image = 0
print(len(lines))

while current_image <= pages:
    img = Image.open("img" + str(current_image) + ".jpg")

    height_percent = ratio/float(img.size[1])
    width_size = int((float(img.size[0])*float(height_percent)))
    img = img.resize((width_size, ratio))

    img = img.crop((img.width // 4,0,(img.width // 4 + 1080) ,1920))
    img = img.filter(ImageFilter.GaussianBlur(blurryness))
    img = ImageEnhance.Brightness(img).enhance(brightness)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("times.ttf", font_size)
    font_source = ImageFont.truetype("timesi.ttf", 25)
    draw.text((880, 1870), "photos: unsplash" ,(font_colour),font=font_source)

    j = 0
    while current_line < len(lines):
        text_x = margin + (line_height*j)
        draw.text((margin, text_x),lines[current_line],(font_colour),font=font) # this will draw text with Blackcolor and 16 size
        
        j += 1
        current_line += 1
        
        if j == max_line_in_one_image:
            img.save('output' + str(current_image) + '.jpg')
            current_image += 1
            print(current_line)
            break
        
        if current_line == len(lines):
            img.save('output' + str(current_image) + '.jpg')
            current_image += 1
            print(current_line) 
            break
        

