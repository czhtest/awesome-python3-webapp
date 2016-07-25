import pandas as pd
#先建一个索引
rowIndexs=[5,15,30,60,'D']
cols=['MA14','MA60','MA99','MA888','LOW','UP']
dayframe = pd.DataFrame(index=rowIndexs,columns=cols)

dbCols=['date','open','close','high','low','volume']