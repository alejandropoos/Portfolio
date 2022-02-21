from atlassian import Jira

Email = ''       #Mail del usuario con el que se va a loguear en Jira (tiene que tener permisos de ver el proyecto)
API_Token = ''      #API Token de un usuario en Jira
URL_base= ''      #URL base de proyecto Jira (Ej: https://xxxxxxxx.atlassian.net)

jira = Jira(url=URL_base, username=Email, password=API_Token)

#MODIFICAR JQL PARA QUE SOLO TRAIGA LOS TICKETS FILTRADOS COMO NECESITES
JQL = 'project = SSHP AND "Squad[Dropdown]" = "Support SMO" AND assignee is empty AND resolution = Unresolved AND (status IN ("Waiting for support")) AND summary !~ "Baja" AND summary !~ "Encontramos" AND summary !~ "estoque" AND summary !~ "stock" AND summary !~ "NÃO AUTORIZADO" AND summary !~ "sem" AND summary !~ "Baixa"  AND summary !~ "Rejeição" AND summary !~ "Pedido" AND summary !~ "Retiros" AND ("Request Type" in ("Cuarentena - Emisión Nota Fiscal") or "Request Type" in ("Taxes - CTe")) ORDER BY priority DESC'

try:
    data = jira.jql(JQL, fields='key', limit=500)
except Exception:
    print('Error de Autenticacion. Ingrese Mail y API Token correctos.')

issues = data['issues']

for issue in issues:
    key = issue['key']
    with open('tickets.txt', 'a') as f:
        f.write(key + '\n')