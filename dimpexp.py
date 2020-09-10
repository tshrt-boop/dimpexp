#! /usr/bin/python3
"""簡易的なDynamoDBのインポート・エクスポートツール

DynamoDBのテーブルを指定して、全データのエクスポート・インポートができます。

python dimpexp.py export -t table_name -o dump.json
python dimpexp.py import -t table_name -i dump.json
"""
import boto3
import json
from decimal import Decimal
import argparse


def import_dynamodb(table, input, **extras):
    """インポート

    指定したテーブルにデータをインポートします。
    Args:
        table: テーブル名
        input: 入力ファイル名
    """

    file_name = input
    try:
        file = open(file_name, encoding='unicode-escape')
        data = file.read()
    except Exception as e:
        print(e)
    finally:
        file.close()
    json_data = json.loads(data, strict=False, parse_float=Decimal)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table)

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
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table)
    res = table.scan()
    file_name = output
    try:
        file = open(file_name, 'w')
        file.write(json.dumps(res['Items'], default=decimal_default_proc))
    except Exception as e:
        print(e)
    finally:
        file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DynamoDB export/import')
    subparsers = parser.add_subparsers()

    parser_add = subparsers.add_parser('export', help='see `export -h`')
    parser_add.add_argument(
        '-t', '--table', help='export table name', required=True)
    parser_add.add_argument(
        '-o', '--output', help='export file name', required=True)
    parser_add.set_defaults(handler=export_dynamodb)

    parser_add = subparsers.add_parser('import', help='see `import -h`')
    parser_add.add_argument(
        '-t', '--table', help='export table name', required=True)
    parser_add.add_argument(
        '-i', '--input', help='input file name', required=True)
    parser_add.set_defaults(handler=import_dynamodb)

    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(**vars(args))
    else:
        # 未知のサブコマンドの場合はヘルプを表示
        parser.print_help()
