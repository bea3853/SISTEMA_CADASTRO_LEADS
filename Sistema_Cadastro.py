import sqlite3 # banco de dados
import tkinter as tk # interface basica
from tkinter import messagebox # caixas de mensagens
from tkinter import ttk # interface grafica tb

def conectar():
    return sqlite3.connect('teste.db')

# colunas do banco de dados
def criar_tabela():
    conn = conectar()
    c= conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER NOT NULL,
        nome TEXT NOT NULL,
        email TEXT NOT NULL              
        )       
    ''')
    conn.commit()
    conn.close()
  


# CREATE
def inserir_usuario():
    nome = entry_nome.get()
    email = entry_email.get()
    cpf =  entry_cpf.get()
   
    if nome and email and cpf:
        conn = conectar()
        c = conn.cursor()
        c.execute('INSERT INTO usuarios(id,nome,email) VALUES(?,?,?)', (cpf,nome, email))
        conn.commit()
        conn.close()
        messagebox.showinfo('AVISO', 'DADOS INSERIDOS COM SUCESSO!') 
        mostrar_usuario()
        # entry_cpf.delete(0,)
        entry_cpf.delete(0, tk.END)
        entry_email.delete(0,tk.END)
        entry_nome.delete(0,tk.END)
    else:
        messagebox.showwarning('ATENÇÃO!', 'INSIRA OS DADOS CORRETAMENTE') 

# READ
def mostrar_usuario():
    for row in tree.get_children():   
        tree.delete(row)
    conn = conectar()
    c = conn.cursor()    
    c.execute('SELECT * FROM usuarios')
    usuarios = c.fetchall()
    for usuario in usuarios:
        tree.insert("", "end", values=(usuario[0], usuario[1],usuario[2]))
    conn.close()    


# DELETE
def delete_usuario():
    dado_del = tree.selection()
    if dado_del:
       user_id = tree.item(dado_del)['values'][0]
       conn = conectar()
       c = conn.cursor()    
       c.execute('DELETE FROM usuarios WHERE id = ? ',(user_id,))
       conn.commit()
       conn.close()
       messagebox.showinfo('', 'DADO DELETADO')
       mostrar_usuario()

    else:
       messagebox.showerror('', 'SELECIONE UM DADO')  

# UPDATE 
       
def editar():
     selecao = tree.selection()
     if selecao:
         user_id = tree.item(selecao)['values'][0]
         novo_nome = entry_nome.get()
         novo_email = entry_email.get()
         

         if novo_nome and novo_email:
            conn = conectar()
            c = conn.cursor()    
            c.execute('UPDATE usuarios SET nome = ? , email = ? WHERE id = ? ',(novo_nome,novo_email,user_id))
            conn.commit()
            conn.close()  
            messagebox.showinfo('', 'DADOS ATUALIZADOS')
            mostrar_usuario()

         else:
             messagebox.showwarning('', 'PREENCHA TODOS OS CAMPOS')

     else:
            messagebox.showerror('','SELECIONE A LINHA PARA EDITAR')


janela = tk.Tk()
janela.title('CRUD')
janela.geometry('1920x1080')
janela.configure(bg = 'gray')

label_nome = tk.Label(janela, text='Nome:', font=('roboto',15))
label_nome.grid(row=0, column=0, padx=10, pady=10, )

entry_nome = tk.Entry(janela, font=('roboto',15))
entry_nome.grid(row=0, column=1, padx=10, pady=10)

label_email = tk.Label(janela, text = 'E-mail:', font=('roboto',15))
label_email.grid(row=1, column=0, padx=10, pady=10)

entry_email = tk.Entry(janela, text = 'E-mail:', font=('roboto',15))
entry_email.grid(row=1, column=1, padx=10, pady=10)



label_CPF = tk.Label(janela, text = 'CPF:', font=('roboto',15))
label_CPF.grid(row=2, column=0, padx=10, pady=10)

entry_cpf = tk.Entry(janela, text = 'CPF:', font=('roboto',15))
entry_cpf.grid(row=2, column=1,   pady=10)



btn_salvar = tk.Button(janela, text='Salvar', command=inserir_usuario,  width=15)
btn_salvar.grid(row= 4, column=1,  pady=10)

btn_deletar = tk.Button(janela, text='deletar', command=delete_usuario , width=15)
btn_deletar.grid(row=4, column=2,  pady=10)

btn_atualizar = tk.Button(janela, text='atualizar', command=editar,  width=15)
btn_atualizar.grid(row=4, column=3,  pady=10)

columns = ('ID', ' NOME', 'E-MAIL')
tree = ttk.Treeview(janela, columns=columns, show='headings',)
tree.grid(row = 6, column=0, columnspan= 10, padx=5, pady=10)

for col in columns:
    tree.heading(col, text=col)

criar_tabela()
mostrar_usuario()


janela.mainloop()






# CREATE  -  CRIAR UM NOVO DADO PARA UMA APLICAÇÃO
# READ    -  SISTEMA LE ESSE DADO
# UPDATE  -  SISTEMA ATUALIZAR O DADO
# DELETE  -  DELETAR O DADOS QUE FOI CRIADO


