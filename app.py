import streamlit as st
import pandas as pd
import sqlite3
from faker import Faker

# Interface Streamlit
def main():
    st.title("ERP Financeiro com Streamlit")
    
    menu = ["Clientes", "Contas a Pagar", "Contas a Receber", "Lançamentos", "Relatórios", "Contas a Pagar por Fornecedor", "Top Clientes", "Receita vs Despesa"]
    choice = st.sidebar.selectbox("Selecione uma opção", menu)
    conn = sqlite3.connect("erp_finance.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()
    
    if choice == "Clientes":
        st.subheader("Cadastro de Clientes")
        df = pd.read_sql_query("SELECT * FROM clientes", conn)
        st.dataframe(df)
        
    elif choice == "Contas a Pagar":
        st.subheader("Contas a Pagar")
        df = pd.read_sql_query("SELECT * FROM contas_pagar", conn)
        st.dataframe(df)
        
    elif choice == "Contas a Receber":
        st.subheader("Contas a Receber")
        df = pd.read_sql_query("SELECT * FROM contas_receber", conn)
        st.dataframe(df)
        
    elif choice == "Lançamentos":
        st.subheader("Lançamentos Financeiros")
        df = pd.read_sql_query("SELECT * FROM lancamentos", conn)
        st.dataframe(df)
        
    elif choice == "Relatórios":
        st.subheader("Relatório de Fluxo de Caixa")
        df = pd.read_sql_query("SELECT tipo, SUM(valor) as total FROM lancamentos GROUP BY tipo", conn)
        st.dataframe(df)

    elif choice == "Contas a Pagar por Fornecedor":
        st.subheader("Distribuição das Contas a Pagar por Fornecedor")
    
        query = "SELECT fornecedor, SUM(valor) as total FROM contas_pagar GROUP BY fornecedor ORDER BY total DESC"
        df = pd.read_sql_query(query, conn)

        if df.empty:
            st.warning("Nenhum dado disponível para exibição.")
        else:
            chart_type = st.radio("Escolha o tipo de gráfico:", ("Pizza", "Barras"))

        if chart_type == "Pizza":
            fig = df.set_index("fornecedor").plot.pie(y="total", autopct='%1.1f%%', startangle=90, figsize=(10, 10), legend = False)
            st.pyplot(fig.figure)
        
        elif chart_type == "Barras":
            st.bar_chart(df.set_index("fornecedor"))

    elif choice == "Top Clientes":
        st.subheader("Top 5 Clientes com Maior Receita")

        query = """
        SELECT c.nome, SUM(cr.valor) as total_receita 
        FROM contas_receber cr
        JOIN clientes c ON cr.cliente_id = c.id 
        GROUP BY c.id, c.nome
        ORDER BY total_receita DESC 
        LIMIT 5
        """
        df = pd.read_sql_query(query, conn)

       
        st.write("Tabela:")
        st.dataframe(df)
            
        st.write("Gráfico de Barras:")
        st.bar_chart(df.set_index("nome"))

    elif choice == "Receita vs Despesa":
        st.subheader("Mês Atual")
        
        query = """
        SELECT tipo, SUM(valor) as total 
        FROM lancamentos 
        WHERE strftime('%Y-%m', data) = strftime('%Y-%m', 'now')
        GROUP BY tipo
        """
        df = pd.read_sql_query(query, conn)
        
    
        st.write("Gráfico de Barras Receita vs Despesa:")
        st.bar_chart(df.set_index("tipo"))    
   
    
    conn.close()
    
if __name__ == "__main__":
    main()
