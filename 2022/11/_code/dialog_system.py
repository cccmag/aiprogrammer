#!/usr/bin/env python3
"""AI Dialog System Demo — Eliza, retrieval, seq2seq, state tracking"""

import re
import random
from collections import defaultdict


# ── 1. Eliza-style pattern matching ──────────────────────────────

ELIZA_PATTERNS = [
    (r'.*我感到(.+)',        '你感到{m1}，能多說說嗎？'),
    (r'.*我(覺得|認為)(.+)',  '你{op}{topic}，是什麼讓你有這種想法？'),
    (r'.*我需要(.+)',         '如果你可以得到{m1}，你認為會怎樣？'),
    (r'.*因為(.+)',           '原來如此，{m1}讓你這麼想嗎？'),
    (r'.*你好',               '你好！我是 Eliza，有什麼可以幫你的嗎？'),
    (r'.*我的(.+)是(.+)',     '你的{k}是{v}，能多說一些嗎？'),
    (r'.*\?',                '你覺得呢？'),
    (r'.*(是|對|嗯).*',      '我明白了，繼續說吧。'),
    (r'.*再見',              '再見！謝謝你今天的談話。'),
]

ELIZA_FALLBACK = [
    '嗯…能多說一些嗎？',
    '這很有趣，繼續說下去。',
    '我明白了，還有其他的嗎？',
    '請告訴我更多。',
    '為什麼你會這麼說呢？',
]


def eliza_respond(text: str) -> str:
    for pattern, template in ELIZA_PATTERNS:
        m = re.match(pattern, text)
        if m:
            groups = m.groups()
            try:
                return template.format(m1=groups[0] if len(groups) > 0 else '',
                                       op=groups[0] if len(groups) > 1 else '',
                                       topic=groups[1] if len(groups) > 1 else '',
                                       k=groups[0] if len(groups) > 1 else '',
                                       v=groups[1] if len(groups) > 1 else '')
            except (IndexError, KeyError):
                return random.choice(ELIZA_FALLBACK)
    return random.choice(ELIZA_FALLBACK)


# ── 2. Retrieval-based response ─────────────────────────────────

RETRIEVAL_KB = {
    '天氣':       '今天天氣晴朗，高溫 28°C，午後有局部雷陣雨。',
    '股價':       '台積電今日收盤價 580 元，漲幅 1.2%。',
    '新聞':       '今天頭條：AI 對話系統突破百億美元市場。',
    '你好':       '你好！我是客服機器人，請描述您的需求。',
    '預約':       '請提供您的姓名和預約時間，我為您登記。',
    '地址':       '我們的地址是台北市信義區智慧路 100 號。',
    '電話':       '客服專線：0800-123-456（週一至週五 9:00-18:00）。',
}


def retrieval_respond(text: str) -> str:
    for key, response in RETRIEVAL_KB.items():
        if key in text:
            return response
    return '抱歉，我沒有關於這個問題的資訊。請聯繫人工客服。'


# ── 3. Seq2Seq simulation (rule-based proxy) ───────────────────

SEQ2SEQ_KB = {
    '你叫什麼名字':   '我是 chatbot，由序列到序列模型生成。',
    '你幾歲':         '我的模型訓練於 2022 年。',
    '你好嗎':         '我很好，謝謝你的關心！',
    '你喜歡什麼':     '我喜歡學習新的對話模式。',
    '你會做什麼':     '我可以回答問題、進行對話和協助任務。',
}


def seq2seq_respond(text: str) -> str:
    return SEQ2SEQ_KB.get(text.strip(),
                          '【seq2seq】生成回覆：我不太理解您的意思。')


# ── 4. Dialog State Tracking ───────────────────────────────────

class DialogState:
    def __init__(self):
        self.slots = {}
        self.history = []
        self.turn = 0

    def update(self, user_input: str, system_response: str):
        self.turn += 1
        self.history.append((user_input, system_response))
        # Slot filling
        m = re.search(r'我(?:叫|是)(.+?)(?:，|。|$)', user_input)
        if m:
            self.slots['name'] = m.group(1).strip()
        m = re.search(r'(\d{3,4})', user_input)
        if m:
            self.slots['phone'] = m.group(1)
        if '預約' in user_input or '訂位' in user_input:
            self.slots['intent'] = 'booking'
        if '查詢' in user_input or '查' in user_input:
            self.slots['intent'] = 'inquiry'

    def is_complete(self) -> bool:
        return 'name' in self.slots and 'intent' in self.slots

    def summary(self) -> str:
        return f'狀態：{dict(self.slots)}，已進行 {self.turn} 輪'


# ── Demo ────────────────────────────────────────────────────────

def demo():
    print('=== AI 對話系統綜合展示 ===')
    print()

    # 1. Eliza
    print('─' * 40)
    print('1. Eliza 風格對話')
    print('─' * 40)
    for inp in ['你好', '我感到難過', '因為今天下雨', '我需要幫助']:
        print(f'  使用者: {inp}')
        print(f'  Eliza : {eliza_respond(inp)}')
    print()

    # 2. Retrieval
    print('─' * 40)
    print('2. 檢索式回覆')
    print('─' * 40)
    for inp in ['今天天氣如何？', '台積電股價多少？', '我想預約']:
        print(f'  使用者: {inp}')
        print(f'  系統  : {retrieval_respond(inp)}')
    print()

    # 3. Seq2Seq
    print('─' * 40)
    print('3. Seq2Seq 模擬')
    print('─' * 40)
    for inp in ['你叫什麼名字', '你會做什麼']:
        print(f'  使用者: {inp}')
        print(f'  系統  : {seq2seq_respond(inp)}')
    print()

    # 4. State tracking
    print('─' * 40)
    print('4. 對話狀態追蹤')
    print('─' * 40)
    ds = DialogState()
    exchanges = [
        ('你好，我想預約今天下午', '好的，請問您的姓名與電話？'),
        ('我叫小明，電話 0912', '已為您登記預約，下午 2:00 準時。'),
    ]
    for user, sys in exchanges:
        ds.update(user, sys)
        print(f'  使用者: {user}')
        print(f'  系統  : {sys}')
    print(f'  摘要  : {ds.summary()}')
    print()

    print('=' * 40)
    print('展示結束。此腳本展示了四種對話系統技術：')
    print('Eliza 模式匹配、檢索式回覆、Seq2Seq 生成、狀態追蹤。')


if __name__ == '__main__':
    demo()
