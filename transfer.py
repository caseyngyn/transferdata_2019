'''
Casey Nguyen
transfer.py
backend of lab2 
1.	Read data from all 3 input files and store in a numpy array or Python container as appropriate.
2.	Calculate all the static data that support data User interaction tasks shown above.
3.	Plot the total transfer trend 
4.	Plot the transfer trend of one or more community colleges and of the average of all the colleges.
5.	Plot the transfer numbers of the top 10 colleges.
'''
import csv

import numpy as np
import  matplotlib.pyplot  as  plt
import operator


def printData(fct):
    '''decorator'''
    def wrapper(*args,**kwargs):
        '''wrappper'''
        result = fct(*args,**kwargs)
        #print(type(result))
        print(result)
        return result
    return wrapper

class Transfer:
    def __init__(self,*filenames):
        self.college_name = Transfer.get_names(filenames[0])
        self.years = Transfer.get_years(filenames[1])
        self.transfer_data = Transfer.get_data(filenames[2])
        self.ttl_transfer_rate = np.sum(self.transfer_data,axis = 1) #axis = 1 means by row 
        self.avg_transfer_rate = self.transfer_data.mean(axis = 0) #means going to col
        
    def get_names(self,infile = "transferCC.csv"):
        """ 
        gets name from transferCC.csv 
        returns: list of college names
        """

        college_name=[]
        with open(infile,'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                college_name.append(row[0])

        return college_name

    def get_years(self,infile= "transferYear.csv"):
        """
        gets years from transferyear.csv
        return list of academic years
        """

        years= []
        with open(infile,'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                for i in range(len(row)):
                    years.append(row[i])

        return years

    def get_data(self,infile = "transferData.csv"):
        """
        Gets transfer numbers form transferData.csv
        Returns: np darray of transfer data
        """

        data_array = []
        with open(infile,'r') as csvfile:
            reader = csv.reader(csvfile)
            strip = lambda strIn: strIn.strip("\'")
            for row in reader:
                temp_list = []
                for i in range(len(row)):
                    temp_list.append(int(strip(row[i])))
                data_array.append(temp_list)
        data_array = np.array(data_array)
            

        return data_array     

    @printData
    def plotTotalTransfer(self):
        """
        Plots the total number of transfers for each academic year
        Returns: np double array of the total transfers
        """
        ttl_transfers = np.sum(self.transfer_data,axis = 0) #axis = 0 mean col   
        
        plt.plot(np.arange(1,12),ttl_transfers)
        plt.xticks(np.arange(1,12),self.years)
        plt.tick_params(axis = 'x',rotation = 45,labelsize = 6)
        plt.title('Number of Transfers')
        plt.xlabel('Years')
        plt.ylabel('Transfer')
        
        #plt.show() 

        return ttl_transfers

    @printData
    def plotEnrollmentTrend(self,*args):
        """ 
        Plots the average transfer trend of colleges thru the academic years
        and plots the transfer numbers of each college in the argument through the 
        academic years
        Returns: np darray of the average enrollment numbers    
        """
        for arg in args:
            plt.plot(np.arange(1,12),self.transfer_data[arg],"-*", label = self.college_name[arg])
        
        plt.plot(np.arange(1,12),self.avg_transfer_rate,"-*", label = 'average transfer')
        
        plt.xticks(np.arange(1,12),self.years)
        plt.tick_params(axis = 'x',rotation = 45,labelsize = 6)
        plt.legend(loc = 'best')
        plt.title('Enrollment Trends')
        plt.xlabel('Years')
        plt.ylabel('Transfers')
        
       # plt.show()
        return self.avg_transfer_rate

    @printData
    def show_top_ten(self):
        """
        plot top 10 schools with a bar graph
        Returns: np dattay of the top 10 transfer numbers.
        """
        transfer_list = list(self.ttl_transfer_rate)
        name_list = list(self.college_name)
        desc_dict={}

        # so I can sort the numbers and the the names will also be sorted
        for x in range(len(transfer_list)):
            desc_dict.update({name_list[x] : transfer_list[x]})

        desc_dict = dict(sorted(desc_dict.items(), key=operator.itemgetter(1),reverse=True))
        
        top_names = []
        top_num = []

        for x in list(desc_dict)[0:10]:
            top_names.append(x)

        for x in list(desc_dict.values())[0:10]:
            top_num.append(x)        

        #reverse bc grapgh wants it from lowest to highest
        top_names.reverse()
        top_num.reverse()

        #bar graph
        plt.bar((1,2,3,4,5,6,7,8,9,10),top_num)
        plt.title('Top 10 Transfers')
        plt.xlabel('College Names')
        plt.ylabel('Transfer Num')
        plt.xticks((1,2,3,4,5,6,7,8,9,10),top_names)
        plt.tick_params(axis = 'x', labelsize = 7)
        #plt.show()

        top_num.reverse()
        top_num = np.array(top_num)
        return top_num

'''

def main():
    filenames = ['transferCC.csv','transferYear.csv','transferData.csv']       
    app = Transfer(*filenames)
    #app.plotTotalTransfer()
    #lists = (0,1,2)
    #app.plotEnrollmentTrend(*lists)
    #app.show_top_ten()

main()
'''