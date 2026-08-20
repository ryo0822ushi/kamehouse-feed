#!/usr/bin/env python3
"""gfeed.xml (おちゃのこGoogleショッピングフィード) → DFOマネージャー入力用9列CSV変換

カードショップカメハウスのメルカリ広告フィード自動更新用。
在庫あり(in stock)の商品だけを抽出し、DFOマネージャー(c10124)が
取り込んでいる既存フォーマットと同一の9列CSV(UTF-8 BOM)を出力する。
"""
import csv, re, sys
import xml.etree.ElementTree as ET

G = '{http://base.google.com/ns/1.0}'
UTM = 'utm_source=mercari&utm_medium=cpc&utm_campaign=infeed_test'
MIN_ROWS = 100  # これ未満ならフィード源の異常とみなし失敗させる(前回の正常ファイルを維持するため)

def text(item, tag, ns=True):
    el = item.find((G if ns else '') + tag)
    return (el.text or '') if el is not None else ''

def flatten(s):
    return re.sub(r'\s+', ' ', s).strip()

def convert(src, dst):
    root = ET.parse(src).getroot()
    rows, skipped = [], 0
    for item in root.iter('item'):
        if text(item, 'availability') != 'in stock':
            skipped += 1
            continue
        link = flatten(text(item, 'link', ns=False))
        rows.append([
            flatten(text(item, 'id')),
            flatten(text(item, 'title', ns=False)),
            flatten(text(item, 'description', ns=False))[:1000],
            flatten(text(item, 'product_type')),
            link,
            link + ('&' if '?' in link else '?') + UTM,
            flatten(text(item, 'image_link')),
            flatten(text(item, 'price')).replace(' JPY', ''),
            'あり',
        ])
    if len(rows) < MIN_ROWS:
        print(f'ERROR: only {len(rows)} in-stock rows (< {MIN_ROWS}) — feed source looks broken, aborting', file=sys.stderr)
        sys.exit(1)
    with open(dst, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['商品ID','商品名','商品説明','カテゴリ','商品URL','計測用URL(UTM付き)','画像URL','販売価格(税込)','在庫'])
        w.writerows(rows)
    print(f'wrote {dst}: {len(rows)} in-stock rows (skipped {skipped} out-of-stock)')

if __name__ == '__main__':
    convert(sys.argv[1] if len(sys.argv) > 1 else 'gfeed.xml',
            sys.argv[2] if len(sys.argv) > 2 else 'kamehouse_products_instock.csv')
