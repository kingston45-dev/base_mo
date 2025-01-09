-- Таблица для медицинских организаций
CREATE TABLE mo (
    id_subject INTEGER PRIMARY KEY,
    mo_name TEXT NOT NULL,
    anchoring CHAR(1) NOT NULL,
    year INTEGER NOT NULL
);

-- Таблица для статистической информации
CREATE TABLE stat_info (
    id_subject INTEGER,
    subject_rf TEXT NOT NULL,
    year INTEGER,
    population_all INTEGER,
    population_adult INTEGER,
    population_city INTEGER,
    population_country INTEGER,
    max_distance FLOAT,
    PRIMARY KEY (id_subject, year)
);

-- Таблица для данных по картам
CREATE TABLE maps_stat (
    id_subject INTEGER PRIMARY KEY,
    map_stat BYTEA
);
