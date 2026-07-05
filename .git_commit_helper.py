import subprocess
from pathlib import Path
p = Path('commit_msg.txt')
msg = 'Refactor: remove legacy analyze-room endpoint; remove Analizar con IA UI; centralize IA in LumiBot; add salon filters; rebuild frontend; audit Configuracion'
p.write_text(msg, encoding='utf-8')
subprocess.run(['git', 'add', '-A'])
res = subprocess.run(['git', 'commit', '-F', str(p)])
print('returncode', res.returncode)
