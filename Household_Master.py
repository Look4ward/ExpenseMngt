
# coding: utf-8

# In[247]:


import pandas as pd
import numpy as np
import glob
import datetime as dt


# In[267]:


file_visa = pd.DataFrame(columns = ['date','item','amount','blank','cardno'])
path = 'VISA*.csv'

FileNo = 1
for fname in glob.glob(path):
    f= pd.read_csv(fname,names = ['date','item','amount','blank','cardno'])
    print (f.head())
    print ('breakline 1---------------- File #',FileNo)
    file_visa = pd.concat([file_visa,f])
    print (file_visa.tail())
    print('breakline 2 -----------------')
    FileNo = FileNo+1

print ( file_visa.groupby(['cardno']).count())
file_visa = file_visa.drop_duplicates(subset=None, keep='first', inplace=False)
print ( file_visa.groupby(['cardno']).count())

file_visa['month']= [x[:2] for x in file_visa['date']]
file_visa['year']= [x[-4:] for x in file_visa['date']]
file_visa['day']= [x[3:5] for x in file_visa['date']]



# In[249]:


file_visa['exp_month'] = file_visa['year'] +'-' + file_visa['month']
#print (file_visa['exp_month'])
file_visa = file_visa.filter(['exp_month','item','amount','cardno'])
print (file_visa.tail())


# In[250]:


file_master = pd.DataFrame(columns = ['date','item','amount','blank','cardno'])
print (file_master)
path = 'CardT*.csv'
FileNo = 1
for fname in glob.glob(path):
    f= pd.read_csv(fname,skiprows =[0,1,2], skipfooter = 8, names = ['date','item','amount','blank','cardno'])
    print (f.head())
    print ('breakline 1---------------- File #',FileNo)
    file_master = pd.concat([file_master,f])
    print (file_master.tail())
    print('breakline 2 -----------------')
    FileNo = FileNo+1


# In[251]:


file_master['date'] = [x[-10:] for x in file_master['date']]
print (file_master['date'])
file_master['month']= [x[-7:-5] for x in file_master['date']]
print (file_master['month'])
file_master['year']= [x[-4:] for x in file_master['date']]
print (file_master['year'])
file_master['day']= [x[-10:-8] for x in file_master['date']]
print (file_master['day'])
file_master['exp_month'] = file_master['year'] +'-' + file_master['month']
print (file_master['exp_month'])


# In[252]:


file_master['cardno'] = 'SCB_Master'
print ( file_master.groupby(['cardno']).count())
file_master = file_master.drop_duplicates()
print ( file_master.groupby(['cardno']).count())
file_master['amount1'] = [float(x[3:-3])*-1 for x in file_master['amount']]
file_master['amount2'] = [x[-2:] for x in file_master['amount']]
file_master['amount'] = file_master['amount1']
file_master = file_master.loc[file_master['amount2'] == 'DR'] 
file_master = file_master.filter(['exp_month','item','amount','cardno']) 
print (file_master)


# In[253]:


expenses = pd.DataFrame()
expenses = pd.concat([file_master,file_visa], ignore_index = True)
print (expenses)


# In[254]:


def shorter(x):
    if len(x.split(' ',1)[0] + ' ' + x.split(' ',2)[1]) >= 5:
        result = x.split(' ',1)[0] + ' ' + x.split(' ',2)[1]
    else:
        result = x.split(' ',1)[0] + ' ' + x.split(' ',2)[1] + ' ' + x.split(' ',3)[2]
    return result
expenses['cat']=[shorter(x) for x in expenses['item']]
print (expenses['cat'])


# In[255]:


lookup = expenses.groupby(['exp_month']).count()

print (lookup)


# In[256]:


lookup.to_csv('lookup_agg.csv')


# In[257]:


expenses_lookup = pd.read_csv('expenses_lookup.csv')
expenses

