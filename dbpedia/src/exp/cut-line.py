# # coding=UTF-8
import re
import time
import sys
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning,InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

reload(sys)
sys.setdefaultencoding('utf8')
def popular(e):
    # s = requests.session()
    # proxies = {'http': 'http://localhost:1087', 'https': 'http://localhost:1087'}
    # url='https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch='+e+'&prop=info&inprop=url&utf8=&format=json'
    # r=s.get(url,proxies=proxies, verify=False)
    # return json.loads(r.text)["query"]["searchinfo"]["totalhits"]

    # baidubaike_entity_synonym_file = open('../../data/entity/baidubaike_entity_synonym.txt', 'w')
    # with open("/Users/ylz/Downloads/DBpedia_2016-2.04/disambiguations_en.ttl", 'r') as f:
    #     firstline=True
    #     quantity=1481710
    #     count=1
    #     for line in f:
    #         if firstline or count==quantity-1:
    #             firstline=False
    #         else:
    #             count+=1
    #             split = line.split('> <')
    #             entity1 = split[0][1:]
    #             entity2 = split[2].split("> ")[0]
    #             entity1 = re.sub('http://dbpedia.org/resource/', '', entity1)
    #             entity2 = re.sub('http://dbpedia.org/resource/', '', entity2)
    #             entity_synonym = '<' + entity2 + '> <' + entity1 + '>\n'
    #             baidubaike_entity_synonym_file.write(entity_synonym)


# with open("/Users/ylz/Downloads/DBpedia_2016-2.04/infobox_properties_en.ttl", 'r') as f:
#     for line in f:
#         m = re.match('^<([^>]+)>\s+<([^>]+)>\s+(.+)', line)
#         if m:
#             v = {'s': None,
#                  'p': None,
#                  'o_kind': None,
#                  'o_value': None}
#             s = m.group(1)
#             p = m.group(2)
#             o = m.group(3)
#             s = re.sub('http://dbpedia.org/resource/', '', s)
#             p = re.sub('http://dbpedia.org/property/', '', p)
#             v['s'] = s
#             v['p'] = p
#             v['o_kind'] = 'unknown'
#             v['o_value'] = o

#             om = re.match('^<([^>]+)>', o)
#             if om:
#                 omv = om.group(1)
#                 omv = re.sub('http://dbpedia.org/resource/', '', omv)
#                 v['o_kind'] = 'resource'
#                 v['o_value'] = omv
#             else:
#                 om = re.match('\"(.+)\"@en', o)
#                 if om:
#                     v['o_kind'] = 'str_en'
#                     v['o_value'] = om.group(1)
            
#             if v['o_kind'] == "unknown":
#                 v['o_value']=re.match('\"(.+)\"', v['o_value']).group()
                
#             print str(v)
#             time.sleep(0.3)
# print names


# from urllib import unquote
# import json
# import time
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')  

# def cut():
#     count=1
#     with open("/Users/ylz/Downloads/DBpedia_2016-2.04/infobox_properties_en.ttl",'r')as fp:
#         for line in fp:
#             count+=1
#         print count
    # baidubaike_entity_file = open('../../data/entity/baidubaike_entity_syn_out_temp.txt', 'r')
    # count=0
    # dataList = []
    # flag=0
    # baidubaike_entity_synonym_file = open("../../data/entity/baidubaike_entity_synonym.txt", 'r')
    # baidubaike_entity_url_file = open("../../data/entity/baidubaike_entity_url.txt", 'r')
    # baidubaike_entity_synonym_temp = []
    # for line in baidubaike_entity_file.readlines():
    #     line = line.strip('\n')
    #     split = line.split('> <')
    #     count+=1
    #     entity = split[0]
    #     entity = entity[1:]
    #     if str("秋季") in entity:
    #         print entity
        # dict = {}
        # dict['entity'] = entity
    # baidubaike_entity_candidate = []
    # baidubaike_candidate_file = open("../../data/entity/baidubaike_entity_synonym.txt", 'r')
    # for line in baidubaike_candidate_file.readlines():
    #     line = line.strip('\n')
    #     split = line.split('> <')
    #     entity = split[0]
    #     entity = entity[1:]
        # print entity
    #     baidubaike_entity_candidate.append(entity) 
    #     if "Alien_(law)"   in baidubaike_entity_candidate:
    #         print entity
    # print "start"
    # print baidubaike_entity_candidate
    path = "../../data/entity/baidubaike_entity_url.txt"
    with open(path, 'r') as f:
        for line in f:
            line = line.strip('\n')
            split = line.split('> <')
            entity = split[0]
            entity = entity[1:]
            # print entity
            if "West Indies" == entity :
                print entity
            


    # baidubaike_candidate_file = open("../../data/entity/baidubaike_entity_synonym.txt", 'r')
    # for line in baidubaike_candidate_file.readlines():
    #     print line            
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
    popular("chicago")