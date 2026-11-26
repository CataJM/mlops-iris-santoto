import subprocess,sys,argparse
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--sin-preparar',action='store_true'); args=p.parse_args()
root=Path(__file__).resolve().parent
for directory in ('data', 'models', 'reports'):
    (root / directory).mkdir(parents=True, exist_ok=True)
stages=[('Preparar',['src/prepare.py']),('Validar',['src/validate_data.py']),('Entrenar',['src/train.py']),('Probar',['-m','pytest','-q','tests'])]
for name,cmd in stages:
    if name=='Preparar' and args.sin_preparar: continue
    print(f'ETAPA: {name}',flush=True)
    r=subprocess.run([sys.executable,*cmd],cwd=root)
    if r.returncode: print(f'Pipeline detenido: {name}',flush=True); sys.exit(r.returncode)
print('PIPELINE FINALIZADO CORRECTAMENTE')
