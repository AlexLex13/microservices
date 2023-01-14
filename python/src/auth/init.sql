CREATE DATABASE auth;

GRANT ALL PRIVILEGES ON auth.* TO 'root'@'localhost';

USE auth;

CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO user (email, password) VALUE ('Georgia@email.com', 'admin');