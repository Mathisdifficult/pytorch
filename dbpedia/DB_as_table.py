

import os.path as path

import math,re,csv,random,time,json

def bubble_sort(x):
    flag=True
    while flag:
        flag=False
        for i in range(len(x)-1):
            if x[i]>x[i+1]:
                x[i],x[i+1]=x[i+1],x[i]
                flag=True
    return x

class Table:

    def __init__(self, table_dir='NULL'):

        self.table_directory=table_dir

        self.table_data=[]

        self.col=0

        self.row=0

        self.shape=[self.row, self.col]

    def __call__(self, *args, **kwargs):

        return self.shape

    def get_col(self,index:int):

        col_data=[]

        try:

            for row in self.table_data:

                col_data.append(row[index])

        except:

            raise Exception('out of index range')

        return col_data

    def get_row(self,index:int):

        try:

            return self.table_data[index]

        except:

            raise Exception('out of index range')

    def updata_shape(self):

        self.row=len(self.table_data)

        self.col=len(self.table_data[0])

        self.shape=[self.row,self.col]

    def display(self):

        print(self.table_data)

    def save_csv(self,table_save_dir):

        f=open(table_save_dir,'w',encoding='utf8')

        csv_file=csv.writer(f)

        csv_file.writerows(self.table_data)

        f.close()


class MarkedTable(Table):

    def __init__(self, table_dir='NULL', table_save_dir='NULL'):

        super(MarkedTable, self).__init__()

        self.table_save_directory=table_save_dir

        self.table_mark=[]

        if not table_dir=='NULL':

            try:

                self.name=path.splitext(path.split(self.table_directory)[1])[0]

                f = open(table_dir, 'r', encoding='utf8')

                json_file = json.load(f)

                for cell in json_file:

                    if cell['isheader']:

                        self.col+=1

                    else:

                        break

                f.close()

                self.row=int(len(json_file)/self.col)

                for i in range(self.row):

                    for j in range(self.col):

                        self.table_data[i].append(json_file[i*self.col+j]['text'])

                        self.table_mark[i].append(json_file[i*self.col+j]['mark'])

            except:

                raise Exception('wrong file directory.')

        else:

            print('table directory is \'NULL\' !')

    def del_col(self, index: int):

        if index == 0:

            print('first col cannot be delete !')

        else:

            try:

                for row in self.table_data:

                    row.pop(index)

                for row in self.table_mark:

                    row.pop(index)

            except:

                raise Exception('out of index range')

    def del_row(self, index: int):

        if index == 0:

            print('header row cannot be delete !')

        else:

            try:

                self.table_data.pop(index)

                self.table_mark.pop(index)

            except:

                raise Exception('out of index range')

    def save_json(self,name):

        if not self.table_save_directory=='NULL':

            f = open(path.join(self.table_save_directory,name+'.json'), 'w', encoding='utf8')

            for i in range(self.row):

                for j in range(self.col):

                    temp_dict = {}

                    if i==0:

                        temp_dict['isheader'] = True

                        temp_dict['text'] = self.table_data[i][j]

                    else:

                        temp_dict['isheader'] = False

                        temp_dict['text'] = self.table_data[i][j]

                    temp_dict['mark'] = self.table_mark[i][j]

                    json.dump(temp_dict, f)
                    #json_table.append(temp_dict)

            f.close()

        else:

            print('table_save_directory is \'NULL\' !')

    def table_decompose(self, name,row_range=10,col_range=10,generate_num:int=10,row_shuffle:bool=True,col_shuffle:bool=True):

        try:

            min_row,max_row=row_range[0],row_range[1]

            min_col,max_col=col_range[0],col_range[1]

        except:

            min_row=max_row=row_range

            min_col=max_col=col_range

        for i in range(generate_num):

            generated_table=MarkedTable(table_save_dir=self.table_save_directory)

            # randomly pick the rows
            row_rand=random.randint(min_row,min(self.row-1,max_row))

            row_index=[n for n in range(1, self.row)]

            random.shuffle(row_index)

            rand_row=row_index[:row_rand]

            if not row_shuffle:

                for row_num in rand_row:

                    generated_table.table_data.append(self.table_data[row_num])

            else:

                rand_row=bubble_sort(rand_row)

                for row_num in rand_row:

                    generated_table.table_data.append(self.table_data[row_num])

                    generated_table.table_mark.append(self.table_mark[row_num])

            col_rand=random.randint(min_col,min(self.col-1,max_col))

            col_index=[n for n in range(1, self.col)]

            random.shuffle(col_index)

            rand_col=col_index[:col_rand]

            if col_shuffle:

                for row in generated_table.table_data:

                    row =[row[0]]+[row[n] for n in rand_col]

                for row in generated_table.table_mark:

                    row=[row[0]]+[row[n] for n in rand_col]

            generated_table.updata_shape()

            generated_table.save_json(name + '_decomposed'+str(i))


class DBpediaAsTable(Table):

    def __init__(self,table_dir):

        # dir is where you save the dbpedia as tables you download
        # table_type is determined by the csv file's name
        super(DBpediaAsTable,self).__init__()

        self.table_directory=table_dir

        self.table_type=path.splitext(path.split(table_dir)[1])[0]

        self.table_data=[]

        f=open(table_dir,'r',encoding='utf8')

        csv_file=csv.reader(f)

        # read the content in the csv file
        for row in csv_file:

            self.table_data.append(row)

        f.close()

        self.row=len(self.table_data)

        self.col=len(self.table_data[0])

        self.shape=[self.row, self.col]

    def __call__(self, *args, **kwargs): # __call__() returns the path of the table

        return self.shape

    # domain of header_ontology following is ['XMLSchema', 'dbpedia', 'w3']
    def table_marked(self,save_dir='NULL',header_ontology:str='dbpedia'): # turn the dbpedia as table into marked table

        # the first column represents the entities for each row
        # the sec column depicts the label corresponding to col 1
        if header_ontology not in ['XMLSchema', 'dbpedia', 'w3']:

            return 'Informal header_ontology, input one of the value in [\'XMLSchema\', \'dbpedia\', \'w3\'] !'

        marked_table=MarkedTable(table_save_dir=save_dir)

        # from index 4 on, we reach the content of the table. do col work.
        # get entity lable, entity pair index
        pair_list=[]

        pattern = re.compile(r'.*_label')

        for i in range(2,self.col):

            if not re.match(pattern,self.table_data[0][i])==None:

                real_header=self.table_data[0][i][:-6]

                for j in range(2,self.col):

                    if real_header==self.table_data[0][j]:

                        pair_list.append(tuple([j,i]))

        pair_list=[(1,0)]+pair_list

        for tup in pair_list:

            data_col=self.get_col(tup[0])

            # precess entity data
            for i in range(len(data_col)):

                try:

                    marked_table.table_data[i].append(data_col[i])

                except:

                    marked_table.table_data.append([])

                    marked_table.table_data[i].append(data_col[i])

            mark_col = self.get_col(tup[1])

            # precess entity data
            for i in range(len(mark_col)):

                try:

                    marked_table.table_mark[i].append(mark_col[i])

                except:

                    marked_table.table_mark.append([])

                    marked_table.table_mark[i].append(mark_col[i])

        header_ontology_num = lambda x: math.ceil(math.sqrt(abs(x - 7) + 1))

        for i in range(1,4):

            if not i == header_ontology_num(len(header_ontology)):

                marked_table.del_row(i)

        marked_table.updata_shape()

        if not save_dir=='NULL':

            marked_table.save_json(self.table_type+'_marked')

        return marked_table










