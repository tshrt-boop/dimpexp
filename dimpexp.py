#! /usr/bin/python3
"""簡易的なDynamoDBのインポート・エクスポートツール

DynamoDBのテーブルを指定して、全データのエクスポート・インポートができます。

python dimpexp.py export -t table_name -o dump.json
python dimpexp.py import -t table_name -i dump.json
"""
import boto3
from boto3.session import Session
import json
from decimal import Decimal
import argparse


def get_table(table, profile):
    """テーブルオブジェクトの取得
    """
    session = Session(profile_name=profile)
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(table)
    return table


def import_dynamodb(table, input, **extras):
    """インポート

    指定したテーブルにデータをインポートします。
    Args:
        table: テーブル名
        input: 入力ファイル名
    """

    try:
        file = open(input, encoding='unicode-escape')
        data = file.read()
    except Exception as e:
        print(e)
    finally:
        file.close()
    json_data = json.loads(data, strict=False, parse_float=Decimal)

    table = get_table(table, extras['profile'])
    with table.batch_writer() as batch:
        for i, (record) in enumerate(json_data):
            print(record)
            batch.put_item(Item=record)


def decimal_default_proc(obj):
    """JSON文字列変換時の型変換
    """
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def export_dynamodb(table, output, **extras):
    """エクスポート

    指定したテーブルからデータをエクスポートします。
    Args:
        table: テーブル名
        output: 出力ファイル名
    """

    table = get_table(table, extras['profile'])
    res = table.scan()
    try:
        file = open(output, 'w')
        file.write(json.dumps(res['Items'], default=decimal_default_proc))
    except Exception as e:
        print(e)
    finally:
        file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DynamoDB export/import')
    subparsers = parser.add_subparsers()

    # エクスポートの実行時引数設定
    parser_add = subparsers.add_parser('export', help='see `export -h`')
    parser_add.add_argument(
        '-t', '--table', help='export table name', required=True)
    parser_add.add_argument(
        '-o', '--output', help='export file name', required=True)
    parser_add.set_defaults(handler=export_dynamodb)

    # インポートの実行時引数設定
    parser_add = subparsers.add_parser('import', help='see `import -h`')
    parser_add.add_argument(
        '-t', '--table', help='export table name', required=True)
    parser_add.add_argument(
        '-i', '--input', help='input file name', required=True)
    parser_add.set_defaults(handler=import_dynamodb)

    # プロファイル名の実行時引数設定
    parser.add_argument('-p', '--profile',
                        help='profile name', default='default')

    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(**vars(args))
    else:
        # 未知のサブコマンドの場合はヘルプを表示
        parser.print_help()
