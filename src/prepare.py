from pathlib import Path
import csv
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
X,y=load_iris(return_X_y=True)
a,b=train_test_split(list(range(len(y))),test_size=.2,random_state=42,stratify=y)
for name,indices in [('train',a),('test',b)]:
    with open(f'data/{name}.csv','w',newline='') as f:
        w=csv.writer(f); w.writerow(['sepal_length','sepal_width','petal_length','petal_width','species','row_id'])
        for i in indices: w.writerow([*X[i],y[i],i])
    print(name,len(indices))
