import pandas as pd 

dados = {
    'nome_colunas' : ['aluno', 'turma', 'idade', 'escola', 'turno', '', '', '', '', ''],
    'alunos' : ['Clara', 'Gustavo', 'Souza', 'Tolentino', 'Filipe', 'Ana Clara', 'Ana Karolina', 'Ingrid', 'Henrique', 'Daniel'],
    'turmas' : ['1a', '2a', '3a', '1b', '2b', '3b', '1c', '2c', '3c', '1d'],
    'idade' : [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    'escolas' : ['Cotemig', 'Cotemig', 'Cotemig','Cotemig', 'Cotemig','Cotemig', 'Cotemig', 'Cotemig','Cotemig', 'Cotemig'],
    'turnos' : ['Manhã', 'Tarde', 'Noite', 'Manhã', 'Tarde', 'Noite', 'Manhã', 'Tarde', 'Noite', 'Noite']
}

indices = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I','J']

df = pd.DataFrame(dados, index=indices)
print(df)

# - Some 1 a todos os valores da coluna numérica
df.idade = df.idade + 1 
print(df)

# - Exiba as 2 primeiras linhas do DataFrame
print(df.head(2))

# - Exiba as 4 últimas linhas do DataFrame
print(df.tail(4))

# - Converta o DataFrame em um dicionário
# - Exiba o dicionário resultante
dicionario = df.to_dict()
print(dicionario)