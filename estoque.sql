CREATE DATABASE almoxarifado;
USE almoxarifado;

CREATE TABLE estoque(
	id INT,
	nome VARCHAR(32) NOT NULL,
	quantidade INT,
	categoria VARCHAR(24) NOT NULL,
	descricao VARCHAR(64) NOT NULL,
    PRIMARY KEY (`id`)
	);

CREATE TABLE usuarios (
	matricula VARCHAR(32) NOT NULL,
	email VARCHAR(48) NOT NULL,
    senha VARCHAR(32) NOT NULL,
    permisao BOOL,
    PRIMARY KEY (`email`)
	);

INSERT INTO usuarios (matricula, email, senha, permisao) VALUES ('ademiro', 'admin@gmail.com', 'admin123', 1)
INSERT INTO usuarios (matricula, email, senha, permisao) VALUES ('usairo', 'user@gmail.com', 'user123', 0)
