import json
import urllib
import operator
import time
import threading
from time import ctime
from preprocess import *
from candidate import *
from disambiguation import *
from sameas import *
from result import *
from mark import *
def preprocess(x,y):
    # baidubaike
    kb_name = 'baidubaike'
    kb_labels_path = '/Users/ylz/Downloads/zhishime_json/baidubaike/home/wl/zhishime2/baidubaike/3.0_baidubaike_labels_zh.json'
    entity_url_output_path = '/Users/ylz/ylz/jist2016-link/data/entity/baidubaike_entity_url.txt'
    kb_infobox_properties_path = '/Users/ylz/Downloads/zhishime_json/baidubaike/home 2/wl/zhishime2/baidubaike/3.0_baidubaike_infobox_properties_zh.json'
    infobox_properties_output_path = '/Users/ylz/ylz/jist2016-link/data/baidubaike_infobox_properties.txt'
    kb_abstracts_path = '/Users/ylz/Downloads/zhishime_json/baidubaike/home 3/wl/zhishime2/baidubaike/3.0_baidubaike_abstracts_zh.json'
    abstracts_output_path = '../../data/abstract/baidubaike_abstracts.txt'
    synonym_path = '../../data/synonym/baidubaike_entities_syn.txt'
    entity_synonym_output_path = '../../data/entity/baidubaike_entity_synonym'+str(x)+'.txt'

    extracter_baidubaike = Preprocess(kb_name, kb_labels_path, entity_url_output_path, kb_infobox_properties_path, infobox_properties_output_path, kb_abstracts_path, abstracts_output_path, synonym_path, entity_synonym_output_path)
    extracter_baidubaike.conbine_entity_synonym()

threads = []
x=0
for t in range(0,2):
    t= threading.Thread(target=preprocess,args=(str(x),x))
    threads.append(t)
    x+=1
if __name__=="__main__":
    for thr in threads:
        thr.start()
    thr.join()
