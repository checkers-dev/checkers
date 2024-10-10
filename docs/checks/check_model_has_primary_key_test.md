::: checkers.checks.check_model_has_primary_key_test
    options:
      show_root_toc_entry: false

## Reason to flag

A primary key test ensures that every table has a single column with unique, not null values. These primary keys are important for debugging issues, and helpful for features like snapshotting. We recommend every model define a primary key.

## Fixing

Add a unique and not_null test to one of the model's columns.

Example yaml entry:

```yaml
models:
  - name: user
    description: A model representing all the product's users
    columns:
      - name: user_id
        tests:
          - unique
          - not_null
```

## Parameters

N/A
