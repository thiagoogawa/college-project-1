CREATE DATABASE Projeto_Integrador_II;
USE Projeto_Integrador_II;

CREATE TABLE `Projeto_Integrador_II`.`Usuarios` (
	`user_id` INT AUTO_INCREMENT NOT NULL PRIMARY KEY, 
	`nome` VARCHAR(150) NOT NULL,
    `cpf` VARCHAR(20) NOT NULL,
    `data_nascimento` DATE NOT NULL,
	`email` VARCHAR(150) NOT NULL UNIQUE,
    `senha` VARCHAR(50) NOT NULL
);


SELECT * FROM `Projeto_Integrador_II`.`Usuarios`;

CREATE TABLE `Projeto_Integrador_II`.`Eventos` (
	`event_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `user_id_criador` INT NOT NULL,
    `title` VARCHAR(50) NOT NULL, 
    `descricao` VARCHAR(150) NOT NULL, 
	`valor_de_cada_cota` DECIMAL(10,2),
    `periodo_para_apostar_inicio` DATETIME NOT NULL,
    `periodo_para_apostar_fim` DATETIME NOT NULL,
    `data_acontecimento` DATE NOT NULL,
    `is_ativo` BOOL DEFAULT 1 NOT NULL,
    `status_de_publicacao` ENUM(
		'texto confuso', 
        'texto inapropriado', 
        'não respeita a política de privacidade e/ou termos de uso da plataforma', 
        'pendente',
        'aprovado'
    ) DEFAULT 'pendente' NOT NULL,
    FOREIGN KEY (user_id_criador) REFERENCES `Usuarios`(user_id)
);
SELECT * FROM `Projeto_Integrador_II`.`eventos`;

CREATE TABLE `Projeto_Integrador_II`.`Apostas` (
	`bet_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `user_id_apostador` INT NOT NULL, 
    `event_id` INT NOT NULL,
    `opcao_apostada_sim_ou_nao` ENUM('sim', 'nao') NOT NULL,
    `qtd_cotas_apostadas` INT NOT NULL, 
    `data_criacao` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
	
    FOREIGN KEY (user_id_apostador) REFERENCES `Usuarios`(user_id),
	FOREIGN KEY (event_id) REFERENCES `Eventos`(event_id)
);

SELECT * FROM `Projeto_Integrador_II`.`apostas`;

CREATE TABLE `Projeto_Integrador_II`.`Carteira` (
	`wallet_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `user_id_dono` INT NOT NULL,
	`saldo` DECIMAL(10,2),
    `historico_compras_creditos` JSON,
    `historico_creditos_apostados` JSON,
	`data_ultimo_saque` DATE NOT NULL,
	`valor_acumulado_saques_diarios` DECIMAL(10,2),
    FOREIGN KEY (user_id_dono) REFERENCES `Usuarios`(user_id)
);

SELECT * FROM `Projeto_Integrador_II`.`Carteira`;

UPDATE Carteira SET Saldo = 5000 WHERE user_id_dono = 2;

SELECT * FROM `Projeto_Integrador_II`.`Eventos`;