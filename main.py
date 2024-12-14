import os
import pandas as pd
import matplotlib.pyplot as plt

def process_energy_data(folder_path):
    # DataFrame do Pandas
    all_data = pd.DataFrame()

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt.phps"):
            # Formato da data
            date = file_name[:6]  
            day, month, year = date[:2], date[2:4], date[4:]
            formatted_date = f"{day}/{month}/20{year}" 

            file_path = os.path.join(anexos, file_name)

            # Ler os dados do arquivo
            with open(file_path, "r") as file:
                lines = file.readlines()

            # Processar as linhas para criar um DataFrame
            data = []
            for line in lines:
                values = line.strip().split(":")
                if len(values) == 23:  # Validar que a linha tem o número correto de colunas
                    time = f"{values[0]}:{values[1]}:{values[2]}"
                    row = [formatted_date, time] + list(map(float, values[3:]))
                    data.append(row)

            # Criar um DataFrame para este arquivo
            columns = ["Date", "Time", "pa", "pb", "pc", "pt", 
                       "epa_c", "epb_c", "epc_c", "ept_c", 
                       "epa_g", "epb_g", "epc_g", "ept_g", 
                       "iarms", "ibrms", "icrms", 
                       "uarms", "ubrms", "ucrms"]
            file_df = pd.DataFrame(data, columns=columns)

            # Concatenar ao DataFrame principal
            all_data = pd.concat([all_data, file_df], ignore_index=True)

    # Converter colunas de data e hora em formato datetime
    all_data["Datetime"] = pd.to_datetime(all_data["Date"] + " " + all_data["Time"], format="%d/%m/%Y %H:%M:%S")
    all_data.sort_values(by="Datetime", inplace=True)

    # Retornar o DataFrame processado
    return all_data

def plot_energy_data(data, columns_to_plot, title="Evolução dos Dados de Energia"):
    # Plotar os dados de evolução
    plt.figure(figsize=(14, 8))
    for column in columns_to_plot:
        plt.plot(data["Datetime"], data[column], label=column)
    
    plt.title(title)
    plt.xlabel("Tempo")
    plt.ylabel("Valores")
    plt.legend()
    plt.grid()
    plt.show()

# Caminho para a pasta onde estão os arquivos
folder_path = "caminho/para/a/pasta"

# Processar os dados
data = process_energy_data(folder_path)

# Selecionar colunas para plotar
columns_to_plot = ["pa", "pb", "pc", "pt"]

# Gerar os gráficos
plot_energy_data(data, columns_to_plot, title="Evolução das Potências")
