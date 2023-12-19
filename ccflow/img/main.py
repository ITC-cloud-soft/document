# 1. execute pip install
import os
import sys
import json

import csv
from datetime import datetime, timedelta


# 打开或创建文件
def open_or_create_file(file_path, mode):
    if os.path.isfile(file_path):
        return open(file_path, mode, newline='\n')
    else:
        return open(file_path, "w")


out_path1 = os.path.join(os.getcwd(), '/opt/csvdata/test')
print("当前文件夹路径:", out_path1)
ts1 = open_or_create_file(os.path.join(out_path1, "ccflow9.tt_wf_order_number.csv"), "a")
nd1track01 = open_or_create_file(os.path.join(out_path1, "ccflow9.nd1track.csv"), "a")
ts3 = open_or_create_file(os.path.join(out_path1, "ccflow9.tt_wf_merchandise_plan.csv"), "a")
ts22 = open_or_create_file(os.path.join(out_path1, "ccflow9.nd5track.csv"), "a")
ts23 = open_or_create_file(os.path.join(out_path1, "ccflow9.tt_wf_arrival_returns.csv"), "a")
ts32 = open_or_create_file(os.path.join(out_path1, "ccflow9.nd7track.csv"), "a")
ts33 = open_or_create_file(os.path.join(out_path1, "ccflow9.tt_wf_stock_adjustment.csv"), "a")
ts4 = open_or_create_file(os.path.join(out_path1, "ccflow9.wf_generworkerlist.csv"), "a")
ts5 = open_or_create_file(os.path.join(out_path1, "ccflow9.wf_generworkflow.csv"), "a")


# 商品計画申請
def create_commodity_csv(total, order_id, pk, work_id):
    # 打开或创建文件函数使用示例

    int_ordernum1 = int(order_id[8:-6])
    # 商品計画申請 id
    item_OID = work_id
    MyPK1 = pk
    # 打开文件后的操作
    for i in range(1, total + 1):
        item_OID += 1
        int_ordernum1 += 1
        item_ordernum1 = "MEP2023" + str(int_ordernum1)
        MyPK1 += 1

        # tt_wf_order_number的数据写入
        line = f"'{item_OID}','001','{datetime.now().strftime('%Y%m%d')}','{item_ordernum1}','{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}','0543956','',''"
        ts1.writelines(line + '\n')

        # nd1track的数据写入
        item_frmb = {
            "ShenQingRen": "真洲句 優祈音",
            "MyNum": "1",
            "CDT": "2023-10-04 14:30",
            "ShenQingRiJi": "2023-10-02",
            "ShenQingRenBuMen": "ＤＸシステム開発Ｇ",
            "FK_DeptText": "ＤＸシステム開発Ｇ",
            "RDT": "2023-10-04 14:30",
            "Rec": "0543956",
            "Title": "ＤＸシステム開発Ｇ-0543956,真洲句 優祈音は2023-10-05 17:22で開始.",
            "OID": item_OID,
            "FK_Dept": "11637",
            "Emps": "0543956",
            "FID": "0",
            "FK_NY": "2023-10",
            "EndJSON": "0",
        }

        item_frmb_str = json.dumps(item_frmb, ensure_ascii=False)
        line = f"'{MyPK1}','1','発送','0',{item_OID},'101','新規申請','102','上司承認','0543956','真洲句 優祈音','0220320','駄御井 進','{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}','0','','','@SendNode=101','(0543956,真洲句 優祈音)','{item_frmb_str}'"
        nd1track01.writelines(line + "\n")

        # tt_wf_merchandise_plan的数据写入
        item_summry = {
            "AgentMode": "0",
            "AutoApprovalMode": "N",
            "content": [
                {"value": "高田　優祈音", "name": "従業員氏名"},
                {"value": "0543956", "name": "発送者"},
                {"value": "MEP2023", "name": "No"},
                {"value": "0543956", "name": "更新者"},
                {"value": "0003", "name": "申請部門"},
                {"value": "発送", "name": "進行ステータス"},
            ],
        }
        item_summry_str = json.dumps(item_summry, ensure_ascii=False)
        now = datetime.now()
        formatted_now = now.strftime('%Y-%m-%d %H:%M:%S')
        formatted_now_short = now.strftime('%Y-%m-%d %H:%M')

        line = (
            f"'{item_OID}','イオンアイビス（株）','ＤＸシステム開発Ｇ','0543956','高田　優祈音',"
            f"'商品計画テスト（王）{i}','','','','{item_summry_str}','{formatted_now}','0543956',"
            f"'{formatted_now}','0','','102','0','@0543956,真洲句 優祈音@','真洲句 優祈音',"
            f"'2023-10-06','ＤＸシステム開発Ｇ','{formatted_now}','0','{formatted_now}','0543956',"
            f"'0543956','1','0','','','','','','','',"
            f"'{formatted_now_short}','102','{formatted_now_short}','0','0543956','0543956','2023-10'"
        )

        ts3.writelines(line + "\n")

        # wf_generworkerlistのデータを書き込む
        current_datetime = datetime.now()
        new_datetime = current_datetime + timedelta(days=1)
        dd = new_datetime.strftime('%Y-%m-%d %H:%M:%S')

        line = f"'{item_OID}','0220320','102','0','駄御井 進','上司承認','001','39510','{dd}','{dd}','{dd}','{dd}','1','0','0','0','0543956,真洲句 優祈音','1','0','','','0','','','@FK_DeptT=デジタルＳ本部長'"
        ts4.writelines(line + "\n")

        line = f"'{item_OID}','0543956','101','0','真洲句 優祈音','新規申請','001','11637','無'," \
               f"'{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'," \
               f"'{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}','{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},''1','0','1','0','','1','0','','','0','','',''"
        ts4.writelines(line + "\n")

        # wf_generworkflow的数据写入
        current_datetime = datetime.now()
        new_datetime = current_datetime + timedelta(days=1)
        dd = new_datetime.strftime('%Y-%m-%d %H:%M:%S')

        item_01 = f"ＤＸシステム開発Ｇ-0543956,真洲句 優祈音は{datetime.now().strftime('%Y-%m-%d %H:%M')}で開始."
        item_02 = f"@LastTruckID={item_ordernum1}"

        line = (
            f"'{item_OID}','0','102','','001','商品計画申請','{item_01}','0','2','0543956',"
            f"'真洲句 優祈音','0543956','{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}',"
            f"'{dd}','102','上司承認','11637','ＤＸシステム開発Ｇ','1',"
            f"'{dd}','','','','0','0','0','','','','','',"
            f"'0220320,駄御井進;',1,'0','{item_02}','@0543956,真洲句 優祈音@','','2023-10',"
            f"'0','0','0','','',''"
        )
        ts5.writelines(line + '\n')


# 入荷返品申請
def create_chargeback_csv(total, chargeback_order_id, chargeback_pk, work_id):
    # Initialize variables ex: chargeback_order_id ALRT202350000002
    int_ordernum2 = int(chargeback_order_id[8:-6])
    MyPK2 = chargeback_pk
    item_OID = work_id

    writer1 = ts1
    writer2 = ts22
    writer3 = ts23
    writer4 = ts4
    writer5 = ts5

    for i in range(1, total + 1):
        item_OID += 1
        int_ordernum2 += 1
        MyPK2 += 1
        item_ordernum2 = f"ALRT2023{int_ordernum2}"

        # 1. tt_wf_order_number
        line = f"'{item_OID}','005','{datetime.now().strftime('%Y%m%d')}','{item_ordernum2}','{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}','0543956','',''"
        writer1.writelines(line + '\n')

        # 2. nd5track
        item_frmb = (f'{{"ShenQingRen": "真洲句 優祈音", "MyNum": 1, "CDT": "2023-10-04 14:38", "ShenQingRiJi": '
                     f'"2023-10-04", "ShenQingRenBuMen": "ＤＸシステム開発Ｇ", "FK_DeptText": "ＤＸシステム開発Ｇ", '
                     f'"RDT": "2023-10-04 14:38", "Rec": "0543956", "Title": "ＤＸシステム開発Ｇ-0543956,'
                     f'真洲句 優祈音は2023-10-05 17:22で開始.", "OID": {item_OID}, "FK_Dept": "11637", "Emps": "0543956", '
                     f'"FID": "0", "FK_NY": "2023-10", "EndJSON": "0"}}')

        item_frmb_str = json.dumps(item_frmb, ensure_ascii=False)
        line = (
            f"'{MyPK2}','1','発送','0','{item_OID}','501','新規申請','502','上司承認','0543956','真洲句 優祈音',"
            f"'0220320','駄御井 進','{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}','0','','',"
            f"'@SendNode=101','(0543956,真洲句 優祈音)','{item_frmb}'")
        writer2.writelines(line + '\n')

        # 3 tt_wf_arrival_returns
        item_summry = (f'{{"AgentMode": "0", "AutoApprovalMode": "N", "content": ['
                       f'{{"value": "高田　優祈音", "name": "従業員氏名"}}, '
                       f'{{"value": "0543956", "name": "社員番号"}}, '
                       f'{{"value": "イオンアイビス（株）", "name": "会社名称"}}, '
                       f'{{"value": "ＤＸシステム開発Ｇ", "name": "所属"}}]}}')

        item_title = f"'ＤＸシステム開発Ｇ-0543956,真洲句 優祈音は{datetime.now().strftime('%Y-%m-%d %H:%M')}で開始.'"

        line = f"'{item_OID}','イオンアイビス（株）','ＤＸシステム開発Ｇ','0543956','高田　優祈音'," \
               f"'111','test','A01','test','入荷返品テスト（王）{i}'," \
               f"'入荷日,仕入伝票No.,返品理由コード,商品名,型番,JANコード,数量,原単価,売単価,総原価,総売価 ?'," \
               f"'','','','{item_summry}'," \
               f"'{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}','0543956'," \
               f"'{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}','0543956','2','11637',{item_title}," \
               f"'0','',502,0,'','真洲句 優祈音'," \
               f"'{datetime.now().strftime('%Y-%m-%d')}','ＤＸシステム開発Ｇ'," \
               f"'{datetime.now().strftime('%Y-%m-%d %H:%M')}',0," \
               f"'{datetime.now().strftime('%Y-%m-%d %H:%M')}','0543956','0543956','1','0','','','','','','',''," \
               f"'{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}',502,'{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'," \
               f"'0','0543956','0543956','2023-10'"

        writer3.writelines(line + '\n')

        # 4. wf_generworkerlist

        # Get the current date and time  Add 1 day to the current date and time
        current_datetime = datetime.now()
        new_datetime = current_datetime + timedelta(days=1)
        dd = new_datetime.strftime('%Y-%m-%d %H:%M:%S')

        # Modified item_title line
        item_title = f"ＤＸシステム開発Ｇ-0543956,真洲句 優祈音は{datetime.now().strftime('%Y-%m-%d %H:%M')}で開始."

        # Modified line
        line = (
            f"'{item_OID}',"
            "'0220320',"
            "'502',"
            "'0',"
            "'駄御井 進',"
            "'上司承認',"
            "'005',"
            "'39510',"
            f"'{dd}',"
            f"'{dd}',"
            f"'{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}',"
            f"'{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}',"
            "'1',"
            "'0',"
            "'0',"
            "'0',"
            "'0543956,真洲句 優祈音',"
            "'1',"
            "'0',"
            "'',"
            "'',"
            "'0',"
            "'',"
            "'',"
            "'@FK_DeptT=デジタルＳ本部長'"
        )
        writer4.writelines(line + '\n')

        line = (
            f"'{item_OID}',"
            "'0543956',"
            "'501',"
            "'0',"
            "'真洲句 優祈音',"
            "'新規申請',"
            "'005',"
            "'11637',"
            "'無',"
            f"'{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}',"
            f"'{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}',"
            f"'{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}','1','0','1','0','','1','0','','','0','','',''"
        )
        writer4.writelines(line + '\n')

        # wf_generworkflow
        current_datetime = datetime.now()
        new_datetime = current_datetime + timedelta(days=1)
        dd = new_datetime.strftime('%Y-%m-%d %H:%M:%S')

        item_01 = f"ＤＸシステム開発Ｇ-0543956,真洲句 優祈音は{datetime.now().strftime('%Y-%m-%d %H:%M')}で開始."
        item_02 = f"@LastTruckID={item_ordernum2}"

        line = (
            f"'{item_OID}','0','102','','005','入荷返品申請','{item_01}','0','2','0543956','真洲句 優祈音','0543956',"
            f"'{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}',"
            f"'{dd}','502','上司承認','11637','ＤＸシステム開発Ｇ','1',"
            f"'{dd}','','','','0','0','0','','','','','','0220320,駄御井進;','1','0','{item_02}','@0543956,真洲句 優祈音@','','2023-10','0','0','0','','',''"
        )
        writer5.writelines(line + '\n')


# 在庫調整
def create_store_csv(total, chargeback_order_id, pk, work_id):
    int_ordernum3 = int(chargeback_order_id[8:-6])
    MyPK3 = pk
    item_OID = work_id

    for i in range(1, total + 1):
        int_ordernum3 += 1
        MyPK3 += 1
        item_OID += 1
        item_ordernum3 = f"SKAT2023{int_ordernum3}"

        # 1.tt_wf_order_numberのデータを書き込む
        line = f"'{item_OID}','007','{datetime.now().strftime('%Y%m%d')}','{item_ordernum3}','{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}','0543956','',''"
        ts1.writelines(line + '\n')

        # 2.nd7trackのデータを書き込む

        item_frmb = {
            "ShenQingRen": "真洲句 優祈音",
            "MyNum": 1,
            "CDT": "2023-10-04 14:38",
            "ShenQingRiJi": "2023-10-04",
            "ShenQingRenBuMen": "ＤＸシステム開発Ｇ",
            "FK_DeptText": "ＤＸシステム開発Ｇ",
            "RDT": "2023-10-04 14:38",
            "Rec": "0543956",
            "Title": f"ＤＸシステム開発Ｇ-0543956,真洲句 優祈音は2023-10-05 17:22で開始.",
            "OID": item_OID,
            "FK_Dept": "11637",
            "Emps": "0543956",
            "FID": "0",
            "FK_NY": "2023-10",
            "EndJSON": "0"
        }

        item_frmb_str = json.dumps(item_frmb, ensure_ascii=False)
        # line = (f"{MyPK3},1,発送,0,{item_OID},"
        #         f"701,新規申請,702,上司承認,0543956,真洲句 優祈音,0220320,駄御井 進,"
        #         f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},0,'','@SendNode=701','(0543956,真洲句 優祈音)','{item_frmb_str}'")
        line = (
            f"'{MyPK3}','1','発送','0','{item_OID}','701','新規申請','702','上司承認','0543956','真洲句 優祈音',"
            f"'0220320','駄御井 進','{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}','0','','',"
            f"'@SendNode=701','(0543956,真洲句 優祈音)','{item_frmb_str}'")
        ts32.writelines(line + '\n')

        # 3 tt_wf_stock_adjustmentのデータを書き込む
        item_summary = {
            "AgentMode": "0",
            "AutoApprovalMode": "N",
            "content": [
                {
                    "value": "高田　優祈音",
                    "name": "従業員氏名"
                },
                {
                    "value": "0543956",
                    "name": "社員番号"
                },
                {
                    "value": "イオンアイビス（株）",
                    "name": "会社名称"
                },
                {
                    "value": "ＤＸシステム開発Ｇ",
                    "name": '所属'
                }
            ]
        }
        item_frmb_str = json.dumps(item_summary, ensure_ascii=False)
        item_title = f"ＤＸシステム開発Ｇ-0543956,真洲句 優祈音は{datetime.now().strftime('%Y-%m-%d %H:%M')}で開始."
        line = (
            f"'{item_OID}',"
            f"'イオンアイビス（株）',"
            f"'ＤＸシステム開発Ｇ',"
            f"'0543956',"
            f"'高田　優祈音',"
            f"'在庫調整申請テスト（王）{i}',"
            f"'倉庫コード,倉庫名,部門コード,部門名,商品コード,品種名,メーカー名,型番,入荷日,ロットNo,原単価,売単価,取引先,仕入伝票No,販売期間,入荷数,単品追加数,単品削除数,入庫数計,出荷済数,ロス数,返品数,不良品数,出荷数計,在庫数,展示品数,出荷準備中数,在庫数計 ? ?111,test,11102,部門テスト1,1110201,,,,,,,,,,,,,,,,,,,,,,, ? ','','','',"
            f"'{item_frmb_str}',"
            f"'{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}',"
            f"'0543956',"
            f"'{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}',"
            f"'0543956',"
            f"'2',"
            f"'11637',"
            f"'{item_title}',"
            f"'0','',"
            f"'702',"
            f"'0',"
            f"'@0543956,真洲句 優祈音@',"
            f"'真洲句 優祈音',"
            f"'{datetime.now().strftime('%Y-%m-%d')}',"
            f"'ＤＸシステム開発Ｇ',"
            f"'{datetime.now().strftime('%Y-%m-%d %H:%M')}',"
            f"'0',"
            f"'{datetime.now().strftime('%Y-%m-%d %H:%M')}',"
            f"'0543956',"
            f"'0543956',"
            f"'1',"
            f"'0','','','','','','','','2023-10-19 09:31:49','702','2023-10-19 09:31:49','0','0543956','0543956','2023-10'"

        )
        ts33.writelines(line + '\n')
        # 4   wf_generworkerlistのデータを書き込む
        current_datetime = datetime.now()
        new_datetime = current_datetime + timedelta(days=1)
        dd = new_datetime.strftime('%Y-%m-%d %H:%M:%S')

        item_title = f'ＤＸシステム開発Ｇ-0543956,真洲句 優祈音は{datetime.now():%Y-%m-%d %H:%M}で開始.'
        # Create the line
        line = (
            f"'{item_OID}',"
            f"'0220320',"
            f"'702',"
            f"'0',"
            f"'駄御井 進',"
            f"'上司承認',"
            f"'007',"
            f"'39510',"
            f"'{dd}',"
            f"'{dd}',"
            f"'{datetime.now():%Y-%m-%d %H:%M:%S}',"
            f"'{datetime.now():%Y-%m-%d %H:%M:%S}',"
            f"'1',"
            f"'0',"
            f"'0',"
            f"'0',"
            f"'0543956,真洲句 優祈音',"
            f"'1',"
            f"'0',"
            f"'',"
            f"'',"
            f"'0',"
            f"'',"
            f"'',"
            f"'@FK_DeptT=デジタルＳ本部長'"
        )
        ts4.writelines(line + '\n')

        # Calculate the current date and time
        now = datetime.now()
        line = (
            f"'{item_OID}',"
            f"'0543956',"
            f"'701',"
            f"'0',"
            f"'真洲句 優祈音',"
            f"'新規申請',"
            f"'007',"
            f"'11637',"
            f"'無',"
            f"'{now.strftime('%Y-%m-%d %H:%M:%S')}',"
            f"'{now.strftime('%Y-%m-%d %H:%M:%S')}',"
            f"'{now.strftime('%Y-%m-%d %H:%M:%S')}',"
            f"'1','0','1','0','','1','0','','','0','','',''"
        )
        ts4.writelines(line + '\n')

        # 5. wf_generworkflowのデータを書き込む
        # Calculate the current date and time
        now = datetime.now()

        # Add 1 day to the current date
        current_datetime = datetime.now()
        new_datetime = current_datetime + timedelta(days=1)
        dd = new_datetime.strftime('%Y-%m-%d %H:%M:%S')

        # Create item_01
        item_01 = f"ＤＸシステム開発Ｇ-0543956,真洲句 優祈音は{now.strftime('%Y-%m-%d %H:%M')}で開始."

        # Create item_02
        item_02 = f"@LastTruckID={item_ordernum3}"

        # Create the line
        line = (
            f"'{item_OID}',"
            f"'0',"
            f"'102',"
            f"'',"
            f"'007',"
            f"'在庫調整申請',"
            f"'{item_01}',"
            f"'0',"
            f"'2',"
            f"'0543956',"
            f"'真洲句 優祈音',"
            f"'0543956',"
            f"'{now.strftime('%Y-%m-%d %H:%M:%S')}',"
            f"'{dd}',"
            f"'702',"
            f"'上司承認',"
            f"'11637',"
            f"'ＤＸシステム開発Ｇ',"
            f"'1',"
            f"'{dd}',"
            f"'','','','0','0','0','','','','','',"
            f"'0220320,駄御井進;',"
            f"'1',"
            f"'0',"
            f"'{item_02}',"
            f"'@0543956,真洲句 優祈音@','',"
            f"'2023-10',"
            f"'0',"
            f"'0',"
            f"'0','','',''"
        )

        ts5.writelines(line + '\n')


def main():
    # 获取命令行参数
    args = sys.argv

    # 打印脚本名称
    script_name = args[0]
    print(f"脚本名称: {script_name}")

    # 打印其他参数
    if len(args) > 1:
        for i, arg in enumerate(args[1:], start=1):
            print(f"参数 {i}: {arg}")

    total = int(args[1])
    work_id = int(args[2])

    commodity_order_id = args[3]
    commodity_pk = int(args[4])

    chargeback_order_id = args[5]
    chargeback_pk = int(args[6])

    store_order_id = args[7]
    store_pk = int(args[8])

    # 1.商品計画申請　100, 'MEP202350000001', 1
    create_commodity_csv(total, commodity_order_id, commodity_pk, work_id)

    # 2. 入荷返品申請 100, 'ALRT202350000001', 1, 1
    create_chargeback_csv(total, chargeback_order_id, chargeback_pk , work_id)

    # 3. 在庫調整    100, 'SKAT202350000001', 1, 1
    create_store_csv(total, store_order_id, store_pk, work_id)


if __name__ == '__main__':
    main()

    # 关闭所有文件
    ts1.close()
    nd1track01.close()
    ts3.close()
    ts22.close()
    ts23.close()
    ts32.close()
    ts33.close()
    ts4.close()
    ts5.close()
