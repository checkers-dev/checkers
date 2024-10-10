::: checkers.checks.check_multiple_sources
    options:
      show_root_toc_entry: false


## Reason to flag

Model's should contain at most one source. This ensures that a single model is responsible for harmonizing a single soruce source table, eg for renaming and recasting fields.

## Fixing

Refactor the model to depend on a single source. This usually means creating 1 model per source, and having only that model reference the source. For example:

```sql
config(materialized='view')

select
  id,
  name
from {{ source('customer_data', 'names')}}
```

## Parameters

None
