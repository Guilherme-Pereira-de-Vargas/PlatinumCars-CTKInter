# importa a biblioteca customtkinter para criar janelas modernas
import customtkinter as ctk
# importa a função que abre o menu principal
from funcs import abrir_menu

# configura o modo escuro da interface
ctk.set_appearance_mode("dark")
# define o tema de cores padrão
ctk.set_default_color_theme("dark-blue")

# cria a janela principal do programa
app = ctk.CTk()
app.geometry("400x480")  # define o tamanho da janela
app.title("Platinum Cars - Sistema")  # define o título da janela

# cria o texto principal da tela
titulo = ctk.CTkLabel(app, text="Platinum Cars", font=("Bahnschrift SemiBold", 35))
titulo.pack(pady=30)  # adiciona espaçamento

# cria o subtítulo abaixo do título
subtitulo = ctk.CTkLabel(app, text="Sistema de Gestão", font=("Bahnschrift SemiLight", 18))
subtitulo.pack(pady=5)

# cria o botão que abre o menu principal do sistema
botao_menu = ctk.CTkButton(
    app,
    text="Entrar no Sistema",
    width=300,
    height=50,
    fg_color="#424242",
    hover_color="#1B1B1B",
    command=lambda: abrir_menu(app)  # chama o menu passando a janela principal
)
botao_menu.pack(pady=50)

# inicia o loop principal da interface gráfica
app.mainloop()
