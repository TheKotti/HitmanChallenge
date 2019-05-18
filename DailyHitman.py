import random
import json
import datetime
import math
import os
import sys
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFilter
import twitter
import configparser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import GlobalVars as V
import ChallengeFunctions as F

location = sys.path[0]

#Open error log
log = open(os.path.join(location,'errors.log'), 'a')

config = configparser.ConfigParser()
config.read(os.path.join(location, "config.ini"))

#Get current day and use it as seed for random
date = datetime.datetime.today().strftime('%d%m%y')
#random.seed(date)

#Get JSON-data from file
json_string = open(os.path.join(location, "data.json")).read()
json_data = json.loads(json_string)

#JSON-data -> list of Challenges
for x in json_data["challenges"]:
    c = V.ChallengeComponent(x["goal"], x["ctype"], x["excludes"])
    if c.ctype == "main":
        V.mainChallenges.append(c)
    else:
        V.extraChallenges.append(c)

#Selects a random map to work on
def selectMap():
    #maps from json
    maplist = list(json_data["maps"].values())
    maplist = [m["id"] for m in maplist]

    #filtered maps from txt
    with open(os.path.join(location, "mapfilter.txt")) as f:
        filterlist = f.readlines()
    filterlist = [x.strip() for x in filterlist] 
    
    #filter
    maplist = [x for x in maplist if x not in filterlist]

    #select map, update mapfilter.txt
    m = random.choice(maplist)
    m = next((item for item in list(json_data["maps"].values()) if item['id'] == m), None)
    filterlist.pop(0)
    filterlist.append(m["id"])
    with open(os.path.join(location, "mapfilter.txt"), "w") as f:
        for item in filterlist:
            f.write("%s\n" % item)

    V.map = V.Map(m["id"],m["title"],m["weapons"],m["floors"],m["unique_npcs"],m["civilians"],m["unique_disguises"],m["npc_outfits"])
    if V.map.civilians == False:
        V.npc_types_list.remove("civilian")
    print(V.map.title)

#Selects random challenges (int i) and remove things they exclude
def selectChallenge(i):
    for z in range(i):
        chal = random.choice(V.mainChallenges)
        V.selected.append(chal)
        V.excluded.append(chal.goal)

        for x in chal.excl:
            V.excluded.append(x)

        for x in V.excluded:
            for y in V.mainChallenges:
                if x == y.goal:
                    V.mainChallenges.remove(y)
print("CHALLENGE SELECTED")

#Generates 2-3 challenges
def generateDaily():
    for x in V.selected:
        getattr(F, x.goal)()
    if random.uniform(0, 1) < 0.70 and len(V.selected) < 3:
        F.randExtra()
pass

#Select a number of targets + challenges + map
V.targetCount = random.randint(3,5)
selectMap()
selectChallenge(math.ceil(random.uniform(1, 2.6)))
#Magic happens
generateDaily()

############################## SELENIUM, gets challenge title


try:
    chrome_options = Options()
    chrome_options.set_headless(headless=True)
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', chrome_options=chrome_options)

    driver.get('https://www.ruggenberg.nl/titels.html')
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, 'generate')))
    driver.find_element(By.NAME, 'generate').click()
    titleOptions = driver.find_elements(By.TAG_NAME, 'input')
    del titleOptions[0]
    title = random.choice(titleOptions)
    title = title.get_attribute("value")
    print(title)
    driver.quit()
except Exception as e:
    title = "Error Handler"
    log.write(str(date) + " - " + str(e) + "\n")



############################## IMAGE GENERATION

#Texts to be added
todaytext = 'Weekly Hitman Challenge, ' + str(datetime.datetime.today().strftime('%d %B %Y'))
dailytext = 'Your goal is to create and complete a contract while following this set of rules:'
mapAndTargets = '{} targets in {}'.format(str(V.targetCount),V.map.title)

#Load image, get dimensions
path = os.path.join(location, "res", V.map.id)
file = random.choice(os.listdir(path))
file = os.path.join(path, file)
print(file)
img = Image.open(file)
img = img.filter(ImageFilter.GaussianBlur(4))
imgWidth, imgHeight = img.size
draw = ImageDraw.Draw(img)

#Load font, set size to fit image
font = ImageFont.truetype(os.path.join(location,'res/coolvetica.ttf'), int(imgWidth * 0.025))
ruleTitleFont = ImageFont.truetype(os.path.join(location,'res/coolvetica.ttf'), int(imgWidth * 0.032))
smallFont = ImageFont.truetype(os.path.join(location,'res/coolvetica.ttf'), int(imgWidth * 0.02))
bigFont = ImageFont.truetype(os.path.join(location,'res/coolvetica.ttf'), int(imgWidth * 0.055))

#Draw title
bigFontWidth, bigFontHeight = draw.textsize(title, font=bigFont)
titleOffset = 0.08
#Black outline
draw.text(((imgWidth-bigFontWidth)/2-1, (imgHeight-bigFontHeight)*titleOffset), title, (0,0,0), font=bigFont)
draw.text(((imgWidth-bigFontWidth)/2+1, (imgHeight-bigFontHeight)*titleOffset), title, (0,0,0), font=bigFont)
draw.text(((imgWidth-bigFontWidth)/2, (imgHeight-bigFontHeight)*titleOffset-1), title, (0,0,0), font=bigFont)
draw.text(((imgWidth-bigFontWidth)/2, (imgHeight-bigFontHeight)*titleOffset+1), title, (0,0,0), font=bigFont)
#White text
draw.text(((imgWidth-bigFontWidth)/2, (imgHeight- bigFontHeight)*titleOffset), title, (255,255,255), font=bigFont)

#Rectangle around title
x0 = (imgWidth-bigFontWidth)/2-bigFontWidth*0.06
y0 = (imgHeight-bigFontHeight)*0.08
x1 = (imgWidth+bigFontWidth)/2+bigFontWidth*0.06
y1 = (imgHeight)*0.195
draw.rectangle([x0,
                 y0,
                 x1,
                 y1], 
               None, (255,255,255))

#Draw current date
fontWidth, fontHeight = draw.textsize(todaytext, font=smallFont)
dateOffset = 0.02
#Black outline
draw.text(((imgWidth-fontWidth)/2-1, (imgHeight-fontHeight)*dateOffset), todaytext, (0,0,0), font=smallFont)
draw.text(((imgWidth-fontWidth)/2+1, (imgHeight-fontHeight)*dateOffset), todaytext, (0,0,0), font=smallFont)
draw.text(((imgWidth-fontWidth)/2, (imgHeight-fontHeight)*dateOffset-1), todaytext, (0,0,0), font=smallFont)
draw.text(((imgWidth-fontWidth)/2, (imgHeight-fontHeight)*dateOffset+1), todaytext, (0,0,0), font=smallFont)
#White text
draw.text(((imgWidth-fontWidth)/2, (imgHeight- fontHeight)*dateOffset), todaytext, (255,255,255), font=smallFont)

#Draw daily description
fontWidth, fontHeight = draw.textsize(dailytext, font=smallFont)
dailyOffset = 0.21
#Black outline
draw.text(((imgWidth-fontWidth)/2-1, (imgHeight-fontHeight)*dailyOffset), dailytext, (0,0,0), font=smallFont)
draw.text(((imgWidth-fontWidth)/2+1, (imgHeight-fontHeight)*dailyOffset), dailytext, (0,0,0), font=smallFont)
draw.text(((imgWidth-fontWidth)/2, (imgHeight-fontHeight)*dailyOffset-1), dailytext, (0,0,0), font=smallFont)
draw.text(((imgWidth-fontWidth)/2, (imgHeight-fontHeight)*dailyOffset+1), dailytext, (0,0,0), font=smallFont)
#White text
draw.text(((imgWidth-fontWidth)/2, (imgHeight- fontHeight)*dailyOffset), dailytext, (255,255,255), font=smallFont)

#Draw map and target count
fontWidth, fontHeight = draw.textsize(mapAndTargets, font=font)
mapOffset = 0.27
#Black outline
draw.text(((imgWidth-fontWidth)/2-1, (imgHeight-fontHeight)*mapOffset), mapAndTargets, (0,0,0), font=font)
draw.text(((imgWidth-fontWidth)/2+1, (imgHeight-fontHeight)*mapOffset), mapAndTargets, (0,0,0), font=font)
draw.text(((imgWidth-fontWidth)/2, (imgHeight-fontHeight)*mapOffset-1), mapAndTargets, (0,0,0), font=font)
draw.text(((imgWidth-fontWidth)/2, (imgHeight-fontHeight)*mapOffset+1), mapAndTargets, (0,0,0), font=font)
#White text
draw.text(((imgWidth-fontWidth)/2, (imgHeight- fontHeight)*mapOffset), mapAndTargets, (255,255,255), font=font)


#Draw rule headers
horizontalOffset = imgWidth*0.1
horizontalOffsetDescription = imgWidth*0.12

for i in range(len(V.finalChallenge)):
    fontWidth, fontHeight = draw.textsize(V.finalChallenge[i].title, font=ruleTitleFont)
    offset = fontHeight + mapOffset*imgHeight + imgHeight*(i/(len(V.finalChallenge)+2))
    #Black outline
    draw.text((horizontalOffset-1, offset), V.finalChallenge[i].title, (0,0,0), font=ruleTitleFont)
    draw.text((horizontalOffset+1, offset), V.finalChallenge[i].title, (0,0,0), font=ruleTitleFont)
    draw.text((horizontalOffset, offset-1), V.finalChallenge[i].title, (0,0,0), font=ruleTitleFont)
    draw.text((horizontalOffset, offset+1), V.finalChallenge[i].title, (0,0,0), font=ruleTitleFont)
    #White text
    draw.text((horizontalOffset, offset), V.finalChallenge[i].title, (255,255,255), font=ruleTitleFont)

    titleFontHeight = fontHeight
    fontWidth, fontHeight = draw.textsize(V.finalChallenge[i].line1, font=font)
    offset = titleFontHeight + mapOffset*imgHeight + imgHeight*(i/(len(V.finalChallenge)+2)) + imgHeight*0.07
    #Black outline
    draw.multiline_text((horizontalOffsetDescription-1, offset), V.finalChallenge[i].line1, (0,0,0), font=font)
    draw.multiline_text((horizontalOffsetDescription+1, offset), V.finalChallenge[i].line1, (0,0,0), font=font)
    draw.multiline_text((horizontalOffsetDescription, offset-1), V.finalChallenge[i].line1, (0,0,0), font=font)
    draw.multiline_text((horizontalOffsetDescription, offset+1), V.finalChallenge[i].line1, (0,0,0), font=font)
    #White text
    draw.multiline_text((horizontalOffsetDescription, offset), V.finalChallenge[i].line1, (255,255,255), font=font)

    #Description line 2
    if V.finalChallenge[i].line2 != "":
        titleFontHeight = fontHeight
        fontWidth, fontHeight = draw.textsize(V.finalChallenge[i].line2, font=font)
        offset = titleFontHeight + mapOffset*imgHeight + imgHeight*(i/(len(V.finalChallenge)+2)) + imgHeight*0.07 + fontHeight*1.15
        #Black outline
        draw.multiline_text((horizontalOffsetDescription-1, offset), V.finalChallenge[i].line2, (0,0,0), font=font)
        draw.multiline_text((horizontalOffsetDescription+1, offset), V.finalChallenge[i].line2, (0,0,0), font=font)
        draw.multiline_text((horizontalOffsetDescription, offset-1), V.finalChallenge[i].line2, (0,0,0), font=font)
        draw.multiline_text((horizontalOffsetDescription, offset+1), V.finalChallenge[i].line2, (0,0,0), font=font)
        #White text
        draw.multiline_text((horizontalOffsetDescription, offset), V.finalChallenge[i].line2, (255,255,255), font=font)


#Save img
img.save(os.path.join(location, 'challenge.jpg'))


################################### TWITTER

try:
    twitterApi = twitter.Api(consumer_key=config['TWITTER']['consumer_key'],
                      consumer_secret=config['TWITTER']['consumer_secret'],
                      access_token_key=config['TWITTER']['access_token_key'],
                      access_token_secret=config['TWITTER']['access_token_secret'])

    twitterApi.PostUpdate('Weekly Hitman Challenge - ' + title, os.path.join(location, "challenge.jpg"))
except Exception as e:
    log.write(str(date) + " - " + str(e) + "\n")


#Close error log
log.close()
