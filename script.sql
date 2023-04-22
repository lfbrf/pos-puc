--drop table eventos;
--drop table usuario;

CREATE TABLE usuario(
    userId INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(80) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(12) NOT NULL
);

CREATE TABLE eventos(
    eventoId INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(40) NOT NULL,
    descricao VARCHAR(200),
    dia VARCHAR(10) NOT NULL,
    hora VARCHAR(5),
    endereco VARCHAR(100),
    userId INTEGER NOT NULL,
    FOREIGN KEY (userId)
        REFERENCES usuario (userId)
);


SELECT * FROM eventos;
SELECT * FROM usuario;

INSERT into usuario (nome, email, password)
VALUES("Project Aluno", "projectaluno@gmail.com", "senha");

INSERT INTO eventos (nome, descricao, dia, hora, endereco, "userId")
VALUES("Prova", "Prova de matematica", "02/05/2023", "10:30", "Rua da Felicidade, 25, SP", 1);

INSERT INTO eventos (nome, descricao, dia, hora, endereco, "userId")
VALUES("Aula", "aula de matematica", "01/05/2023", "10:30", "Rua da Felicidade, 25, SP", 1);


INSERT INTO eventos (nome, descricao, dia, hora, endereco, "userId")
VALUES("Contar Dinheiro", "Cofre", "05/05/2023", "10:10", "Rua da Riqueza, 25, RN", 2);

DELETE  FROM eventos WHERE eventoId=10;

