import sys,json
from pathlib import Path
import joblib,pandas as pd
from sklearn.metrics import accuracy_score
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from validate_data import validate_input,validate_file,C

def test_valid(): assert not validate_input(C['valid_example'])
def test_invalid(): assert validate_input(C['invalid_example'])
def test_null(): assert validate_input({**C['valid_example'],'petal_width':None})
def test_range(): assert validate_input({**C['valid_example'],'petal_width':-1})
def test_type(): assert validate_input({**C['valid_example'],'sepal_length':'cinco'})
def test_train(): assert not validate_file('data/train.csv')[0]
def test_test(): assert not validate_file('data/test.csv')[0]
def test_no_overlap(): assert not (validate_file('data/train.csv')[1]&validate_file('data/test.csv')[1])
def test_model(): assert joblib.load('models/model.pkl').n_features_in_==4
def test_accuracy():
    b=pd.read_csv('data/test.csv'); m=joblib.load('models/model.pkl'); assert accuracy_score(b.species,m.predict(b[list(C['features'])]))>=.8
