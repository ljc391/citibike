from __future__  import print_function, division
import pylab as pl
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import os

%pylab inline

import os
import json
#s = json.load(open(os.getenv('PUI2016') + "/bikedata.json") )
#pl.rcParams.update(s)

os.getenv('PUI2016')
#os.getenv("PUIDATA")


def getCitiBikeCSV(datestring):
    print ("Downloading", datestring)
    if not os.path.isfile(os.getenv("PUIDATA") + "/" + datestring + "-citibike-tripdata.csv"):
        if os.path.isfile(datestring + "-citibike-tripdata.csv"):
            if os.system("mv " + datestring + "-citibike-tripdata.csv " + os.getenv("PUIDATA")):
                print ("Error moving file!, Please check!")
        else:
            if not os.path.isfile(os.getenv("PUIDATA") + "/" + datestring + "-citibike-tripdata.zip"):
                if not os.path.isfile(datestring + "-citibike-tripdata.zip"):
                    os.system("curl -O https://s3.amazonaws.com/tripdata/" + datestring + "-citibike-tripdata.zip")
                os.system("mkdir " + os.getenv("PUIDATA"))
                os.system("mv " + datestring + "-citibike-tripdata.zip " + os.getenv("PUIDATA"))
            os.system("unzip " + os.getenv("PUIDATA") + "/" + datestring + "-citibike-tripdata.zip -d " + os.getenv("PUIDATA"))
            if '2014' in datestring:
                os.system("mv " + datestring[:4] + '-' +  datestring[4:] + 
                          "\ -\ Citi\ Bike\ trip\ data.csv " + datestring + "-citibike-tripdata.csv")
                os.system("mv " + datestring + "-citibike-tripdata.csv " + os.getenv("PUIDATA"))
    if not os.path.isfile(os.getenv("PUIDATA") + "/" + datestring + "-citibike-tripdata.csv"):
        print ("WARNING!!! something is wrong: the file is not there!")

    else:
        print ("file in place, you can continue")

datestring = '201601'
getCitiBikeCSV(datestring)

df=pd.read_csv(os.getenv("PUIDATA") + "/" + datestring + '-citibike-tripdata.csv')

#woman who ride bike 
#female = df[['gender', 'birth year']]  
female = df[(df['gender']==2)]
female = female[['birth year']] .groupby(female['birth year']).count()

#sum of the woman who ride bicycle yunger than 25
sum(female['birth year'][1991:2000])

#sum of the woman who ride bicycle order than 25
sum(female['birth year'][:1990])

# for plot
female['birth year'].head()

#sum of the man who ride bicycle yunger than 25
sum(male['birth year'][1991:2000])

#sum of the w0man who ride bicycle order than 25
sum(male['birth year'][:1990])

# for plot
male['birth year'].head()

fig=pl.figure(figsize(15,15))

#instad of plotting with matplotlib i.e. plot() i use the plot method in pandas
 
ax =(male['birth year']).plot(kind="bar",color='IndianRed',  alpha=0.5)
(female['birth year']).plot(kind="bar" ,     alpha=0.5)
ax.set_ylabel ("Number of rides")
ax.set_xlabel ("Years")
pl.legend(['men bikers','women bikers'],fontsize=20)

fig=pl.figure(figsize(15,15))

#instad of plotting with matplotlib i.e. plot() i use the plot method in pandas
norm_m = 1
error_m = np.sqrt(male['birth year'])
ax =(male['birth year']).plot(kind="bar",color='IndianRed',yerr=[ ((error_m) / norm_m, (error_m) / norm_m)],  alpha=0.5)
norm_w = 1
error_w = np.sqrt(female['birth year'])
(female['birth year']).plot(kind="bar" ,yerr=[ ((error_w) / norm_w, (error_w) / norm_w)],    alpha=0.5)
ax.set_ylabel ("Number of rides")
ax.set_xlabel ("Years")
pl.legend(['men bikers ','women bikers'],fontsize=20)



#instad of plotting with matplotlib i.e. plot() i use the plot method in pandas
norm_m = male['birth year'].sum()
error_m = np.sqrt(male['birth year'])
ax =(male['birth year']/ norm_m).plot(kind="bar",color='IndianRed',yerr=[ ((error_m) / norm_m, (error_m) / norm_m)],  alpha=0.5)
norm_w = female['birth year'].sum()
error_w = np.sqrt(female['birth year'])
(female['birth year']/ norm_w).plot(kind="bar" ,yerr=[ ((error_w) / norm_w, (error_w) / norm_w)],    alpha=0.5)
ax.set_ylabel ("Fraction of rides")
ax.set_xlabel ("Years")
pl.legend(['men bikers ','women bikers'],fontsize=20)

fig = pl.figure(figsize(15,6))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax1.set_xticks([])
ax2.set_xticks([])
old_w = sum(female['birth year'][1926:1990]) * 1.0 / norm_w
young_w = sum(female['birth year'][1991:2000]) * 1.0 / norm_w
eold_w = np.sqrt(sum(error_w[1926:1990]**2)) / norm_w
eyoung_w = np.sqrt(sum(error_w[1991:2000]**2)) / norm_w

old_m = sum(male['birth year'][1926:1990]) * 1.0 / norm_m
young_m = sum(male['birth year'][1991:2000]) * 1.0 / norm_m
eold_m = np.sqrt(sum(error_m[1926:1990]**2)) / norm_m
eyoung_m = np.sqrt(sum(error_m[1991:2000]**2)) / norm_m

print("Men: old:{0:.3f}, young:{1:.3f}, young error:{2:.3f}, young error:{3:.3f}"\
      .format(old_m, young_m, eold_m, young_m))
print("Women: old:{0:.3f}, young:{1:.3f}, young error:{2:.3f}, young error:{3:.3f}"\
      .format(old_w, young_w, eold_w, young_w))

ax1.errorbar([0.4], [old_m], yerr=[eold_m], fmt='o', label='men')
ax1.errorbar([0.2], [old_w], yerr=[eold_w], fmt='o', label='women')
ax1.set_xlim(0, 0.5)
ax2.errorbar([0.4], [young_m], yerr=[eyoung_m], fmt='o', label='men')
ax2.errorbar([0.2], [young_w], yerr=[eyoung_w], fmt='o', label='women')
ax1.set_xlim(0, 0.5)
ax1.set_title("older than 25")
ax2.set_title("younger than 25")
ax2.set_ylabel("Fraction of normalized rides by gender")
ax1.set_ylabel("Fraction of normalized rides by gender")

pl.xlim(-0.5, 1.5)
pl.legend(fontsize = 20)
