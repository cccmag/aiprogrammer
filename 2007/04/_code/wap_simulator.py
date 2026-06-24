#!/usr/bin/env python3
"""WAP 瀏覽器模擬器 - WML 解析器"""

from html.parser import HTMLParser
from urllib.parse import urljoin, parse_qs
import xml.etree.ElementTree as ET
import re

class WMLParser:
    def __init__(self):
        self.cards = {}
        self.current_card = None
        self.content = []
        self.navigation = []

    def parse(self, wml_content):
        try:
            root = ET.fromstring(wml_content)
            wml = root

            for card in wml.findall('.//card'):
                card_id = card.get('id', '')
                card_title = card.get('title', '')
                card_content = self._parse_card_content(card)
                self.cards[card_id] = {
                    'id': card_id,
                    'title': card_title,
                    'content': card_content,
                    'links': self._extract_links(card)
                }

            return True
        except ET.ParseError as e:
            print(f'XML 解析錯誤: {e}')
            return False

    def _parse_card_content(self, card):
        lines = []
        for elem in card.iter():
            if elem.tag == 'p':
                for text in elem.itertext():
                    if text.strip():
                        lines.append(text.strip())
            elif elem.tag == 'br':
                lines.append('')
            elif elem.tag == 'do':
                label = elem.get('label', '')
                lines.append(f'[{label}]')
        return '\n'.join(lines)

    def _extract_links(self, card):
        links = []
        for a in card.findall('.//a'):
            href = a.get('href', '')
            text = ''.join(a.itertext()).strip()
            links.append({'href': href, 'text': text})
        return links

    def get_card(self, card_id):
        return self.cards.get(card_id)

    def get_first_card(self):
        if self.cards:
            return list(self.cards.values())[0]
        return None

class WAPBrowser:
    def __init__(self):
        self.parser = WMLParser()
        self.current_card_id = None
        self.history = []
        self.screen_width = 20

    def load_wml(self, wml_content):
        self.parser = WMLParser()
        if self.parser.parse(wml_content):
            first_card = self.parser.get_first_card()
            if first_card:
                self.current_card_id = first_card['id']
                self.history = [self.current_card_id]
            return True
        return False

    def navigate_to(self, card_id):
        if card_id in self.parser.cards:
            self.history.append(self.current_card_id)
            self.current_card_id = card_id
            return True
        return False

    def go_back(self):
        if len(self.history) > 1:
            self.history.pop()
            self.current_card_id = self.history[-1]
            return True
        return False

    def render_current_card(self):
        card = self.parser.get_card(self.current_card_id)
        if not card:
            return None

        lines = []
        lines.append('─' * self.screen_width)
        lines.append(f'  {card["title"]}')
        lines.append('─' * self.screen_width)

        for line in card['content'].split('\n'):
            wrapped = self._wrap_text(line, self.screen_width - 2)
            lines.extend(wrapped)

        if card['links']:
            lines.append('')
            for link in card['links']:
                lines.append(f'  → {link["text"]}')

        lines.append('─' * self.screen_width)
        lines.append('  [返回] [選單]')

        return '\n'.join(lines)

    def _wrap_text(self, text, width):
        words = text.split()
        lines = []
        current_line = ''

        for word in words:
            if not current_line:
                current_line = word
            elif len(current_line) + 1 + len(word) <= width:
                current_line += ' ' + word
            else:
                lines.append('  ' + current_line)
                current_line = word

        if current_line:
            lines.append('  ' + current_line)

        return lines or ['  ']

def demo():
    print('=' * 30)
    print('  WAP 瀏覽器模擬器 v1.0')
    print('=' * 30)
    print()

    browser = WAPBrowser()

    sample_wml = '''<?xml version="1.0"?>
<!DOCTYPE wml PUBLIC "-//WAPFORUM//DTD WML 1.1//EN"
"http://www.wapforum.org/DTD/wml_1.1.xml">
<wml>
  <card id="home" title="手機入口">
    <p mode="nowrap">
      歡迎使用手機入口<br/>
      <a href="#news">新聞</a><br/>
      <a href="#weather">天氣</a><br/>
      <a href="#stock">股票</a>
    </p>
  </card>

  <card id="news" title="最新新聞">
    <p>
      1. iPhone 六月上市<br/>
      2. Google 發布 Android<br/>
      3. Web 2.0 持續熱門<br/>
      <a href="#news1">詳情</a>
    </p>
    <do type="prev" label="返回">
      <prev/>
    </do>
  </card>

  <card id="weather" title="天氣預報">
    <p>
      今天：晴朗 26°C<br/>
      明天：多雲 24°C<br/>
      後天：下雨 20°C
    </p>
    <do type="prev" label="返回">
      <prev/>
    </do>
  </card>

  <card id="stock" title="股票報價">
    <p>
      加權指數：9500<br/>
      上漲 50 點<br/>
      <a href="#home">回首頁</a>
    </p>
    <do type="prev" label="返回">
      <prev/>
    </do>
  </card>

  <card id="news1" title="iPhone 新聞">
    <p>
      蘋果宣佈 iPhone 將於<br/>
      六月正式上市，配備<br/>
      Safari 瀏覽器...
    </p>
    <do type="prev" label="返回">
      <prev/>
    </do>
  </card>
</wml>'''

    if browser.load_wml(sample_wml):
        print('首頁：')
        print(browser.render_current_card())
        print()

        print('導航到「天氣」頁面：')
        browser.navigate_to('weather')
        print(browser.render_current_card())
        print()

        print('返回上一頁：')
        browser.go_back()
        print(browser.render_current_card())
        print()

        print('導航到「新聞」頁面：')
        browser.navigate_to('news')
        print(browser.render_current_card())
    else:
        print('WML 解析失敗')

if __name__ == '__main__':
    demo()