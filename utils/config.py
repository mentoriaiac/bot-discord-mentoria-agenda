import json
from dateutil import tz

TZ = tz.gettz("America/Sao_Paulo")
EVENT_TEMPLATE = """```yml
Assunto: {}
Local: {}
Data: {} - Hora de Brasilia
```
"""



with open('config.json') as f:
    config = json.load(f)


