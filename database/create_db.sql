DROP TABLE Buttons;
CREATE TABLE IF NOT EXISTS Buttons
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    text TEXT,
    url TEXT,
    code_name TEXT
);

CREATE TABLE IF NOT EXISTS Photos
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file BLOB,
    button_id INTEGER,
    FOREIGN KEY (button_id)  REFERENCES Buttons (id)
);

CREATE TABLE IF NOT EXISTS Descriptions
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT,
    button_id INTEGER,
    FOREIGN KEY (button_id)  REFERENCES Buttons (id)
);