import bcrypt

senha_plana = "minha_senha_secreta"

bytes_senha = senha_plana.encode('utf-8')
bytes_hash = bcrypt.hashpw(bytes_senha, bcrypt.gensalt())

print("Hash gerado:", bytes_hash.decode('utf-8'))


senha_digitada = "minha_senha_comida"

if bcrypt.checkpw(senha_digitada.encode('utf-8'), bytes_hash):
    print("Sucesso: A senha está correta!")
else:
    print("Erro: Senha incorreta.")
