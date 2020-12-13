# !/usr/bin/python
# -*- coding:utf-8 -*-  
# Author: Shengjia Yan
# Date: 2017/5/9
# Email: sjyan@seu.edu.cn

# 结果模块，将人工标注数据与计算系统标注结果相比较，从而得出实体链接的准确率

import json
from table import *

class Result(object):
    # table_path: 表格路径
    # single_kb_el_result_path: 单库EL结果路径
    # multiple_kb_el_result_path: 多库EL结果路径
    # baidubaike_human_mark_entity_path: 基于 baidubaike 的表格EL人工标注结果路径
    # hudongbaike_human_mark_entity_path: 基于 hudongbaike 的表格EL人工标注结果路径
    # zhwiki_human_mark_entity_path: 基于 zhwiki 的表格EL人工标注结果路径
    def __init__(self, table_path, single_kb_el_result_path, multiple_kb_el_result_path, baidubaike_human_mark_entity_path, hudongbaike_human_mark_entity_path, zhwiki_human_mark_entity_path):
        self.table_path = table_path
        table_manager = TableManager(table_path)
        self.tables = table_manager.get_tables()
        self.table_quantity = table_manager.table_quantity
        self.single_kb_el_result_path = single_kb_el_result_path
        self.multiple_kb_el_result_path = multiple_kb_el_result_path
        self.baidubaike_human_mark_entity_path = baidubaike_human_mark_entity_path
        self.hudongbaike_human_mark_entity_path = hudongbaike_human_mark_entity_path
        self.zhwiki_human_mark_entity_path = zhwiki_human_mark_entity_path

    def compare(self):
        baidubaike_human_mark_entity_file = open(self.baidubaike_human_mark_entity_path, 'r')
        baidubaike_human_mark_entity = baidubaike_human_mark_entity_file.read()
        baidubaike_human_mark_entity_json = json.loads(baidubaike_human_mark_entity, encoding='utf8')

        # hudongbaike_human_mark_entity_file = open(self.hudongbaike_human_mark_entity_path, 'r')
        # hudongbaike_human_mark_entity = hudongbaike_human_mark_entity_file.read()
        # hudongbaike_human_mark_entity_json = json.loads(hudongbaike_human_mark_entity, encoding='utf8')

        # zhwiki_human_mark_entity_file = open(self.zhwiki_human_mark_entity_path, 'r')
        # zhwiki_human_mark_entity = zhwiki_human_mark_entity_file.read()
        # zhwiki_human_mark_entity_json = json.loads(zhwiki_human_mark_entity, encoding='utf8')

        single_kb_el_result_file = open(self.single_kb_el_result_path, 'r')
        single_kb_el_result = single_kb_el_result_file.read()
        single_kb_el_result_json = json.loads(single_kb_el_result, encoding='utf8')

        # multiple_kb_el_result_file = open(self.multiple_kb_el_result_path, 'r')
        # multiple_kb_el_result = multiple_kb_el_result_file.read()
        # multiple_kb_el_result_json = json.loads(multiple_kb_el_result, encoding='utf8')
        try:
            # Single KB
            print 'The Result of Entity Linking only with Single KB:'

            # baidubaike
            print 'baidubaike:'
            baidubaike_total_mention_quantity = 0
            baidubaike_total_correct_link_quantity = 0

            for i in range(self.table_quantity):
                table = self.tables[i]
                row_num = table.row_num
                col_num = table.col_num
                current_table_mention_quantity = 0
                current_table_correct_link_quantity = 0

                for r in range(row_num):
                    if r == 0:
                        continue
                    for c in range(col_num):
                        if baidubaike_human_mark_entity_json[i][r][c]['entity'] == 'Null':
                            continue

                        human_mark_entity = baidubaike_human_mark_entity_json[i][r][c]['entity']
                        system_mark_entity = single_kb_el_result_json[i][r][c]['entity']


                        if human_mark_entity == system_mark_entity:
                            current_table_correct_link_quantity += 1
                            baidubaike_total_correct_link_quantity += 1
                        else:
                            print human_mark_entity+" "+system_mark_entity

                        current_table_mention_quantity += 1
                        baidubaike_total_mention_quantity += 1

                if current_table_mention_quantity == 0:
                    print 'Table ' + str(i) + 'has no Mention!'
                    continue
                else:
                    current_table_precision = float(current_table_correct_link_quantity) / current_table_mention_quantity
                    print 'Table ' + str(i) + ' Precision: ' + str(current_table_correct_link_quantity) + '/' + str(current_table_mention_quantity) + ' = ' + str(current_table_precision)
            total_precision = float(baidubaike_total_correct_link_quantity) / baidubaike_total_mention_quantity
            print 'Total Precision Evaluated with baidubaike: ' + str(baidubaike_total_correct_link_quantity) + '/' + str(baidubaike_total_mention_quantity) + ' = ' + str(total_precision)
            print

   

        finally:
            if baidubaike_human_mark_entity_file:
                baidubaike_human_mark_entity_file.close()

