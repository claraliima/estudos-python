import pandas as pd 

# crie duas listas com pelo menos 10 em elementos cada uma (uma lista numérica e outra com texto);
numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
letras = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

# converta-as em series;
serie1 = pd.Series(letras, index=numeros) # atribua índice alfabético para uma delas;
serie2 = pd.Series(numeros, index=letras)

# exiba todo o conteúdo delas;
print(serie1, serie2)

# some um em todos os dígitos na serie numérica;
serie2 = serie2 + 1 

# exiba 0s 6 primeiros elementos da serie do tipo string;
print(serie1.head(6))

# exiba os 7 últimos elementos da serie numérica;
print(serie2.tail(7))

# converta as series em dicionário;
serie1_dicionario = serie1.to_dict()
serie2_dicionario = serie2.to_dict()

# exiba os dicionários.
print(serie1_dicionario, serie2_dicionario)

