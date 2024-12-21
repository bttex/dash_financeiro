# 🏦 **Dashboard Financeiro**

## 📊 Descrição

Este projeto é um **Dashboard Financeiro** interativo construído com **Streamlit** e **Altair**, que permite visualizar e analisar dados financeiros a partir de um arquivo CSV contendo informações sobre lançamentos financeiros, como entradas e saídas. A interface apresenta gráficos dinâmicos e cards com informações resumidas para facilitar a visualização dos dados.

## 🚀 Funcionalidades

- **Visão geral financeira**: Exibe o saldo final, o total de entradas e saídas.
- **Análise de entradas e saídas**: Gráficos que mostram as entradas e saídas por mês.
- **Evolução do saldo acumulado**: Visualização do saldo acumulado ao longo dos meses.
- **Análise por Histórico**: Exibe os totais por categoria de histórico financeiro (se disponível).
- **Detalhes dos dados**: Tabela com todos os dados financeiros carregados.

## 💡 Tecnologias Utilizadas

- **Streamlit**: Framework para criação de aplicações web interativas com Python.
- **Altair**: Biblioteca de visualização de dados para gráficos interativos.
- **Pandas**: Biblioteca para manipulação de dados em Python.
- **Python**: Linguagem de programação usada no desenvolvimento do projeto.

## 📥 Instalação

Para rodar o projeto localmente, siga os passos abaixo:

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/dashboard-financeiro.git
    ```

2. Navegue até o diretório do projeto:
    ```bash
    cd dashboard-financeiro
    ```

3. Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Para sistemas Unix (Linux/macOS)
    venv\Scripts\activate     # Para Windows
    ```

4. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

5. Execute a aplicação Streamlit:
    ```bash
    streamlit run app.py
    ```

6. Abra o navegador e acesse `http://localhost:8501` para ver o dashboard.

## 📄 Como Usar

1. **Carregar os Dados**: Substitua o caminho do arquivo `Extrato.csv` com seus próprios dados financeiros. O arquivo deve conter pelo menos as colunas **Valor** e **Data Lançamento**.
   
2. **Visualizar as Informações**: O dashboard exibirá a visão geral do seu saldo, entradas e saídas por mês, a evolução do saldo acumulado, além de gráficos e uma tabela com os dados financeiros.

3. **Interagir com os Gráficos**: As barras de gráficos são interativas e permitem uma análise dinâmica das entradas e saídas.

## 🎨 Layout

O layout foi projetado para ser **centrado**, com uma interface simples e limpa, incluindo:

- **Cards** com informações rápidas sobre o saldo, entradas e saídas.
- **Gráficos interativos** para análise de dados financeiros por mês.
- **Tabela de detalhes** para visualização dos dados brutos.

## 💬 Contribuição

Contribuições são bem-vindas! Se você deseja contribuir com este projeto, siga as etapas abaixo:

1. **Fork** este repositório.
2. Crie uma nova branch:
    ```bash
    git checkout -b nome-da-sua-branch
    ```
3. Faça suas alterações e **commit**:
    ```bash
    git add .
    git commit -m "Descrição das suas mudanças"
    ```
4. **Push** para o seu repositório:
    ```bash
    git push origin nome-da-sua-branch
    ```
5. Abra um **Pull Request** explicando suas mudanças.

## 📑 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

## 📧 Contato

Se você tiver dúvidas ou sugestões, sinta-se à vontade para abrir uma **issue** ou entrar em contato diretamente.

**Autor**: Bruno Teixeira 
**Email**: itbttex@itbttexhome.icu

---

🍀 **Obrigado por usar o Dashboard Financeiro!** 🌟
