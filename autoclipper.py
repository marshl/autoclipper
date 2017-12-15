import time
import re
import numpy as np

from selenium import webdriver

from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

baseurl = 'http://www.decisionproblem.com/paperclips/index2.html'

xpath = {
    'makepaperclipButton': '//*[@id="btnMakePaperclip"]',
    'fundsText': '//*[@id="funds"]',
    'unsoldClipsText': '//*[@id="unsoldClips"]'
}

mydriver = webdriver.Chrome()
mydriver.get(baseurl)
# mydriver.maximize_window()



UPDATE_INTERVAL = 0.1
TREND_LENGTH = 2 / UPDATE_INTERVAL


class PaperClipGame:
    def __init__(self):
        self.unsold_clips = 0
        self.available_funds = 0
        self.paperclip_trend = 0.0
        self.wire_inches = 0

        self.paperclips_over_time = list()

    def make_paperclip(self):
        mydriver.find_element_by_xpath(xpath['makepaperclipButton']).click()

    def lower_price(self):
        print('Lowering price')
        mydriver.find_element_by_id('btnLowerPrice').click()

    def raise_price(self):
        print('Raising price')
        mydriver.find_element_by_id('btnRaisePrice').click()

    def buy_wire(self):
        print('Buying wire')
        mydriver.find_element_by_id('btnBuyWire').click()

    def text_to_number(self, text):
        return int(re.sub('\D', '', text))

    def can_make_auto_clippers(self):
        return self.get_auto_clipper_btn().is_enabled()

    def buy_auto_clipper(self):
        self.get_auto_clipper_btn().click()

    def get_auto_clipper_btn(self):
        print('Buying auto-clipper')
        return mydriver.find_element_by_id('btnMakeClipper')

    def get_stats(self):
        self.available_funds = float(mydriver.find_element_by_id('funds').text)
        self.unsold_clips = int(mydriver.find_element_by_id('unsoldClips').text)
        self.wire_inches = self.text_to_number(mydriver.find_element_by_id('wire').text)

        self.paperclips_over_time.append(self.unsold_clips)
        if len(self.paperclips_over_time) > TREND_LENGTH:
            self.paperclips_over_time.pop(0)

        x = np.arange(0, len(self.paperclips_over_time))
        y = np.array(self.paperclips_over_time)
        z = np.polyfit(x, y, 1)
        self.paperclip_trend = z[0]

        print(f'Funds: {self.available_funds} UnsoldClips: {self.unsold_clips} PCTrend: {self.paperclip_trend}')


game = PaperClipGame()

step = 0

while (True):
    time.sleep(UPDATE_INTERVAL)
    step += 1
    game.get_stats()
    game.make_paperclip()

    if step % (5 / UPDATE_INTERVAL) == 0:
        if game.paperclip_trend > 0.1:
            game.lower_price()
        else:
            game.raise_price()

    if game.wire_inches == 0:
        game.buy_wire()

    if game.can_make_auto_clippers():
        game.buy_auto_clipper()

# mydriver.close()
