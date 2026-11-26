import csv,json,math,sys
from pathlib import Path
C=json.loads(Path('data_contract.json').read_text())
def validate_input(row):
    errors=[]
    if set(row)!=set(C['features']): errors.append('Estructura incorrecta')
    for k,r in C['features'].items():
        v=row.get(k)
        if v is None or v=='': errors.append(f'{k}: nulo'); continue
        if type(v) not in (int,float) or not math.isfinite(v): errors.append(f'{k}: tipo numérico inválido'); continue
        if not r['minimum']<=v<=r['maximum']: errors.append(f'{k}: fuera de rango')
    return errors

def validate_file(path):
    errors=[]; ids=set(); classes=set()
    with open(path,newline='') as f:
        reader=csv.DictReader(f)
        expected=[*C['features'],'species','row_id']
        if reader.fieldnames!=expected: return ['Encabezado incorrecto'],ids
        for i,row in enumerate(reader,2):
            if None in row: errors.append(f'Fila {i}: columnas adicionales')
            values={}
            for k in C['features']:
                v=row[k]
                try: values[k]=float(v) if v not in ('',None) else None
                except ValueError: values[k]=v
            errors.extend(f'Fila {i}: {e}' for e in validate_input(values))
            try:
                target=int(row['species']); idx=int(row['row_id'])
                if target not in C['training_target']['allowed']: raise ValueError()
                if idx<0 or idx>=150 or idx in ids: errors.append(f'Fila {i}: ID inválido o repetido')
                ids.add(idx); classes.add(target)
            except (ValueError,TypeError): errors.append(f'Fila {i}: clase o ID inválido')
    if classes!={0,1,2}: errors.append('Faltan clases')
    if len(ids)!=(120 if 'train' in str(path) else 30): errors.append('Tamaño inesperado')
    return errors,ids
if __name__=='__main__':
    a,ia=validate_file('data/train.csv'); b,ib=validate_file('data/test.csv')
    errors=a+b
    if ia & ib: errors.append('Fuga de datos: IDs compartidos')
    if errors: print('\n'.join(errors)); sys.exit(1)
    print('Validación aprobada: tipos, nulos, rangos, clases, estructura e IDs')
