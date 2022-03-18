-- Command to run this sqlite:
-- sqlite3
-- .read CI10X-Archive_create.sql
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS project_users;

-- tables
-- Table: project_users

CREATE TABLE project_users (
    id integer NOT NULL CONSTRAINT project_users_pk PRIMARY KEY,
    user_id integer NOT NULL,
    project_id integer NOT NULL,
    CONSTRAINT project_students_students FOREIGN KEY (user_id)
    REFERENCES users (user_id),
    CONSTRAINT project_students_projects FOREIGN KEY (project_id)
    REFERENCES projects (project_id)
);

-- Table: projects
CREATE TABLE projects (
    project_id integer NOT NULL CONSTRAINT projects_pk PRIMARY KEY,
    academic_year integer,
    lab_number integer,
    project_name text,
    project_description text,
    CONSTRAINT Project_Name UNIQUE (academic_year, lab_number, project_name)
);

-- Table: roles
CREATE TABLE roles (
    role_id integer NOT NULL CONSTRAINT roles_pk PRIMARY KEY,
    role_description text
);

-- Table: users
CREATE TABLE users (
    user_id integer NOT NULL CONSTRAINT user_id PRIMARY KEY,
    email text,
    password text,
    name text,
    role_id integer NOT NULL,
    CONSTRAINT user_email UNIQUE (email),
    CONSTRAINT users_roles FOREIGN KEY (role_id)
    REFERENCES roles (role_id)
);

-- End of file.

