# kamehouse-feed

カードショップカメハウスの商品フィード自動更新リポジトリ。

- 毎朝9時(JST)にClaude定期タスク「kamehouse-feed-update」がおちゃのこネットの公開フィード(gfeed.xml)を取得し、
  在庫あり商品のみの9列CSV `kamehouse_products_instock.csv` に変換してこのリポジトリにpushする。
- DFOマネージャー(メルカリ広告用フィード生成)が毎日11:05にこのCSVのraw URLを自動取得する。
  - 取得URL: https://raw.githubusercontent.com/ryo0822ushi/kamehouse-feed/main/kamehouse_products_instock.csv
- 掲載しているのはショップサイトで公開済みの商品情報のみ。
- 変換失敗時(在庫あり100件未満・取得エラー等)はpushせず前回の正常なCSVが維持され、Slack DMで牛島涼に通知される。

**止め方**: 定期タスク「kamehouse-feed-update」を削除する
（またはDFOマネージャー側の取得方法を手動アップロードに戻す）。
