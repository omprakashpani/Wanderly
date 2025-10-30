
CREATE DATABASE IF NOT EXISTS wandely CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE wandely;


CREATE USER IF NOT EXISTS 'wandely_user'@'localhost' IDENTIFIED BY 'wander123';
GRANT ALL PRIVILEGES ON wandely.* TO 'wandely_user'@'localhost';
FLUSH PRIVILEGES;


DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS trip_planner;
DROP TABLE IF EXISTS trips;
DROP TABLE IF EXISTS cuisines;
DROP TABLE IF EXISTS foods;
DROP TABLE IF EXISTS monasteries;
DROP TABLE IF EXISTS users;


CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL
);

INSERT INTO users (username, password) VALUES
('admin','admin123'),
('traveler','travel123');


CREATE TABLE monasteries (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  location VARCHAR(255),
  description TEXT,
  image_url VARCHAR(255)
);

INSERT INTO monasteries (name, location, description) VALUES
('Rumtek Monastery', 'Gangtok', 'The seat of the Karmapa and major Kagyu monastery.'),
('Pemayangtse Monastery', 'Pelling', '17th-century monastery with wooden carvings.'),
('Gonjang Monastery', 'East Sikkim', 'Tashi Viewpoint, Gangtok'),
('Karkot Monastery', 'West Sikkim', 'situated near Yuksom'),
('Phensang Monastery', 'North Sikkim', 'belongs to the Nyingma sect and is known for its scenic location'),
('Phodong Monastery', 'North Sikkim', 'is a major Buddhist monastery of the Karma Kagyu sect.');


CREATE TABLE foods (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  image_url VARCHAR(255)
);


CREATE TABLE cuisines (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  image_url VARCHAR(255)
);

INSERT INTO cuisines (name, description, image_url) VALUES
('Nepali','Nepali food influences in Sikkim','/static/images/nepali.jpg'),
('Bhutia','Tibetan-influenced cuisine','/static/images/bhutia.jpg');


CREATE TABLE trips (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  image_url VARCHAR(255)
);

INSERT INTO trips (title, description) VALUES
('Rumtek Dharma Chakra Centre',
 'Old Rumtek Gompa – Colourful interiors, picnic lawns, panoramic views. Nehru Botanical Garden – Orchids, temperate plants, calm walking paths.'),

('Pemayangtse Monastery',
 'Rabdentse Ruins – Forest walk to Sikkim’s former capital. Sewaro Rock Garden – Landscaped park with waterfalls. Rimbi Waterfall – Beautiful natural cascade. Pelling Skywalk & Chenrezig Statue – Scenic glass-skywalk experience.'),

('Phensang Monastery',
 'Kabi Lungchok – Historic treaty site of Lepchas & Bhutias. Seven Sisters Waterfall – Quick scenic stop on the highway. Labrang Monastery – Peaceful site with unique architecture.'),

('Phodong Monastery',
 'Labrang Monastery – 19th-century monastery, peaceful & scenic. Seven Sisters Waterfall – Beautiful photography spot. Kabi Lungchok – Historic blood brotherhood site.'),

('Kartok Monastery',
 'Kartok Lake – Scenic, tranquil meditation spot. Norbugang Coronation Throne – Coronation site of 1st Chogyal (1642). Tashi Tenka – Valley viewpoint near Yuksom.'),

('Gonjang Monastery',
 'Tashi Viewpoint – Sunrise over Kanchenjunga. Ganesh Tok & Hanuman Tok – Hilltop temples with panoramic views. Enchey Monastery – 200-year-old Buddhist heritage site. Bakthang Waterfall – Small scenic waterfall. Flower Exhibition Centre – Famous for orchids & seasonal blooms.');


CREATE TABLE comments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  trip_id INT NOT NULL,
  user_id INT NOT NULL,
  comment TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


CREATE TABLE trip_planner (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  trip_name VARCHAR(255),
  start_date DATE,
  end_date DATE,
  monasteries_selected TEXT,
  preferences TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

