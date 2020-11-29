# coding=UTF-8
from urllib import unquote
import json
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')  

def cut():
    baidubaike_entity_file = open('../../data/entity/baidubaike_entity_syn_out_temp.txt', 'r')
    count=0
    dataList = []
    flag=0
    baidubaike_entity_synonym_file = open("../../data/entity/baidubaike_entity_synonym.txt", 'r')
    baidubaike_entity_url_file = open("../../data/entity/baidubaike_entity_url.txt", 'r')
    baidubaike_entity_synonym_temp = []
    for line in baidubaike_entity_file.readlines():
        line = line.strip('\n')
        split = line.split('> <')
        count+=1
        entity = split[0]
        entity = entity[1:]
        if str("秋季") in entity:
            print entity
        # dict = {}
        # dict['entity'] = entity

    # baidubaike_entity_candidate = []
    # for i in range(0,30):
    #     path = "/Users/ylz/ylz/jist2016-link/data/disambiguation/baidubaike/result/" + str(i) + '.txt'
    #     with open(path, 'r') as f:
    #         aa = json.load(f)
    #         baidubaike_entity_candidate.append(aa)
    # baidubaike_candidate_file = open("../../data/disambiguation/baidubaike/result/single_kb_el_result.txt", 'w')                
    # baidubaike_entity_candidate_json = json.dumps(baidubaike_entity_candidate,ensure_ascii=False)
    # print baidubaike_entity_candidate_json
    # baidubaike_candidate_file.write(baidubaike_entity_candidate_json)
    #     baidubaike_entity_synonym_temp.append(dict)
    # for entity_synonymm in baidubaike_entity_synonym_temp:
    #     for line2 in baidubaike_entity_synonym_file.readlines():
    #         line2 = line2.strip('\n')
    #         split2 = line2.split('> <')
    #         entity2 = split2[0] 
    #         if entity_synonymm['entity']==entity2:
    #             synonym = split2[1]
    #             flag = 1
    #             entity_synonym = '<' + entity_synonymm['entity'] + '> <' + synonym + '>\n'
    #             baidubaike_entity_file.write(entity_synonym)
    #     if flag==0:
    #         entity_synonym = '<' + entity_synonymm['entity'] + '> <'  +entity_synonymm['entity']+ '>\n'
    #         baidubaike_entity_file.write(entity_synonym)                
    #     count+=1

    # print count

if __name__ == "__main__":
    cut()