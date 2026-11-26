import json, hashlib, platform
import pandas as pd
import mlflow, mlflow.sklearn, joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,f1_score
from pathlib import Path
C=json.loads(Path('data_contract.json').read_text()); cols=list(C['features'])
a=pd.read_csv('data/train.csv'); b=pd.read_csv('data/test.csv')
model=RandomForestClassifier(n_estimators=100,max_depth=None,random_state=42)
mlflow.set_tracking_uri('sqlite:///mlflow.db'); mlflow.set_experiment('Proyecto_Final_Grado')
with mlflow.start_run(run_name='Pipeline_Iris') as run:
    model.fit(a[cols],a.species); pred=model.predict(b[cols])
    metrics={'accuracy':accuracy_score(b.species,pred),'f1_macro':f1_score(b.species,pred,average='macro'),'accuracy_train':model.score(a[cols],a.species)}
    mlflow.log_params({'n_estimators':100,'max_depth':'None','split_seed':42,'model_seed':42,'test_size':.2,'stratified':True})
    mlflow.log_metrics(metrics); mlflow.set_tag('python',platform.python_version())
    for name in ['train','test']: mlflow.set_tag(name+'_sha256',hashlib.sha256(Path(f'data/{name}.csv').read_bytes()).hexdigest())
    mlflow.sklearn.log_model(model,artifact_path='iris_model',input_example=a[cols].head(2))
    for f in ['requirements.txt','data_contract.json']: mlflow.log_artifact(f)
    joblib.dump(model,'models/model.pkl')
    Path('reports/metrics.json').write_text(json.dumps({**metrics,'run_id':run.info.run_id},indent=2))
    print(metrics,run.info.run_id)
