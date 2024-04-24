
/* This is used for creating tables*/




CREATE TABLE IF NOT EXISTS accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    relationship VARCHAR(255),
    role VARCHAR(255) DEFAULT 'user',
    mobile VARCHAR(12),
    volunteer ENUM('yes', 'no') DEFAULT 'no',
    basic ENUM('yes', 'no') DEFAULT 'no',
    advanced ENUM('yes', 'no') DEFAULT 'no',
    food ENUM('yes', 'no') DEFAULT 'no',
    expert ENUM('yes', 'no'),
    transport ENUM('yes', 'no'),
    event ENUM('yes', 'no'),
    status VARCHAR(255)
);



CREATE TABLE IF NOT EXISTS events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_date DATE,
    event_name VARCHAR(40),
    start_time TIME,
    end_time TIME,
    user_id INT,
    tutor VARCHAR(25),
    FOREIGN KEY (user_id) REFERENCES accounts(id)
);


CREATE TABLE IF NOT EXISTS events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_date DATE,
    event_name VARCHAR(40),
    start_time TIME,
    end_time TIME,
    user_id INT,
    tutor VARCHAR(25),
    FOREIGN KEY (user_id) REFERENCES accounts(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);

CREATE TABLE IF NOT EXISTS locations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    location_name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    location_address VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS reset (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    token VARCHAR(128) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES accounts(id)
);


CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(255) NOT NULL,
    tutor VARCHAR(255) NOT NULL,
    user_id INT NOT NULL,
    attendance_status ENUM('present', 'absent') NOT NULL DEFAULT 'absent',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    event_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES accounts(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);


CREATE TABLE IF NOT EXISTS event_registration (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    event_id INT,
    user_name VARCHAR(25),
    user_email VARCHAR(50),
    event_name VARCHAR(50),
    start_time TIME,
    end_time TIME,
    tutor VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES accounts(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);


CREATE TABLE IF NOT EXISTS event (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    pdf BLOB NOT NULL,
    softcopy BLOB NOT NULL
);







