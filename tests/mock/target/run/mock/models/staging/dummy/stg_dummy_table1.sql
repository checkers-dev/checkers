

  create view "dev"."main"."stg_dummy_table1__dbt_tmp" as (
    select *
from './sources/table1.csv'
  );
