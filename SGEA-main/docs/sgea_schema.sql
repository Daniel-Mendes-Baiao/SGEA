
-- =======================================================
-- SCRIPT DE CRIAÇÃO E POPULAÇÃO DO BANCO SGEA
-- =======================================================

-- =========================
-- TABELAS BASE DO DJANGO
-- =========================
CREATE TABLE auth_user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME,
    is_superuser BOOLEAN NOT NULL,
    username VARCHAR(150) UNIQUE NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    email VARCHAR(254),
    is_staff BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    date_joined DATETIME NOT NULL
);

-- =========================
-- PERFIS DE USUÁRIO
-- =========================
CREATE TABLE accounts_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK(role IN ('aluno', 'professor', 'organizador'))
);

-- =========================
-- EVENTOS
-- =========================
CREATE TABLE events_event (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    date DATETIME NOT NULL,
    location VARCHAR(255) NOT NULL,
    organizer_id INTEGER NOT NULL REFERENCES accounts_profile(id) ON DELETE CASCADE
);

-- =========================
-- INSCRIÇÕES
-- =========================
CREATE TABLE registrations_registration (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES accounts_profile(id) ON DELETE CASCADE,
    event_id INTEGER NOT NULL REFERENCES events_event(id) ON DELETE CASCADE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- CERTIFICADOS
-- =========================
CREATE TABLE certificates_certificate (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    registration_id INTEGER NOT NULL REFERENCES registrations_registration(id) ON DELETE CASCADE,
    issued_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    file_path VARCHAR(255)
);

-- =========================
-- RELATÓRIOS
-- =========================
CREATE TABLE reports_report (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL REFERENCES events_event(id) ON DELETE CASCADE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    file_path VARCHAR(255)
);

-- =======================================================
-- POPULAÇÃO INICIAL
-- =======================================================

-- USUÁRIOS
INSERT INTO auth_user (id, username, password, is_superuser, is_staff, is_active, date_joined)
VALUES 
(1, 'organizador_carla', 'pbkdf2_sha256$260000$org123$hashhash', 1, 1, 1, CURRENT_TIMESTAMP),
(2, 'prof_maria', 'pbkdf2_sha256$260000$prof123$hashhash', 0, 0, 1, CURRENT_TIMESTAMP),
(3, 'aluno_joao', 'pbkdf2_sha256$260000$aluno123$hashhash', 0, 0, 1, CURRENT_TIMESTAMP);

-- PERFIS
INSERT INTO accounts_profile (id, user_id, role)
VALUES
(1, 1, 'organizador'),
(2, 2, 'professor'),
(3, 3, 'aluno');

-- EVENTOS
INSERT INTO events_event (id, title, description, date, location, organizer_id)
VALUES
(1, 'Semana Acadêmica de Tecnologia', 'Palestras e workshops sobre tecnologia e inovação.', '2025-11-20 19:00:00', 'Auditório Central', 1),
(2, 'Workshop de Inteligência Artificial', 'Oficina prática sobre aplicações de IA no cotidiano.', '2025-12-05 14:00:00', 'Laboratório 3', 1);

-- INSCRIÇÕES
INSERT INTO registrations_registration (id, user_id, event_id, created_at)
VALUES
(1, 2, 1, CURRENT_TIMESTAMP),
(2, 3, 1, CURRENT_TIMESTAMP),
(3, 3, 2, CURRENT_TIMESTAMP);

-- CERTIFICADOS
INSERT INTO certificates_certificate (id, registration_id, issued_at, file_path)
VALUES
(1, 1, CURRENT_TIMESTAMP, '/media/certificados/cert_prof_maria_semana.pdf'),
(2, 3, CURRENT_TIMESTAMP, '/media/certificados/cert_aluno_joao_ia.pdf');

-- RELATÓRIOS
INSERT INTO reports_report (id, event_id, created_at, file_path)
VALUES
(1, 1, CURRENT_TIMESTAMP, '/media/reports/report_semana_academica.pdf'),
(2, 2, CURRENT_TIMESTAMP, '/media/reports/report_workshop_ia.pdf');
