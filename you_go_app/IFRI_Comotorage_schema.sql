
-- IFRI_Comotorage+ Schema.sql
-- MySQL / MariaDB compatible (peut être adapté pour PostgreSQL)

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    username VARCHAR(150) UNIQUE,
    photo_profile VARCHAR(255),
    role ENUM('PASSENGER', 'DRIVER') DEFAULT 'PASSENGER',
    default_start_point VARCHAR(255),
    default_end_point VARCHAR(255),
    default_start_time TIME,
    default_end_time TIME,
    consent_tracking_default BOOLEAN DEFAULT TRUE,
    is_kyc_validated BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    date_joined DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_modified_username DATETIME
);

CREATE TABLE kyc_documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    document_file VARCHAR(255),
    status ENUM('PENDING', 'APPROVED', 'REJECTED') DEFAULT 'PENDING',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    validated_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    brand VARCHAR(100),
    model VARCHAR(100),
    license_plate VARCHAR(50),
    seats_available INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE ride_offers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    driver_id INT,
    start_point VARCHAR(255),
    end_point VARCHAR(255),
    start_time DATETIME,
    seats_available INT,
    description TEXT,
    price_type ENUM('FREE', 'FIXED', 'ESTIMATED') DEFAULT 'FREE',
    fixed_price DECIMAL(10,2),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('ACTIVE', 'CANCELLED', 'COMPLETED') DEFAULT 'ACTIVE',
    FOREIGN KEY (driver_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE ride_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    passenger_id INT,
    start_point VARCHAR(255),
    end_point VARCHAR(255),
    start_time DATETIME,
    price_preference ENUM('FREE', 'FIXED', 'ESTIMATED') DEFAULT 'FREE',
    max_price DECIMAL(10,2),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('ACTIVE', 'CANCELLED', 'COMPLETED') DEFAULT 'ACTIVE',
    FOREIGN KEY (passenger_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE ride_matches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ride_offer_id INT,
    ride_request_id INT,
    driver_accepted BOOLEAN DEFAULT FALSE,
    passenger_accepted BOOLEAN DEFAULT FALSE,
    tracking_driver_consent BOOLEAN DEFAULT FALSE,
    tracking_passenger_consent BOOLEAN DEFAULT FALSE,
    status ENUM('PENDING', 'CONFIRMED', 'REFUSED', 'CANCELLED', 'COMPLETED') DEFAULT 'PENDING',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ride_offer_id) REFERENCES ride_offers(id) ON DELETE CASCADE,
    FOREIGN KEY (ride_request_id) REFERENCES ride_requests(id) ON DELETE CASCADE
);

CREATE TABLE tracking_positions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT,
    user_id INT,
    latitude DOUBLE,
    longitude DOUBLE,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id) REFERENCES ride_matches(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE chat_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT,
    receiver_id INT,
    match_id INT,
    content TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (match_id) REFERENCES ride_matches(id) ON DELETE SET NULL
);

CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    type ENUM('MATCH_REQUEST', 'MATCH_CONFIRMED', 'CHAT_MESSAGE', 'TRACKING_STARTED', 'RIDE_COMPLETED', 'GENERAL') DEFAULT 'GENERAL',
    title VARCHAR(255),
    body TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE invoices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT,
    driver_id INT,
    passenger_id INT,
    total_price DECIMAL(10,2),
    pdf_file VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id) REFERENCES ride_matches(id) ON DELETE CASCADE,
    FOREIGN KEY (driver_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (passenger_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE driver_reliability_score (
    id INT AUTO_INCREMENT PRIMARY KEY,
    driver_id INT,
    total_rides_completed INT DEFAULT 0,
    feedback_positive_count INT DEFAULT 0,
    feedback_negative_count INT DEFAULT 0,
    score FLOAT DEFAULT 0.0,
    FOREIGN KEY (driver_id) REFERENCES users(id) ON DELETE CASCADE
);
