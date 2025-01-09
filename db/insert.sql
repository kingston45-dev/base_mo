-- Таблица mo
INSERT INTO mo (id_subject, mo_name, anchoring, year) VALUES
(1, 'Городская больница №1', '+', 2023),
(2, 'Поликлиника №3', '-', 2023);

-- Таблица stat_info
INSERT INTO stat_info (id_subject, subject_rf, year, population_all, population_adult, population_city, population_country, max_distance) VALUES
(1, 'Московская область', 2023, 7500000, 5200000, 6300000, 1200000, 50.5);

-- Таблица maps_stat
INSERT INTO maps_stat (id_subject, map_stat) VALUES
(1, DECODE('...', 'base64'));
