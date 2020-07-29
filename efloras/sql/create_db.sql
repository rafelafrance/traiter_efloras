drop table if exists families;
create table families (
    flora_id   integer,
    taxon_id   integer,
    family     text,
    link       text,
    flora_name text
);
create index families_key on families (flora_id, taxon_id);
create index families_family on families (family);


drop table if exists pages;
create table pages (
    flora_id  integer,
    taxon_id  integer,
    family    text,
    page_type text,
    page_no   int,
    html      blob
);
create index pages_key on pages (flora_id, taxon_id);
create index pages_fam on pages (flora_id, family);
create index pages_type on pages (page_type);


drop table if exists taxa;
create table taxa (
    flora_id integer,
    taxon_id integer,
    family   text,
    taxon    text
);
create index taxa_key on taxa (flora_id, taxon_id);
create index taxa_family on taxa (family);


drop table if exists treatments;
create table treatments (
    flora_id  integer,
    taxon_id  integer,
    treatment text
);
create index treatments_key on treatments (flora_id, taxon_id);


drop table if exists traits;
create table traits (
);
