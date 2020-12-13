# !/usr/bin/python
# -*- coding:utf-8 -*-
# Author: Shengjia Yan
# Date: 2017/3/3
# Email: sjyan@seu.edu.cn
# 实验的第一步：原始知识库数据预处理
# 从原始nt文件中抽取实体及其对应的url，并转码

from urllib import unquote
import json
import time
import re
class Preprocess(object):
    # kb_name: 知识库的名称
    # kb_labels_path: 知识库 label 文件的路径
    # kb_entity_quantity: 知识库中实体的数量
    # entity_url_output_path: 处理好的实体以及url数据的输出路径
    # kb_infobox_properties_path: 知识库 infobox_properties 文件路径，用于检测2个实体是否在同一个 RDF 三元组中，以及获取实体的上下文
    # infobox_properties_output_path: 从 infobox_properties 文件中抽取出的 RDF 三元组数据的输出路径
    # kb_infobox_properties_quantity: 知识库中 infobox_properties 的数量
    # kb_abstracts_path: 知识库 abstracts 文件路径，用于获取实体的上下文
    # abstracts_output_path: 从 abstracts 文件中抽取出的数据
    # kb_abstracts_quantity: 知识库中 abstracts 的数量
    # synonym_path: 由 BabelNet 生成的实体同义词文件的路径
    # entity_synonym_output_path: 实体及其同义词的联合文件输出路径
    # synonym_quantity: 知识库中有同义词的实体数量
    def __init__(self, kb_name, kb_labels_path, entity_url_output_path, kb_infobox_properties_path, infobox_properties_output_path, kb_abstracts_path, abstracts_output_path, synonym_path, entity_synonym_output_path):
        self.kb_name = kb_name
        self.kb_labels_path = kb_labels_path
        self.entity_url_output_path = entity_url_output_path
        self.kb_entity_quantity = 0
        self.kb_infobox_properties_path = kb_infobox_properties_path
        self.infobox_properties_output_path = infobox_properties_output_path
        self.kb_infobox_properties_quantity = 0
        self.kb_abstracts_path = kb_abstracts_path
        self.abstracts_output_path = abstracts_output_path
        self.kb_abstracts_quantity = 0
        self.synonym_path = synonym_path
        self.entity_synonym_output_path = entity_synonym_output_path
        self.synonym_quantity = 0

    # 从 labels 文件中抽取知识库的实体
    def extract_entity(self):
        # dbpedia
        if self.kb_name == 'dbpedia':
            baidubaike_entity_counter = 0
            baidubaike_entities = open(self.entity_url_output_path, 'a')
            baidubaike_entity_sum = 12301673
            count=1
            try:
                first_line = True
                with open(self.kb_labels_path,'r')as fp:
                    for line in fp:
                        if first_line or count == baidubaike_entity_sum :
                            first_line = False
                        else:
                            count +=1
                            first_split = line.split("> ")
                            first_uri = first_split[0][1:]
                            second_uri = first_split[1][1:]
                            second_split = first_split[2].split("\"")
                            label = second_split[1]
                            third_split = second_split[2].split(" ")
                            language = third_split[0][1:]
                            entity_url = '<' + label + '> <' + first_uri + '>\n'
                            baidubaike_entities.write(entity_url)

            finally:
                self.kb_entity_quantity = baidubaike_entity_counter
                print count


    # 从 infobox_properties 文件中抽取 RDF 数据，用来：
    # 1. 检测2个实体是否存在于同一个 RDF 中
    # 2. 获取实体的上下文
    def extract_infobox_properties(self):
        # dbpedia
        if self.kb_name == 'dbpedia':
            baidubaike_infobox_properties_counter = 0
            baidubaike_infobox_properties_sum = 30024095
            baidubaike_isrdf = open(self.infobox_properties_output_path, 'a')
            count=1
            try:
                first_line = True
                with open("/Users/ylz/Downloads/DBpedia_2016-2.04/infobox_properties_en.ttl", 'r') as f:
                    for line in f:
                        count+=1
                        m = re.match('^<([^>]+)>\s+<([^>]+)>\s+(.+)', line)
                        if m:
                            v = {'s': None,
                                 'p': None,
                                 'o_kind': None,
                                 'o_value': None}
                            s = m.group(1)
                            p = m.group(2)
                            o = m.group(3)
                            s = re.sub('http://dbpedia.org/resource/', '', s)
                            p = re.sub('http://dbpedia.org/property/', '', p)
                            v['s'] = s
                            v['p'] = p
                            v['o_kind'] = 'unknown'
                            v['o_value'] = o

                            om = re.match('^<([^>]+)>', o)
                            if om:
                                omv = om.group(1)
                                omv = re.sub('http://dbpedia.org/resource/', '', omv)
                                v['o_kind'] = 'resource'
                                v['o_value'] = omv
                            else:
                                om = re.match('\"(.+)\"@en', o)
                                if om:
                                    v['o_kind'] = 'str_en'
                                    v['o_value'] = om.group(1)
                            
                            if v['o_kind'] == "unknown":
                                v['o_value']=re.match('\"(.+)\"', v['o_value']).group()
                            new_rdf = '<' + v['s'] + '> <' + v['p'] + '> <' + v['o_value'] + '>\n'
                            baidubaike_isrdf.write(new_rdf)
            finally:
                self.kb_infobox_properties_quantity = baidubaike_infobox_properties_counter

    # 从 abstracts 文件中抽取 abstract 数据，用于获取实体的上下文
    def extract_abstracts(self):
        # dbpedia
        if self.kb_name == 'dbpedia':
            baidubaike_abstracts_file = open(self.kb_abstracts_path, 'r')
            baidubaike_abstracts_output_file = open(self.abstracts_output_path, 'a')
            count = 0
            baidubaike_abstracts_sum = 5045733
            try:
                first_line = True
                with open(self.kb_abstracts_path, 'r')as fp:
                    for line in fp:
                        if first_line or count == baidubaike_abstracts_sum :
                            first_line = False
                        else:
                            count +=1
                            first_split = line.split("> ")
                            first_uri = first_split[0][1:]
                            entity = re.sub('http://dbpedia.org/resource/', '', first_uri)
                            try:
                                third_split = re.match('\"(.+)\"@en', first_split[2]).group()
                                third_split= re.sub('\"', '', third_split)
                                abstract= re.sub('@en', '', third_split)
                            except Exception as e:
                                abstract = ""

                            entity_abstract = '<' + entity + '> <' + abstract + '>\n'
                            baidubaike_abstracts_output_file.write(entity_abstract)

            finally:
                self.kb_abstracts_quantity = count

                if baidubaike_abstracts_file:
                    baidubaike_abstracts_file.close()

                if baidubaike_abstracts_output_file:
                    baidubaike_abstracts_output_file.close()

    # 将实体和同义词合并
    def conbine_entity_synonym(self):
        # baidubaike
        if self.kb_name == 'baidubaike':
            baidubaike_entity_file = open(self.entity_url_output_path, 'r')
            baidubaike_synonym_file = open(self.synonym_path, 'r')
            baidubaike_entity_synonym_file = open(self.entity_synonym_output_path, 'a')
            baidubaike_synonym = []
            baidubaike_synonym_quantity = 77509
            synonym_counter = 0
            count=0
            try:
                for line in baidubaike_synonym_file.readlines():
                    synonym_counter += 1
                    dict = {}
                    line = line.strip('\n')

                    # split
                    split1 = line.split('> <')
                    entity = split1[0]
                    syn = split1[1]
                    dict['entity'] = entity
                    dict['synonym'] = syn

                    baidubaike_synonym.append(dict)

                for line in baidubaike_entity_file.readlines():
                    count += 1
                    line = line.strip('\n')

                    # split
                    split = line.split('> <')
                    entity = split[0]

                    # clean
                    entity = entity[1:]

                    # combine
                    synonym = ''

                    for d in baidubaike_synonym:
                        if entity == d['entity']:
                            synonym = d['synonym']
                            break
                    entity_synonym = '<' + entity + '> <' + synonym + '>\n'
                    baidubaike_entity_synonym_file.write(entity_synonym)
                    print count

            finally:
                self.synonym_quantity = synonym_counter

                # if baidubaike_entity_file:
                #     baidubaike_entity_file.close()

                # if baidubaike_synonym_file:
                #     baidubaike_synonym_file.close()

                # if baidubaike_entity_synonym_file:
                #     baidubaike_entity_synonym_file.close()

