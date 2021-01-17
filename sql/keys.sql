-- Table: public.todos

-- DROP TABLE public.todos;

create table keys
(
    keys_id  serial      not null
        constraint firstkey
            primary key,
    api_key varchar(50) not null,
    key     varchar(150) not null
);
