from pathlib import Path
import re

root = Path('c:/Users/USER/Documents/Cognitive/ICC/proyecto/Proyecto_Cognitive')
exts = {'.py', '.ts', '.tsx', '.md', '.sql', '.json', '.txt'}
exclude_dirs = {'frontend/dist'}

replacements = [
    (re.compile(r'ADMINISTRADOR'), 'ADMINISTRADOR'),
    (re.compile(r'Administrador'), 'Administrador'),
    (re.compile(r'administrador'), 'administrador'),
]

for path in root.rglob('*'):
    if not path.is_file():
        continue
    if path.suffix.lower() not in exts:
        continue
    if any(str(path).replace('\\','/').startswith(str(root / d).replace('\\','/') + '/') for d in exclude_dirs):
        continue
    try:
        text = path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    new_text = text
    for pattern, repl in replacements:
        new_text = pattern.sub(repl, new_text)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        print(f'updated {path.relative_to(root)}')
