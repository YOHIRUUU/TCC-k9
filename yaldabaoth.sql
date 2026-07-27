CREATE DATABASE IF NOT EXISTS almoxarifado;
USE almoxarifado;

CREATE TABLE IF NOT EXISTS usuarios (
    email VARCHAR(100) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    permisao INT DEFAULT 0,
    PRIMARY KEY (email)
);

CREATE TABLE IF NOT EXISTS estoque (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    quantidade INT DEFAULT 0,
    categoria VARCHAR(50) NOT NULL,
    descricao VARCHAR(255),
    preco decimal(9, 2) NOT NULL,
    imagem Varchar(255) NOT NULL
);

CREATE TABLE historico_estoque (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    acao VARCHAR(50) NOT NULL,
    produto_nome VARCHAR(100) NOT NULL,
    qtd_anterior INT DEFAULT 0,
    qtd_nova INT DEFAULT 0,
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //
CREATE TRIGGER log_insert_estoque
AFTER INSERT ON estoque
FOR EACH ROW
BEGIN
    INSERT INTO historico_estoque (acao, produto_nome, qtd_anterior, qtd_nova)
    VALUES ('Novo Produto Cadastrado', NEW.nome, 0, NEW.quantidade);
END; //
DELIMITER ;

DELIMITER //
CREATE TRIGGER log_update_estoque
AFTER UPDATE ON estoque
FOR EACH ROW
BEGIN
    DECLARE tipo_acao VARCHAR(50);
    
    IF NEW.quantidade > OLD.quantidade THEN
        SET tipo_acao = 'Adição';
    ELSEIF NEW.quantidade < OLD.quantidade THEN
        SET tipo_acao = 'Subtração';
    ELSE
        SET tipo_acao = 'Edição de Dados';
    END IF;

    INSERT INTO historico_estoque (acao, produto_nome, qtd_anterior, qtd_nova)
    VALUES (tipo_acao, NEW.nome, OLD.quantidade, NEW.quantidade);
END; //
DELIMITER ;

DELIMITER //
CREATE TRIGGER log_delete_estoque
AFTER DELETE ON estoque
FOR EACH ROW
BEGIN
    INSERT INTO historico_estoque (acao, produto_nome, qtd_anterior, qtd_nova)
    VALUES ('Item Deletado', OLD.nome, OLD.quantidade, 0);
END; //
DELIMITER ;
