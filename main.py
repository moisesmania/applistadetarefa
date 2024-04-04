import streamlit as st
import sqlite3

# Função para conectar ao banco de dados SQLite3
def conectar_bd():
    conn = sqlite3.connect ('lista_tarefas.db')
    c = conn.cursor()
    return conn, c

# Função para criar a tabela se não existir
def criar_tabela():
    conn, c = conectar_bd()
    c.execute('''CREATE TABLE IF NOT EXISTS tarefas (
                    id INTEGER PRIMARY KEY,
                    descricao TEXT,
                    concluida BOOLEAN
                  )''')
    conn.commit()
    conn.close()

# Função para adicionar tarefa
def adicionar_tarefa(descricao):
    conn, c = conectar_bd()
    c.execute ("INSERT INTO tarefas (descricao, concluida) VALUES (?, ?)", (descricao, False))
    conn.commit()
    conn.close()

# Função para excluir tarefa
def excluir_tarefa(id_tarefa):
    conn, c = conectar_bd()
    c.execute("DELETE FROM tarefas WHERE id=?", (id_tarefa,))
    conn.commit()
    conn.close()

# Função para editar tarefa
def editar_tarefa(id_tarefa, nova_descricao):
    conn, c = conectar_bd()
    c.execute("UPDATE tarefas SET descricao=? WHERE id=?", (nova_descricao, id_tarefa))
    conn.commit()
    conn.close()

# Função para obter todas as tarefas
def obter_tarefas():
    conn, c = conectar_bd()
    c.execute("SELECT * FROM tarefas")
    tarefas = c.fetchall()
    conn.close()
    return tarefas

# Criar a tabela se não existir
criar_tabela()

# Interface Streamlit
def main():
    st.title("Lista de Tarefas Diárias")

    # Entrada para adicionar tarefa
    descricao = st.text_input("Nova Tarefa:")

    # Botão para adicionar tarefa
    if st.button("Adicionar Tarefa"):
        if descricao:
            adicionar_tarefa(descricao)
            st.success("Tarefa adicionada com sucesso!")
        else:
            st.warning("Por favor, insira uma descrição para a tarefa.")

    # Listar tarefas
    tarefas = obter_tarefas()
    if tarefas:
        st.write("## Tarefas:")
        for tarefa in tarefas:
            concluida = "Concluída" if tarefa[2] else "Pendente"
            st.write (f"{tarefa[0]}: {tarefa[1]} - {concluida}")

        # Opções para editar e excluir tarefa
        opcao = st.selectbox("Selecione uma opção:", ["Editar Tarefa", "Excluir Tarefa"])
        if opcao == "Editar Tarefa":
            id_tarefa = st.text_input("ID da Tarefa:")
            nova_descricao = st.text_input("Nova Descrição:")
            if st.button("Editar"):
                if id_tarefa and nova_descricao:
                    editar_tarefa(id_tarefa, nova_descricao)
                    st.success("Tarefa editada com sucesso!")
                else:
                    st.warning("Por favor, insira o ID da tarefa e a nova descrição.")
        elif opcao == "Excluir Tarefa":
            id_tarefa = st.text_input("ID da Tarefa:")
            if st.button("Excluir"):
                if id_tarefa:
                    excluir_tarefa(id_tarefa)
                    st.success("Tarefa excluída com sucesso!")
                else:
                    st.warning("Por favor, insira o ID da tarefa para excluir.")
    else:
        st.write("Ainda não há tarefas adicionadas.")

if __name__ == "__main__":
    main()
