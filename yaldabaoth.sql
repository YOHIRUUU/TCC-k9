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
INSERT INTO usuarios (email, nome, senha, permisao) 
