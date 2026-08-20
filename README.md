# kamehouse-feed

カードショップカメハウスの商品フィード自動更新リポジトリ。

- 毎朝9時(JST)にGitHub Actionsがおちゃのこネットの公開フィード(gfeed.xml)を取得し、
  在庫あり商品のみの9列CSV `kamehouse_products_instock.csv` に変換してコミットする。
- DFOマネージャー(メルカリ広告用フィード生成)が毎日11:05にこのCSVのraw URLを自動取得する。
- 掲載しているのはショップサイトで公開済みの商品情報のみ。

**止め方**: このリポジトリの Actions タブで update-feed ワークフローを Disable する
（またはDFOマネージャー側の取得方法を手動アップロードに戻す）。
