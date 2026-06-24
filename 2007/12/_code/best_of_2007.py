#!/usr/bin/env python3
"""2007 年度精選程式回顧"""

def demo():
    print('2007 年度精選開源專案')
    print('=' * 40)

    projects = [
        {
            'name': 'Git 1.5',
            'category': '版本控制',
            'description': '分散式版本控制系統'
        },
        {
            'name': 'jQuery 1.1',
            'category': 'JavaScript 框架',
            'description': '簡潔的 DOM 操作庫'
        },
        {
            'name': 'Django 0.96',
            'category': 'Web 框架',
            'description': 'Python Web 開發框架'
        },
        {
            'name': 'Hadoop',
            'category': '大數據',
            'description': '分散式資料處理'
        },
        {
            'name': 'Ruby on Rails',
            'category': 'Web 框架',
            'description': '敏捷 Web 開發框架'
        }
    ]

    print('\n精選專案：')
    for i, p in enumerate(projects, 1):
        print(f'\n{i}. {p["name"]} ({p["category"]})')
        print(f'   {p["description"]}')

    print('\n\n2007 年技術趨勢：')
    trends = [
        '雲端運算興起',
        '社交網路爆發',
        '行動 Web 起飛',
        '開放平台流行'
    ]
    for t in trends:
        print(f'  - {t}')

if __name__ == '__main__':
    demo()