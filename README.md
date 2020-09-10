dimpexp
====

簡易的なDynamoDBのインポート・エクスポートツール

## Description

DynamoDBのテーブルを指定して、全データのエクスポート・インポートができます。  
エラー処理は十分ではないので、実行時には十分な読み込み・書き込みキャパシティユニットを確保してください。

## Requirement

- Python 3.8.x
- pipenv
  - [インストール](https://pipenv-ja.readthedocs.io/ja/translate-ja/install.html#pragmatic-installation-of-pipenv)

## Usage

```
pipenv shell
# export
python dimpexp.py export -t table_name -o dump.json
# import
python dimpexp.py import -t table_name -i dump.json
```

プロファイルの指定

```
python dimpexp.py -p profile_name export -t table_name -o dump.json
```

サブコマンド(export, import)の前に指定する必要があります。

## Install

```
git clone https://github.com/tshrt-boop/dimpexp.git
cd dimpexp
pipenv install
```

## Todo



## Licence

[MIT](https://ja.osdn.net/projects/opensource/wiki/licenses%2FMIT_license)

## Author

[@tshrt-boop](https://github.com/tshrt-boop)

