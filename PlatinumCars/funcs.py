# importa a biblioteca customtkinter para criar janelas modernas
import customtkinter as ctk
# importa o conector mysql para comunicação com banco de dados
import mysql.connector
# importa messagebox para criar alertas e mensagens
from tkinter import messagebox

# função que conecta ao banco de dados
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="platinum_cars"
    )

# função que abre o menu principal do sistema
def abrir_menu(menu):
    menu.withdraw()  # esconde a janela anterior
    janela = ctk.CTkToplevel(menu)  # cria nova janela
    janela.title("Menu Principal")
    janela.geometry("400x480")

    ctk.CTkLabel(janela, text="Menu Principal", font=("Bahnschrift SemiBold", 35)).pack(pady=25)

    # função que abre a tela de operações (cadastrar, pesquisar etc.)
    def abrir_opcao(nome, titulo):
        janela.withdraw()
        abrir_janela_operacoes(janela, nome, titulo)

    # lista de botões principais
    botoes = [
        ("Clientes", "cliente", "Cliente"),
        ("Vendedores", "vendedor", "Vendedor"),
        ("Veículos", "estoque", "Veículo"),
        ("Vendas", "vendas", "Venda")
    ]

    # cria um botão para cada opção do menu
    for texto, tabela, titulo in botoes:
        ctk.CTkButton(
            janela, text=texto, width=300, height=50,
            fg_color="#424242", hover_color="#1B1B1B",
            command=lambda t=tabela, ti=titulo: abrir_opcao(t, ti)
        ).pack(pady=10)

    # botão voltar
    def voltar():
        janela.destroy()
        menu.deiconify()

    ctk.CTkButton(janela, text="Voltar", width=300, command=voltar).pack(pady=25)


# função que abre a janela com as operações (cadastrar, pesquisar, atualizar, excluir)
def abrir_janela_operacoes(menu, tabela, titulo):
    menu.withdraw()
    janela = ctk.CTkToplevel(menu)
    janela.geometry("400x500")
    janela.title(f"Gerenciar {titulo}s")

    ctk.CTkLabel(janela, text=f"{titulo}s", font=("Bahnschrift SemiBold", 35)).pack(pady=25)

    # abre a janela específica da ação escolhida
    def abrir_acao(acao):
        janela.withdraw()
        abrir_janela_acao(janela, tabela, acao, titulo)

    # cria botões das ações
    for acao in ["Cadastrar", "Pesquisar", "Atualizar", "Excluir"]:
        ctk.CTkButton(
            janela, text=acao, width=300, height=50,
            fg_color="#424242", hover_color="#1B1B1B",
            command=lambda a=acao: abrir_acao(a)
        ).pack(pady=10)

    # botão voltar
    def voltar():
        janela.destroy()
        menu.deiconify()

    ctk.CTkButton(janela, text="Voltar", width=300, command=voltar).pack(pady=25)


# função que abre a janela de cada ação (cadastrar, pesquisar etc.)
def abrir_janela_acao(menu, tabela, acao, titulo):
    menu.withdraw()
    janela = ctk.CTkToplevel(menu)
    janela.geometry("450x550")
    janela.title(f"{acao} {titulo}")

    ctk.CTkLabel(janela, text=f"{acao} {titulo}", font=("Bahnschrift SemiBold", 30)).pack(pady=20)

    # dicionário com os campos de cada tabela
    campos = {
        "cliente": ["cpf", "nome", "cidade", "estado", "telefone"],
        "vendedor": ["cpf", "nome", "cidade", "estado", "telefone", "email"],
        "estoque": ["placa", "nome", "modelo", "cor", "chassi", "spoiler", "categoria", "ano_carro"],
        "vendas": ["id_venda", "cpf_cliente", "cpf_vendedor", "placa", "produto", "preco", "data", "forma_pagamento"]
    }

    entradas = {}
    # cria um campo de entrada para cada coluna da tabela
    for campo in campos[tabela]:
        entradas[campo] = ctk.CTkEntry(janela, placeholder_text=campo.capitalize(), width=300)
        entradas[campo].pack(pady=4)

    # ação cadastrar
    if acao == "Cadastrar":
        def salvar():
            valores = [e.get().strip() for e in entradas.values()]  # pega valores digitados
            if any(v == "" for v in valores):  # verifica campos vazios
                messagebox.showwarning("Aviso", "Preencha todos os campos antes de salvar!")
                return

            con = conectar()
            cursor = con.cursor()
            colunas = ", ".join(campos[tabela])
            placeholders = ", ".join(["%s"] * len(campos[tabela]))
            cursor.execute(f"INSERT INTO {tabela} ({colunas}) VALUES ({placeholders})", valores)
            con.commit()
            con.close()
            messagebox.showinfo("Sucesso", f"{titulo} cadastrado com sucesso!")

        ctk.CTkButton(janela, text="Salvar", fg_color="#424242", hover_color="#1B1B1B", command=salvar).pack(pady=15)

    # ação pesquisar
    elif acao == "Pesquisar":
        janela.geometry("600x1080")

        # chave primária de cada tabela
        chaves = {
            "cliente": "cpf",
            "vendedor": "cpf",
            "estoque": "placa",
            "vendas": "id_venda"
        }
        chave = chaves[tabela]

        ctk.CTkLabel(
            janela,
            text=f"Informe o {chave.upper()} ou deixe vazio para listar todos:",
            font=("Arial", 13)
        ).pack(pady=5)

        campo_pesquisa = ctk.CTkEntry(janela, placeholder_text=f"{chave.upper()} (opcional)", width=300)
        campo_pesquisa.pack(pady=5)

        # caixa de texto onde resultados aparecem
        caixa = ctk.CTkTextbox(janela, width=500, height=420)
        caixa.pack(pady=10)

        # função que realiza a busca
        def pesquisar():
            identificador = campo_pesquisa.get().strip()
            con = conectar()
            cursor = con.cursor()

            # busca por um registro específico ou todos
            if identificador:
                cursor.execute(f"SELECT * FROM {tabela} WHERE {chave} = %s", (identificador,))
            else:
                cursor.execute(f"SELECT * FROM {tabela}")

            registros = cursor.fetchall()
            colunas = [desc[0] for desc in cursor.description]
            con.close()

            caixa.delete("1.0", "end")

            # mostra os resultados
            if not registros:
                caixa.insert("end", "Nenhum registro encontrado.\n")
            else:
                for r in registros:
                    for c, v in zip(colunas, r):
                        caixa.insert("end", f"{c.capitalize()}: {v}\n")
                    caixa.insert("end", "-" * 50 + "\n")

        ctk.CTkButton(
            janela,
            text="Pesquisar",
            fg_color="#424242",
            hover_color="#1B1B1B",
            command=pesquisar
        ).pack(pady=10)

    # ação atualizar
    elif acao == "Atualizar":
        ctk.CTkLabel(janela, text="Preencha apenas os campos que deseja alterar.\n(Use o identificador principal)", font=("Arial", 12)).pack(pady=5)

        # função que atualiza o registro
        def atualizar():
            valores = {c: e.get().strip() for c, e in entradas.items()}
            chave = list(valores.keys())[0]  # primeira coluna é sempre o identificador
            valor_chave = valores[chave]

            if valor_chave == "":
                messagebox.showwarning("Aviso", f"Informe o {chave.upper()} para atualizar!")
                return

            campos_para_atualizar = {c: v for c, v in valores.items() if v != "" and c != chave}

            if not campos_para_atualizar:
                messagebox.showwarning("Aviso", "Nenhum campo para atualizar!")
                return

            con = conectar()
            cursor = con.cursor()
            cursor.execute(f"SELECT * FROM {tabela} WHERE {chave} = %s", (valor_chave,))
            existe = cursor.fetchone()

            if not existe:
                con.close()
                messagebox.showerror("Erro", f"Nenhum registro com {chave.upper()} '{valor_chave}' encontrado!")
                return

            set_clause = ", ".join([f"{c}=%s" for c in campos_para_atualizar])
            valores_sql = list(campos_para_atualizar.values()) + [valor_chave]

            cursor.execute(f"UPDATE {tabela} SET {set_clause} WHERE {chave}=%s", valores_sql)
            con.commit()
            con.close()

            messagebox.showinfo("Sucesso", f"{titulo} atualizado com sucesso!")

        ctk.CTkButton(janela, text="Atualizar", fg_color="#424242", hover_color="#1B1B1B", command=atualizar).pack(pady=15)

    # ação excluir
    elif acao == "Excluir":
        # oculta todos os campos menos o identificador
        for w in list(entradas.values())[1:]:
            w.pack_forget()

        ctk.CTkLabel(
            janela,
            text="Informe apenas o identificador principal (CPF, Placa ou ID_Venda)",
            font=("Arial", 12)
        ).pack(pady=5)

        # função que exclui o registro
        def excluir():
            chave = list(entradas.keys())[0]
            valor = entradas[chave].get().strip()

            if valor == "":
                messagebox.showwarning("Aviso", "Informe o identificador para excluir!")
                return

            con = conectar()
            cursor = con.cursor()
            cursor.execute(f"SELECT * FROM {tabela} WHERE {chave}=%s", (valor,))
            registro = cursor.fetchone()

            if not registro:
                con.close()
                messagebox.showerror("Erro", f"Nenhum registro com {chave.upper()} '{valor}' encontrado!")
                return

            colunas = [desc[0] for desc in cursor.description]
            info = "\n".join([f"{c.capitalize()}: {v}" for c, v in zip(colunas, registro)])
            con.close()

            confirmar = messagebox.askyesno(
                "Confirmação",
                f"Tem certeza que deseja excluir este {titulo}?\n\n{info}"
            )

            if not confirmar:
                return

            con = conectar()
            cursor = con.cursor()
            cursor.execute(f"DELETE FROM {tabela} WHERE {chave}=%s", (valor,))
            con.commit()
            con.close()

            messagebox.showinfo("Sucesso", f"{titulo} excluído com sucesso!")

        ctk.CTkButton(
            janela,
            text="Excluir",
            fg_color="#424242",
            hover_color="#1B1B1B",
            command=excluir
        ).pack(pady=15)

    # botão voltar
    def voltar():
        janela.destroy()
        menu.deiconify()

    ctk.CTkButton(janela, text="Voltar", width=300, command=voltar).pack(pady=15)
