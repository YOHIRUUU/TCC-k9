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
    imagem Varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS historico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_email VARCHAR(100) NOT NULL,
    item_nome VARCHAR(100) NOT NULL,
    quantidade INT NOT NULL, -- Positivo para entrada, Negativo para saída
    tipo VARCHAR(20) NOT NULL, -- 'Entrada' ou 'Saída'
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_email) REFERENCES usuarios (email) ON DELETE CASCADE
);

INSERT INTO usuarios (email, nome, senha, permisao) 
