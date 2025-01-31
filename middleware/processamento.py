import pandas as pd
import math



def processar_arquivo(arquivo):
    try:
        # Lê o arquivo Excel
        dados_iniciais = pd.read_excel(arquivo, header=None)

        # Encontra a linha que contém "Conta" e define como cabeçalho
        header_row = None
        for i, row in dados_iniciais.iterrows():
            if 'Conta' in row.values:
                header_row = i
                break
        if header_row is None:
            raise ValueError("Cabeçalho 'Conta' não encontrado no arquivo.")

        # Lê novamente o arquivo com o cabeçalho dinâmico
        dados = pd.read_excel(arquivo, header=header_row)

        # Função auxiliar para concatenar valores sem gerar 'nan nan'
        def concatenar_valores(col1, col2):
            col1 = col1.fillna('').astype(str).str.strip()  # Remove espaços extras
            col2 = col2.fillna('').astype(str).str.strip()
            return col1 + " " + col2

        # Ajustes nas colunas de saldo
        if 'Unnamed: 2' in dados.columns and 'Saldo Anterior' in dados.columns:
            dados['Saldo Anterior'] = concatenar_valores(
                dados['Unnamed: 2'], dados['Saldo Anterior']
            )
        if 'Unnamed: 8' in dados.columns and 'Saldo Atual' in dados.columns:
            dados['Saldo Atual'] = concatenar_valores(
                dados['Unnamed: 8'], dados['Saldo Atual']
            )

        # Função auxiliar para ajustar o saldo
        def ajustar_saldo(valor):
            try:
                # Converte para string e limpa espaços extras
                valor = str(valor).strip()

                # Verificar se o formato é brasileiro com vírgula como separador decimal e pontos como separadores de milhar
                if ',' in valor and '.' in valor:
                    # Remove os pontos usados como separador de milhar e troca a vírgula pelo ponto decimal
                    valor = valor.replace('.', '').replace(',', '.')
                    print(f"Convertendo valor no formato brasileiro: {valor}")
                else:
                    # Caso contrário, mantém a lógica padrão
                    print(f"Valor no formato padrão: {valor}")

                # Tratar valores que terminam com 'C' ou 'D'
                if valor.endswith('D'):
                    valor = valor[:-1]  # Remove 'D' do fim
                    print(f"Removendo 'D': {valor}")
                elif valor.endswith('C'):
                    valor = f"-{valor[:-1]}"  # Remove 'C' do fim e torna negativo
                    print(f"Removendo 'C': {valor}")

                # Converte o valor para float
                valor = float(valor)  # Garante que seja um número válido

                # Use ceil apenas para números positivos e floor para números negativos
                if valor >= 0:
                    valor = math.ceil(valor)  # Arredonda para cima no caso de positivo
                else:
                    valor = math.floor(valor)  # Arredonda para baixo (mais negativo) no caso de negativo

                print(f"Valor convertido e arredondado: {valor}")

                return int(valor)  # Retorna como inteiro após arredondar
            except ValueError:
                # Caso o valor não seja válido, captura o erro
                print(f"Valor inválido ignorado: {valor}")
                return 0# Ignorar valores inválidos e substituir por 0

        # Aplicando a lógica para ajustar os saldos
        dados['Saldo Anterior'] = dados['Saldo Anterior'].apply(lambda x: ajustar_saldo(x))
        dados['Saldo Atual'] = dados['Saldo Atual'].apply(lambda x: ajustar_saldo(x))
        dados['Débitos'] = dados['Débitos'].apply(lambda x: ajustar_saldo(x))
        dados['Créditos'] = dados['Créditos'].apply(lambda x: ajustar_saldo(x))

        

        # Removendo colunas indesejadas
        colunas_para_remover = ['Unnamed: 2', 'Unnamed: 6', 'Unnamed: 8', " ", " .1"]
        dados.drop(columns=[col for col in colunas_para_remover if col in dados.columns], inplace=True)

        # Ajustes na coluna "Conta"
        dados['Conta'] = dados['Conta'].astype(str).str.replace('.', '', regex=False)
        dados['Conta'] = pd.to_numeric(dados['Conta'], errors='coerce')
        dados = dados.dropna(subset=['Conta'])
        dados['Conta'] = dados['Conta'].astype(int)

        return dados
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
        return None