import re
import json
import pymssql
from re import RegexFlag

# ★★★TiDBのDB初期化スクリプトの格納場所
_sql_script_path = r'<パース>\ebs-mysql.sql'
# ★★★出力場所
_output_table_path = r'<パース>\target_table_list.txt'

# 取得元のSQL　Server情報
# ★★★実行HOSTのIPはSQLデータベースのファイアウォールに設定必要
_conn = pymssql.connect(
    server='saas-core.database.windows.net',
    user='saas',
    password='eh0iSL-s3xi2amoL',
    database='20240109_EBS',
    as_dict=True
) 

# 登録日時、更新日時のNULL値があるかおうかのチェック
def _check_update_col_contains_null(table_info: dict) -> bool:
    cursor = _conn.cursor()
    cursor.execute(f"SELECT COUNT(1) AS EXIST_NULL FROM {table_info['name']} WHERE {table_info['create']} IS NULL OR {table_info['update']} IS NULL")
    result = cursor.fetchone()
    cursor.close()
    return result['EXIST_NULL'] > 0

# 指定テーブルの主キー取得
def _get_primary_keys(table_info: dict) -> list:
    cursor = _conn.cursor()
    # ★★★TABLE_SCHEMAは「dbo」以外の場合変更必要
    sql = f"""
SELECT COLUMN_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE OBJECTPROPERTY(OBJECT_ID(CONSTRAINT_SCHEMA + '.' + QUOTENAME(CONSTRAINT_NAME)), 'IsPrimaryKey') = 1
AND TABLE_NAME = '{table_info['name']}' AND TABLE_SCHEMA = 'dbo'
"""
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    if result:
        return [row['COLUMN_NAME'] for row in result]
    else:
        return []

# テーブル一覧作成(主キー、更新日時項目などの情報)
def _get_table_list_with_update_datetime():
    tabel_start = False
    CREATE_KEYS = ["REC_ENT_DATE", "TOROKUYMD", "CREATE_DATE"]
    UPDATE_KEYS = ["REC_EDT_DATE", "KOSHINYMD", "UPDATE_DATE"]
    table_list = list()
    table_info = dict()

    with open(_sql_script_path, mode='r', encoding='utf-8') as fp:
        for line in fp:
            if re.match(r'CREATE\s+TABLE\s+(.+)\s+\(', line, flags=RegexFlag.IGNORECASE):
                tabel_start = True
                table_info = dict(name=re.match(r'CREATE\s+TABLE\s+(.+)\s+\(', line, flags=RegexFlag.IGNORECASE).group(1), create="", update="", primary=list(), can_diff=False)
                table_info['primary'] = _get_primary_keys(table_info)
            elif tabel_start:
                if line.upper().count(' DATE') > 0:
                    col_name = line.upper().strip().split(' ')[0]
                    if col_name in CREATE_KEYS:
                        table_info['create'] = col_name
                    elif col_name in UPDATE_KEYS:
                        table_info['update'] = col_name

                if line.count(",") < 1 and line.count('--') < 1:
                    tabel_start = False
                    table_list.append(table_info)
                    if len(table_info['primary']) > 0 and len(table_info['update']) > 0 and not _check_update_col_contains_null(table_info):
                        table_info['can_diff'] = True
                    
                    if len(table_list) % 5 == 0:
                        print(f"Completed {len(table_list)}, Please waiting...")

    table_list.sort(key=lambda x: x['create'])
    print(len(table_list))
    with open(_output_table_path, 'w', encoding='utf-8', newline='') as wfp:
        wfp.write(json.dumps(table_list, indent=2))

if __name__ == '__main__':
    _get_table_list_with_update_datetime()
    _conn.close()
