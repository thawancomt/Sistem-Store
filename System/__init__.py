from datetime import datetime

# Suponhamos que seu timestamp seja 1643145028 (um exemplo qualquer)
timestamp = 1706199463.471797
data = datetime.fromtimestamp(timestamp)

# Formate a data conforme necessário
formato_data = data.strftime('%d/%m/%Y - %H:%M:%S')
print(formato_data)