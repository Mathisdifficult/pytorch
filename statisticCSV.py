import csv
import os
import pandas as pd
import xml.etree.ElementTree  as ET
from xml.dom.minidom import parse
# import ulad
all_num=0
Limaye200 = "/Users/ylz/ylz/web_table_database/Limaye200/raw"
Limaye_complete = "/Users/ylz/ylz/web_table_database/Limaye_complete/all_tables_raw(regen)"
def scan_folder(directory, prefix=None, postfix=None):
    global all_num
    files_list = []
    #os.chdir(os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))) #进入上一级目录
    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            if postfix:
                if special_file.endswith(postfix):
                    files_list.append(os.path.join(root, special_file))
            elif prefix:
                if special_file.startswith(prefix):
                    files_list.append(os.path.join(root, special_file))
            else:
                files_list.append(os.path.join(root, special_file))
    all_num = len(files_list)
    return files_list

def roughly_statistic_xml(folder_path):

    count = 0
    cellnum=0
    l=[]
    csvfolder_path = folder_path
    # print(csvfolder_path)
    # print(all_num)
    domTree = parse(folder_path)
    rootNode = domTree.documentElement
    cells = rootNode.getElementsByTagName("cell")
    for cell in cells:
        html = cell.getElementsByTagName("html")[0]
        if(html.childNodes):
            cellnum+=1

            if (', ' in html.childNodes[0].data):
                count += 1
                print(folder_path)
                print(html.nodeName, ":", html.childNodes[0].data)
                l+=html.childNodes[0].data
                # if wikipedia.childNodes:
                break

    if(count!=0):
        print('statistic cell number: %d' % count, '\n', 'all cell number: %d' % cellnum, '\n',
              'ratio: %.4f' % (count / cellnum))
        # print(count)
        print("\n")
    return  l


        # # phone 元素
        # phone = customer.getElementsByTagName("phone")[0]
        # print(phone.nodeName, ":", phone.childNodes[0].data)
        # # comments 元素
        # comments = customer.getElementsByTagName("comments")[0]
        # print(comments.nodeName, ":", comments.childNodes[0].data)

    # print(cells)
    # print("\n")
def roughly_statistic(folder_path):
    count = 0
    l=[]
    csvfolder_path = folder_path
    all_num = len(scan_folder(csvfolder_path))
    for csvfile in scan_folder(csvfolder_path):
        with open(csvfile, 'r', encoding='utf-8') as f:
            flag = False
            for row in f:
                try:
                    header += 1
                except:
                    header = 0
                    if 'Date' in row or 'date' in row:
                        flag = True
                    continue
                if ', ' in row and flag == False:
                    count += 1
                    print(csvfile)
                    break
            del header

    print('list cell number: %d' % count, '\n', 'all table number: %d' % all_num, '\n',
          'ratio: %.4f' % (count / all_num))
    print(count)

def precise_statistic(folder_path):
    count = 0
    csvfolder_path = folder_path
    all_num = len(scan_folder(csvfolder_path))
    for csvfile in scan_folder(csvfolder_path):
        file = pd.read_csv(csvfile)
        #df = pd.DataFrame(file)
        for i in range(file.columns.size - 1):
            col = file.iloc[:, i:i + 1]
            if 'Date' in col.loc[0] or 'date' in col.loc[0]:
                continue
            else:
                data_col = col.loc[1:]
                for j in len(data_col):
                    if ', ' in str(data_col.loc[j]):
                        count += 1
                        print(csvfile)
                        break


    print('list cell number: %d' % count, '\n', 'all table number: %d' % all_num, '\n',
          'ratio: %.4f' % (count / all_num))

# csv_folder=r'/Users/ylz/Downloads/200_tables_regen/raw'
Limaye200 = r"/Users/ylz/ylz/web_table_database/Limaye200/raw"
Limaye_complete = r"/Users/ylz/ylz/web_table_database/Limaye_complete/all_tables_raw(regen)"
i=0

l=[]

for file in scan_folder(Limaye_complete):
    l+=roughly_statistic_xml(file)
    l+="\n"
    # i+=1
    # if i%100==10:
    #     l.append(file)
    # print(l)
print(l)
# newDir=r'/home/yanglianzheng/output'

# ulad.moveFiles(newDir,l)

#roughly_statistic(csv_folder)
