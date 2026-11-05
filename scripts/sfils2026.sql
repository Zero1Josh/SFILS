CREATE DATABASE sfils2026;

USE sfils2026;

CREATE TABLE patron_types (
    patron_type_code INT PRIMARY KEY,
    patron_type_definition VARCHAR(50) NOT NULL
);

CREATE TABLE home_libraries (
    home_library_code VARCHAR(10) PRIMARY KEY,
    home_library_definition VARCHAR(100) NOT NULL
);

CREATE TABLE notification_types (
    notification_medium_code VARCHAR(10) PRIMARY KEY,
    notification_code_definition VARCHAR(50) NOT NULL
);

CREATE TABLE patrons (
    patron_id INT AUTO_INCREMENT PRIMARY KEY, 
    patron_type_code INT, 
    total_checkouts INT,
    total_renewals INT,
    age_range VARCHAR(20),
    home_library_code VARCHAR(10),
    circulation_active_month VARCHAR(15),
    circulation_active_year INT,
    notification_medium_code VARCHAR(10),
    provided_email_address BOOLEAN,
    within_sf_county BOOLEAN,
    year_patron_registered INT,
    FOREIGN KEY (patron_type_code) REFERENCES patron_types(patron_type_code),
    FOREIGN KEY (home_library_code) REFERENCES home_libraries(home_library_code),
    FOREIGN KEY (notification_medium_code) REFERENCES notification_types(notification_medium_code)
);

SELECT COUNT(*) FROM patrons;
SELECT COUNT(*) FROM patron_types;