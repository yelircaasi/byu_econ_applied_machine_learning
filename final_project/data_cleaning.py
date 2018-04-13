# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 21:25:29 2018

@author: iriley

Cleans up the raw data file and outputs a csv that will be easier to work with.
"""

import os
import sys
sys.path.append('r:\\joepriceresearch\\python\\anaconda3\\lib\\site-packages')
import pandas as pd
import numpy as np


#loc = 'C:\\Users\\iriley\\Google Drive\\B. Asistente de investigación\\Dr. Baum\\
        ###SACMEQ. PASEC private school analysis\\Data\\SACMEQ15_final.csv'
loc = 'C:\\Users\\iriley\\Downloads\\SACMEQ15_final.csv'

#import list of variables in dataset and delete empty strings
cols_ = open('colnames.txt', 'r').read().split('\n')
cols_ = [c for c in cols_ if c != '']

#divide the variables into groups and decide which ones we can already drop
zcols = [c for c in cols_ if c[0]=='z' or c[0]=='Z']
zcols = [c for c in zcols if c[1] not in ['h','w','']]
zcols = [c for c in zcols if 'hiv' not in c and 'hin' not in c and 'htest' not in c and 
         'hcr' not in c and 'hinf' not in c]
xcols = [c for c in cols_ if c[0]=='x' or c[0]=='X']
ycols = [c for c in cols_ if c[0]=='y' or c[0]=='Y']
idcols = ['COUNTRY', 'REGION', 'DISTRICT', 'SCHOOL', 'PUPIL', 'PCLASS', 'idpupil', 'idschool', 
          'class', 'stratum', 'strsize', 'enr6', 'difenr', 'difenr2', 'numstu', 'xnumstu', 
          'prob1', 'RF1', 'pweight1', 'RF2', 'pweight2', 'achieved', 'pweighta']
pcols = [c for c in cols_ if c[0]=='p' or c[0]=='P' and c not in idcols]
pcols = [c for c in pcols if 'HINFO' not in c and 'HCLS' not in c and 'HLTH' not in c]
scols = [c for c in cols_ if c[0]=='s' or c[0]=='S' and c not in idcols]
allcols = [zcols,xcols,ycols,idcols,pcols,scols]
cols = zcols+xcols+ycols+idcols+pcols+scols
print([len(a) for a in allcols])

#now I can actually import the dataset
df_ = pd.read_csv(loc, usecols = cols)

#I need to find the columns with string values to take care of
probcols = [c for c in cols if df_[c].dtype==object]

#I also define 2 functions to make repetitive work easier
def showunique(collist, dataframe=df_):
    '''
    shows the number of unique values in a factor
    '''
    for c in collist:
        print(c+':\t', dataframe[c].unique())


def uniqueset(collist, dataframe=df_):
    '''
    shows the number of distinct values across multiple factors
    '''
    temp = []
    for c in collist:
        temp.extend(list(dataframe[c].unique()))
    return set(temp)

#test out the function
showunique(probcols, df_)

#first I group some of the most common factors by their values to make replacing them faster
yesno = [c for c in probcols if 'YES' in df_[c].unique() and 'NO' in df_[c].unique() and 'NO CLASS LIBRARY' not in df_[c].unique() and 'NO LIBRARY' not in df_[c].unique()]
yesno.extend([c for c in probcols if 'Yes' in df_[c].unique() and 'No' in df_[c].unique()])
yesno.extend([c for c in probcols if 'Y' in df_[c].unique() or 'N' in df_[c].unique()])
yesno.extend([c for c in probcols if 'Yes' in df_[c].unique() and 'No/Not sure' in df_[c].unique()])
lib = [c for c in probcols if 'NO CLASS LIBRARY' in df_[c].unique() or 'NO LIBRARY' in df_[c].unique()]
freq1 = [c for c in probcols if 'SOMETIMES' in df_[c].unique() and 'NEVER' in df_[c].unique() and 'OFTEN' in df_[c].unique()]
freq2 = [c for c in probcols if 'MOST OF THE TIME' in df_[c].unique()]# and 'ALL THE TIME' in df[c].unique()]
abcd = [c for c in probcols if 'A' in df_[c].unique() and 'B' in df_[c].unique()]
tick = [c for c in probcols if 'TICK' in df_[c].unique() and 'NO TICK' in df_[c].unique()]
days = [c for c in probcols if 'MOST DAYS' in df_[c].unique() and 'SOME DAYS' in df_[c].unique()]
othertime = [c for c in probcols if ('Never' in df_[c].unique() or 'NEVER' in df_[c].unique()) and c not in (freq1+freq2) and 2006 not in df_[c].unique()]
nums = [c for c in probcols if '1' in df_[c].unique() or '2' in df_[c].unique()]
have1_none = [c for c in probcols if 'Have at least one' in df_[c].unique()]
rare_often = [c for c in probcols if 'Never/a few times a year' in df_[c].unique()]
classletter = [c for c in probcols if 'E' in df_[c].unique() and  'F' in df_[c].unique()]

#now I can finally go through and replace the values with number values or create dummies
#the first step is to create the mappings
showunique(yesno)
uniqueset(yesno)
yesno_d = {'YES':1, 'NO':0, 'Yes':1, 'No':0, 'Y':1, 'N':0, 'No/Not sure':0, "I DON'T KNOW":0.5, 
           'NOT SURE':0.5, 'nan':-1, "DON'T KNOW":0.5, 'DK':0.5}
showunique(lib)
uniqueset(lib)
lib_d = {'YES':1, 'NO':0, 'NO CLASS LIBRARY':-1, 'NO LIBRARY':-1, 'NOT ALLOWED TO BORROW':0, 'ALLOWED TO BORROW':1}
showunique(freq1)
uniqueset(freq1)
freq1_d = {'SOMETIMES':1, 'OFTEN':2, 'NEVER':0}
showunique(freq2)
uniqueset(freq2)
freq2_d = {'SOMETIMES':1, 'MOST OF THE TIME':2, 'NEVER':0, 'NO HOMEWORK':-1, 'ALL THE TIME':3}
showunique(abcd)
uniqueset(abcd)
abcd_d = {'A':1, 'B':2, 'C':3, 'D':4, 'nan':0, '.a':0, 'MULTIPLE RESPONSE':0}
showunique(tick)
uniqueset(tick)
tick_d = {'TICK':1, 'NO TICK':0, 'nan':0}
showunique(days)
uniqueset(days)
days_d = {'MOST DAYS':2, 'SOME DAYS':1, 'NEVER':0}
showunique(othertime)
uniqueset(othertime)
othertime_d = {'NEVER':0, 'Never':0, 'Sometimes/Often':1, 'nan':-1, 'SOME DAYS':1, 
               'MOST DAYS':2, 'ONCE':1, 'TWICE':2, 'THREE PLUS':3, 'A FEW TIMES A WK':1, 'A FEW TIMES A YR':3, 
               'A FEW TIMES A MNTH':2, 'ONCE A TERM':2, 'ONCE OR MORE PER MONTH':3, 'ONCE PER YEAR':1, 
               'Sometimes/Most of the time/All the time':1, 'A few months':1, 'One year':2, 'Two years':3, 
               'Three years or more':4, 'At least once per year':1, 'ONCE OR MORE A MONTH':3, 'A FEW MONTHS':1, 
               'TWO YEARS':3, 'ONE YEAR':2, 'THREE OR MORE YEARS':4, 'ONCE A YEAR':1, 'Some days/Most days':1, 
               'ONCE PER TERM':2, 'I AM THE SCHOOL HEAD':4}
showunique(nums)
uniqueset(nums)
nums_d = {'1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '.a':-1}
showunique(have1_none)
uniqueset(have1_none)
have1_none_d = {'nan':-1, 'Have at least one':1, 'Do not have':0}
showunique(rare_often)
uniqueset(rare_often)
rare_often_d = {'A few times a month or a few times a week':1, 'Never/a few times a year':0, 'nan':-1}
showunique(classletter)
uniqueset(classletter)
classletter_d = {'nan':0, 'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8, 
                'I':9, 'J':10, 'K':11, 'L':12, 'M':13}
qmap = {'A':1, 'B':2, 'C':3, 'D':4, 'MULTIPLE RESPONSE':0, '.a':0, nan:0}

#now I can apply the mappings
df_[yesno] = df_[yesno].applymap(lambda s: yesno_d.get(s) if s in yesno_d else s)
df_[lib] = df_[lib].applymap(lambda s: lib_d.get(s) if s in lib_d else s)
df_[freq1] = df_[freq1].applymap(lambda s: freq1_d.get(s) if s in freq1_d else s)
df_[freq2] = df_[freq2].applymap(lambda s: freq2_d.get(s) if s in freq2_d else s)
df_[abcd] = df_[abcd].applymap(lambda s: abcd_d.get(s) if s in abcd_d else s)
df_[tick] = df_[tick].applymap(lambda s: tick_d.get(s) if s in tick_d else s)
df_[days] = df_[days].applymap(lambda s: days_d.get(s) if s in days_d else s)
df_[othertime] = df_[othertime].applymap(lambda s: othertime_d.get(s) if s in othertime_d else s)
df_[nums] = df_[nums].applymap(lambda s: nums_d.get(s) if s in nums_d else s)
df_[have1_none] = df_[have1_none].applymap(lambda s: have1_none_d.get(s) if s in have1_none_d else s)
df_[rare_often] = df_[rare_often].applymap(lambda s: rare_often_d.get(s) if s in rare_often_d else s)
df_[classletter] = df_[classletter].applymap(lambda s: classletter_d.get(s) if s in classletter_d else s)

#let's have a look at the remaining problem factors
combined = yesno+lib+freq1+freq2+abcd+tick+days+othertime+nums+have1_none+rare_often+classletter
probsleft = [c for c in combined if df_[c].dtype==object]
df_[probsleft]
for c in combined:
    print(df_[c].dtype)

#and lets pull out a few to save for later
stype = df_['STYPE']
stype2 = df_['zstype']
math = df_['zmalocp']
reading = df_['zralocp']
stratum = df_['stratum']
classid = df_['SFCLASS']




#now we go through and do the dirty work, inspecting the factors and deciding which
    #will be made into dummies and which will be manually coded up
dummies = []
print(df_['zplight'].unique())
dummies.append('zplight')
print(df_['zplight'].unique())
dummies.append('zplight')
print(df_['zpfloor'].unique())
dummies.append('zpfloor')
print(df_['zpwall'].unique())
dummies.append('zpwall')
print(df_['zproof'].unique())
dummies.append('zproof')
print(df_['zpborowc'].unique())
df_['zpborows'].map({'Allowed':1, 'No library/Not allowed/Do not know':0})
print(df_['zpborows'].unique())
df_['zpborows'].map({'Allowed':1, 'No library/Not allowed/Do not know':0})
print(df_['zpsit'].unique())
df_['zpsit'].map({'I have my own sitting place':1, 'No place/share':0})
print(df_['zpwrite'].unique())
df_['zpwrite'].map({'I have my own writing place':1, 'No place/share':0})
print(df_['zpctaugh'].unique())
dummies.append('zpctaugh')
print(df_['zpmealsc'].unique())
df_['zpmealsc'].map({'Two or more per day':2, 'One per day':1, 'No':0})
print(df_['zpxtfreq'].unique())
df_['zpxtfreq'] = df_['zpxtfreq'].map({'I do not take extra tuition':0, '3 or more times per week':4, 'Once a month':1, 
                     'Once or twice per week':3, '2 or 3 times per month':2})
print(df_['zpextpay'].unique())
dummies.append('zpextpay')
print(df_['zpextwhy'].unique())
dummies.append('zpextwhy')
print(df_['zphmwk'].unique())
df_['zphmwk'].map({'No homework/1-2 per month/1-2 per week':0, 'Most days of the week':1})
print(df_['zphmwkc'].unique())
df_['zphmwkc'] = df_['zphmwkc'].map({'Most of time/Always corrects':2, 'Sometimes corrects':1, 'Never corrects':0, 'No homework':0})
print(df_['zphmwkhl'].unique())
dummies.append('zphmwkhl')
print(df_['zphmwks'].unique())
df_['zphmwks'] = df_['zphmwks'].map({'Most of time/Always explains':2, 'Sometimes explains':1, 'Never explains':0, 'No homework':0})
print(df_['zptextr'].unique())
df_['zptextr'] = df_['zptextr'].map({'Own textbook':1, 'No textbook/share':0})
print(df_['zptextm'].unique())
df_['zptextm'] = df_['zptextm'].map({'Own textbook':1, 'No textbook/share':0})
print(df_['zphclsbt'].unique())
dummies.append('zphclsbt')
print(df_['zposlev'].unique())
df_['zposlev'] = df_['zposlev'].map({'High SES':1, 'Low SES':0})
print(df_['zslocati'].unique())
dummies.append('zslocati')
print(df_['zsloc'].unique())
dummies.append('zsloc')
print(df_['zstype'].unique())
df_['zstype'] = df_.drop('zstype',axis=1)
print(df_['zsbldgco'].unique())
df_['zsbldgco'] = df_['zsbldgco'].map({'Minor repair/Good condition ':1, 'Complete rebuiding/Major repair':0})
print(df_['zsborrow'].unique())
df_['zsborrow'] = df_['zsborrow'].map({'Can borrow':1, 'Can not borrow':0})
print(df_['zshrisku'].unique())
df_['zshrisku'] = df_['zshrisku'].map({'High/very high':1, 'No risk/low/medium':0})
print(df_['zshriskt'].unique())
df_['zshriskt'] = df_['zshriskt'].map({'High/very high':1, 'No risk/low/medium':0})
print(df_['zxresuse'].unique())
df_['zxresuse'] = df_['zxresuse'].map({'Not used':0, 'Used':1})
print(df_['zyresuse'].unique())
df_['zyresuse'] = df_['zyresuse'].map({'Not used':0, 'Used':1})
print(df_['zxcondli'].unique())
df_['zxcondli'] = df_['zxcondli'].map({'Minor repair/Good condition ':1, 'Poor/Major repair':0})
print(df_['zycondli'].unique())
df_['zycondli'] = df_['zycondli'].map({'Minor repair/Good condition ':1, 'Poor/Major repair':0})
print(df_['zxtest'].unique())
df_['zxtest'] = df_['zxtest'].map({'3 times or less per term':1, '2-3 times per month':2, 'Once or more per week':3})
print(df_['zytest'].unique())
df_['zytest'] = df_['zytest'].map({'3 times or less per term':1, '2-3 times per month':2, 'Once or more per week':3})
print(df_['zxhrisku'].unique())
df_['zxhrisku'] = df_['zxhrisku'].map({'No risk/low/medium':0, 'High/very high':1})
print(df_['zxhriskt'].unique())
df_['zxhriskt'] = df_['zxhriskt'].map({'No risk/low/medium':0, 'High/very high':1})
print(df_['zyhrisku'].unique())
df_['zyhrisku'] = df_['zyhrisku'].map({'No risk/low/medium':0, 'High/very high':1})
print(df_['zyhriskt'].unique())
df_['zyhriskt'] = df_['zyhriskt'].map({'No risk/low/medium':0, 'High/very high':1})
print(df_['ZPSESLV2'].unique())
df_['ZPSESLV2'] = df_['ZPSESLV2'].map({'PSES-Top quarter':3, 'PSES-Middle half':2, 'PSES-Bottom quarter ':1})
print(df_['ZPSESLV3'].unique())
df_['ZPSESLV3'] = df_['ZPSESLV3'].map({'PSES-Top quarter':3, 'PSES-Middle half':2, 'PSES-Bottom quarter ':1})
print(df_['XSEX'].unique())
df_['XSEX'] = df_['XSEX'].map({'MALE':0, 'FEMALE':1})
print(df_['XQPERMNT'].unique())
dummies.append('XQPERMNT')
print(df_['XQACADEM'].unique())
df_['XQACADEM'] = df_['XQACADEM'].map({'SENIOR SECONDARY':3, 'JUNIOR SECONDARY':2, 'FIRST DEGREE':5, 'A-LEVEL':4, 'PRIMARY':1})
print(df_['XQPROFES'].unique())
df_['XQPROFES'] = df_['XQPROFES'].map({'3 YRS TT':3, '2 YRS TT':2, '>3 YRS TT':4, '1 YR TT':1, 'NO TT':0, '<1 YR TT':0.5})
print(df_['XINSERVE'].unique())
df_['XINSERVE'] = df_['XINSERVE'].map({'NO IN-SERVICE COURSE':0, 'VERY EFFECTIVE':4, 'REASONABLY EFFECTIVE':2,
                                       'EFFECTIVE':3, 'NOT EFFECTIVE':1})
print(df_['XRCVISIT'].unique())
dummies.append('XRCVISIT')
print(df_['XCONDLIV'].unique())
df_['XCONDLIV'] = df_['XCONDLIV'].map({'MINOR REPAIRS':2, 'NEED MAJOR REPAIRS':1, 'POOR':0, 'GOOD CONDITION':3})
print(df_['XTEST'].unique())
df_['XTEST'] = df_['XTEST'].map({'2-3/TERM':3, '2-3/MONTH':4, '1 OR MORE/WK':5, '1/TERM':2, '1/YR':1, 'NO TESTS':0})
print(df_['YSEX'].unique())
df_['YSEX'] = df_['YSEX'].map({'MALE':0, 'FEMALE':1})
print(df_['YQPERMNT'].unique())
dummies.append('YQPERMNT')
print(df_['YQACADEM'].unique())
df_['YQACADEM'] = df_['YQACADEM'].map({'SENIOR SECONDARY':3, 'JUNIOR SECONDARY':2, 'FIRST DEGREE':5, 'A-LEVEL':4, 'PRIMARY':1})
print(df_['YQPROFES'].unique())
df_['YQPROFES'] = df_['YQPROFES'].map({'3 YRS TT':3, '2 YRS TT':2, '>3 YRS TT':4, '1 YR TT':1, 'NO TT':0, '<1 YR TT':0.5})
print(df_['YINSERVE'].unique())
df_['YINSERVE'] = df_['YINSERVE'].map({'NO IN-SERVICE COURSE':0, 'VERY EFFECTIVE':4, 'REASONABLY EFFECTIVE':2,
                                       'EFFECTIVE':3, 'NOT EFFECTIVE':1})
print(df_['YRCVISIT'].unique())
dummies.append('YRCVISIT')
print(df_['YCONDLIV'].unique())
df_['YCONDLIV'] = df_['YCONDLIV'].map({'MINOR REPAIRS':2, 'NEED MAJOR REPAIRS':1, 'POOR':0, 'GOOD CONDITION':3})
print(df_['YTEST'].unique())
df_['YTEST'] = df_['YTEST'].map({'2-3/TERM':3, '2-3/MONTH':4, '1 OR MORE/WK':5, '1/TERM':2, '1/YR':1, 'NO TESTS':0})
print(df_['COUNTRY'].unique())
dummies.append('COUNTRY')
print(df_['REGION'].unique())
dummies.append('REGION')
print(df_['DISTRICT'].unique())
dummies.append('DISTRICT')
print(df_['stratum'].unique())
dummies.append('stratum')
print(df_['PSEX'].unique())
df_['PSEX'] = df_['PSEX'].map({'BOY':0, 'GIRL':1})
print(df_['PPSTAY'].unique())
dummies.append('PPSTAY')
print(df_['PTRAVEL'].unique())
df_['PTRAVEL'] = df_['PTRAVEL'].map({'>0.5-1KM':2,  '>1-1.5KM':3,  'UP TO 0.5KM':1,  '>3-3.5KM':7,  '>2.5-3KM':6, '>3.5-4KM':8,
                                     '>2-2.5KM':5, '>4KM-4.5KM':9, '>1.5-2KM':4, '>4.5-5KM':10, '>5KM':11})
print(df_['PTRAVEL2'].unique())
dummies.append('PTRAVEL2')
print(df_['PMOTHER'].unique())
df_['PMOTHER'] = df_['PMOTHER'].map({'I Do Not Have a Mother':0, 'I Do Not Know':np.nan, 'Completed All Secondary':4,
                                     'Completed Some Primary':1, 'Completed All Primary':2, 'Completed Training After Secondary':5, 
                                     'No School, No Adult Education':0.5, 'Completed Some Secondary':3, 'No School, Some Adult Education':3,
                                     'Some Training After Primary':3, 'Completed Some University':5, 'Completed University Degree':6})
print(df_['PFATHER'].unique())
df_['PFATHER'] = df_['PFATHER'].map({'I Do Not Have a Father':0, 'I Do Not Know':np.nan, 'Completed All Secondary':4,
                                     'Completed Some Primary':1, 'Completed All Primary':2, 'Completed Training After Secondary':5, 
                                     'No School, No Adult Education':0.5, 'Completed Some Secondary':3, 'No School, Some Adult Education':3,
                                     'Some Training After Primary':3, 'Completed Some University':5, 'Completed University Degree':6})
print(df_['PLIGHT'].unique())
dummies.append('PLIGHT')
print(df_['PFLOOR'].unique())
dummies.append('PFLOOR')
print(df_['PWALL'].unique())
dummies.append('PWALL')
print(df_['PROOF'].unique())
dummies.append('PROOF')
print(df_['PBORROWS'].unique())
df_['PBORROWS'] = df_['PBORROWS'].map({'ALLOWED TO BORROW':1, 'NO SCHOOL LIBRARY':0, 'NOT ALLOWED TO BORROW':0})
print(df_['PSIT'].unique())
dummies.append('PSIT')
print(df_['PWRITE'].unique())
dummies.append('PWRITE')
print(df_['PCTAUGHT'].unique())
dummies.append('PCTAUGHT')
print(df_['PMEAL1'].unique())
df_['PMEAL1'] = df_['PMEAL1'].map({'1-2DAYS/WEEK':1, '3-4DAYS/WEEK':2, 'EVERY DAY':3, 'NOT AT ALL':0})
print(df_['PMEAL2'].unique())
df_['PMEAL2'] = df_['PMEAL2'].map({'1-2DAYS/WEEK':1, '3-4DAYS/WEEK':2, 'EVERY DAY':3, 'NOT AT ALL':0})
print(df_['PMEAL3'].unique())
df_['PMEAL3'] = df_['PMEAL3'].map({'1-2DAYS/WEEK':1, '3-4DAYS/WEEK':2, 'EVERY DAY':3, 'NOT AT ALL':0})
print(df_['PMEALSCH'].unique())
df_['PMEALSCH'] = df_['PMEALSCH'].map({'YES, 2 OR MORE PER DAY':2, 'YES, 1 PER DAY':1, 'NO':0})
print(df_['PXTFREQ'].unique())
df_['PXTFREQ'] = df_['PXTFREQ'].map({'3ORMORE/WK':4, '1/MNT':1, '1 OR 2/WK':3, '2 OR 3/MNTH':2})
print(df_['PEXTPAY'].unique())
dummies.append('PEXTPAY')
print(df_['PEXTWHY'].unique())
dummies.append('PEXTWHY')
print(df_['PHMWK'].unique())
df_['PHMWK'] = df_['PHMWK'].map({'1-2/WEEK':2, '1-2/MONTH':1, 'MOST DAYS':3, 'NO HOMEWORK':0})
print(df_['PHMWKC'].unique())
df_['PHMWKC'] = df_['PHMWKC'].map({'ALWAYS':3, 'MOST':2, 'SOMETIMES':1, 'NEVER CORRECTS':0, 'NO HOMEWORK':0})
print(df_['PHMWKS'].unique())
df_['PHMWKS'] = df_['PHMWKS'].map({'ALWAYS':3, 'SOMETIMES':1, 'MOST':2, 'NEVER EXPLAINS':0, 'NO HOMEWORK':0})
print(df_['PTEXTR'].unique())
dummies.append('PTEXTR')
print(df_['PTEXTM'].unique())
df_['PTEXTM'] = df_['PTEXTM'].map({'USE BY MYSELF':4, 'SHARE WITH 1':3, 'NO MATH TEXTBOOKS':0, 'SHARE WITH 2+':2, 'ONLY TEACHER':1})
print(df_['PHFRIEND'].unique())
dummies.append('PHFRIEND')
print(df_['PFCLASS'].unique())
#ID
print(df_['PFSEX'].unique())
df_['PFSEX'] = df_['PFSEX'].map({'B':0, 'G':1})
print(df_['stratum'].unique())
print(df_['STYPE'].unique())
df_ = df_.drop('STYPE',axis=1)
print(df_['SLEVELS'].unique())
dummies.append('SLEVELS')
print(df_['SLOCAT'].unique())
dummies.append('SLOCAT')
print(df_['SSEX'].unique())
df_['SSEX'] = df_['SSEX'].map({'FEMALE':0, 'MALE':1})
print(df_['SQACADEM'].unique())
df_['SQACADEM'] = df_['SQACADEM'].map({'JUNIOR SEC':2, 'TERTIARY ED':5, 'PRIMARY':1, 'SENIOR SEC':3, 'A-LEVEL':4})
print(df_['SQTT'].unique())
df_['SQTT'] = df_['SQTT'].map({'2 YEARS':2, 'MORE THAN 3 YRS':4, '3 YEARS':3, '1 YEAR':1, 'NO TT':0, 'LESS THAN 1 YR':0.5})
print(df_['SCONDIT'].unique())
df_['SCONDIT'] = df_['SCONDIT'].map({'SOME MINOR REPAIRS':3, 'SOME MAJOR REPAIRS':1, 'GOOD CONDITION':4, 
                                     'ALL MINOR REPAIRS':2, 'NEEDS REBUILDING':0})
print(df_['SPROBCOM'].unique())
df_['SPROBCOM'] = df_['SPROBCOM'].map({'MINOR PROBLEM':1, 'NOT A PROBLEM':0, 'MAJOR PROBLEM':2})
print(df_['SYRINSP'].unique())
df_['SYRINSP'] = df_['SYRINSP'].map({'BEFORE 2003':5, '2005':2, '2003':4, '2006':1, '2007':0, '2004':3, 'NEVER':6, 2007:0, 
                                     2005:2, 2006:1, 2003:4, 2004:3})
print(df_['SSFP'].unique())
df_['SSFP'] = df_['SSFP'].map({'YES, 2 OR MORE/DAY':2, 'YES, 1/DAY':1, 'NO':0})
df_['SSFP_yn'] = df_['SSFP'].map({'YES, 2 OR MORE/DAY':1, 'YES, 1/DAY':1, 'NO':0})
print(df_['SFCLASS'].unique())
#TO IDS
print(df_['PBORROWC'].unique())
df_['PBORROWC'] = df_['PBORROWC'].map({'I DON"T KNOW':0})

print(df_['zpborowc'].unique())
df_['zpborowc'] = df_['zpborowc'].map({'No library/Not allowed/Do not know':0, 'Allowed':1})
print(df_['zpborows'].unique())
df_['zpborows'] = df_['zpborows'].map({'No library/Not allowed/Do not know':0, 'Allowed':1})
print(df_['zpsit'].unique())
df_['zpsit'] = df_['zpsit'].map({'I have my own sitting place':1, 'No place/share':0})
print(df_['zpwrite'].unique())
df_['zpwrite'] = df_['zpwrite'].map({'I have my own writing place':1, 'No place/share':0})
print(df_['zpmealsc'].unique())
df_['zpmealsc'] = df_['zpmealsc'].map({'Two or more per day':2, 'One per day':1, 'No':0})
print(df_['zphmwk'].unique())
df_['zphmwk'] = df_['zphmwk'].map({'No homework/1-2 per month/1-2 per week':0, 'Most days of the week':1})
print(df_['zstype'].unique())
df_ = df_.drop('zstype')

#now we create the dummies
df = pd.get_dummies(data=df_, columns=dummies)

#one last check
l = list(df.columns.values)
probsleft2 = [c for c in l if df[c].dtype==object]

#now, finally, we can save the dataset as a csv and begin the fun parts of our project
os.chdir('R:\\JoePriceResearch\\RA_work_folders\\Isaac_Riley')
df.to_csv('clean.csv')