-- Tabla: Drones
CREATE TABLE Drones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    serial_number VARCHAR(100) NOT NULL,
    model ENUM('Lightweight', 'Middleweight', 'Cruiserweight', 'Heavyweight') NOT NULL,
    weight_limit FLOAT NOT NULL CHECK (0 < weight_limit <= 500),
    battery_capacity INT NOT NULL CHECK (battery_capacity >= 0 AND battery_capacity <= 100),
    state ENUM('IDLE', 'LOADING', 'LOADED', 'DELIVERING', 'DELIVERED', 'RETURNING') DEFAULT 'IDLE'
);

-- Tabla: Medications
CREATE TABLE Medications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    weight FLOAT NOT NULL CHECK (0 < weight <= 500),
    code VARCHAR(50) NOT NULL UNIQUE,
    image_path VARCHAR(255)
);

-- Tabla: loaded_medications (Carga de medicamentos en drones)
CREATE TABLE loaded_medications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    drone_id INT,
    medication_id INT,
    quantity INT,
    FOREIGN KEY (drone_id) REFERENCES Drones(id),
    FOREIGN KEY (medication_id) REFERENCES Medications(id)
);

-- Tabla: delivery_history (Historial de entregas)
CREATE TABLE delivery_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    drone_id INT,
    delivery_date TIMESTAMP,
    medication_id INT,
    quantity INT,
    -- Otras columnas relevantes para el historial de entregas
    FOREIGN KEY (drone_id) REFERENCES Drones(id),
    FOREIGN KEY (medication_id) REFERENCES Medications(id)
);

-- Created by: Luis Alberto Guisado
-- email: bethocubans1990@gmail.com 