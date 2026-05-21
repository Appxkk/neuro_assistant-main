create extension if not exists pgcrypto;

alter table employees
    add column if not exists username text,
    add column if not exists password_hash text,
    add column if not exists access_level text not null default 'low',
    add column if not exists must_change_password boolean not null default true,
    add column if not exists updated_at timestamp with time zone default now();

alter table employees
    drop constraint if exists employees_access_level_check;

alter table employees
    add constraint employees_access_level_check
    check (access_level in ('low', 'medium', 'high'));

update employees
set
    username = coalesce(username, 'employee_' || id::text),
    password_hash = coalesce(
        password_hash,
        'sha256$' || encode(digest(('Temp' || id::text || '!2026')::text, 'sha256'), 'hex')
    ),
    access_level = coalesce(access_level, 'low'),
    must_change_password = true,
    updated_at = now()
where username is null
   or password_hash is null
   or access_level is null;

create unique index if not exists employees_username_unique_idx
    on employees (lower(username))
    where username is not null;

-- После выполнения миграции существующие сотрудники смогут войти так:
-- логин: employee_<id>
-- пароль: Temp<id>!2026
-- пример для сотрудника с id = 1: employee_1 / Temp1!2026
--
-- Для администратора выставьте высокий уровень доступа:
-- update employees set access_level = 'high' where id = 1;
