#excel
import xlrd
from xlutils.copy import copy
import types
#定义操作数据excel的单元格
#data = xlrd.open_workbook('E:/PYWork/awesome-python3-webapp/www/yupen.xls')
print('..............')
class MyData():
    file = 'yupen.xls'
    data = xlrd.open_workbook(file)
    table = data.sheet_by_index(0)
    nrows = table.nrows
    date=None
    wb = copy(data)
    ws = wb.get_sheet(0)

    #找到日期行，不存在，添加
    def check_date(self):
        if not self.date.strip():
            print('日期为空...')
            return -1
        else:
            for row in range(self.table.nrows):
                if self.date in self.table.cell(row,0).value:
                    print('日期已经存在:',self.date)
                    return row
            #找不到的时候需要写入

            #print('cols',self.ncols)
            self.ws.write(self.nrows,0,self.date)
            self.nrows = self.nrows + 1
            print('write after',self.nrows,'col',0,'date',self.date)
            #self.wb.save(self.file)

            return self.nrows
    def write_data(self,col,value):
        #nrow = self.check_date()
        #print('nrow:',nrow)
        if col >= self.table.ncols:
            print('超出列范围:value',value)
            return
        if self.nrows != -1:
            #print('write nrow',nrow,'col',col,'value',value)

            self.ws.write(self.nrows,col,value)


    def writeSZZSClose(self,close):
        self.write_data(1,close)
    def writeSZZSLimit(self,limit):
        self.write_data(2,limit)
    def writeSZZSPer(self,close,limit):
        self.writePer(3,close,limit)
    def writePer(self,col,close,limit):
        nrow=self.check_date()

        if nrow != -1:
           if type(close) ==int and type(limit)==int:
                #print "%.2f%" % ((limit-close)/close)
                self.write_data(col,round((limit-close)/close,2))
    def writeCYBZClose(close):
        self.write_data(4,close)
    def writeCYBZLimit(self,limit):
        self.write_data(5,limit)
    def writeCYBZPer(self,close,limit):
        self.writePer(6,close,limit)

    def writeZXBZClose(self,close):
        self.write_data(7,close)
    def writeZXBZLimit(self,limit):
        self.write_data(8,limit)
    def writeZXBZPer(self,close,limit):
        self.writePer(9,close,limit)

    def writeYSBZClose(self,close):
        self.write_data(10,close)
    def writeYSBZLimit(self,limit):
        self.write_data(11,limit)
    def writeYSBZPer(self,close,limit):
        self.writePer(12,close,limit)
    def save(self):
        self.wb.save(self.file)

data = MyData()
data.date = '2016-07-03'
data.check_date()
data.writeSZZSLimit(2870)
data.writeCYBZLimit(3000)

data.date='2016-07-04'
data.check_date()
data.writeSZZSLimit(2871)
data.writeCYBZLimit(4444)

data.date='2016-07-05'
data.check_date()
data.writeSZZSLimit(2872)
data.writeCYBZLimit(4446)
data.save()