::: checkers.checks.check_model_has_description
    options:
      show_root_toc_entry: false

## Reason to flag

Checks that a model includes a description in its config.

## Fixing

Add a description to the model's config block.

```sql
{{
  config(
    description="A model representing all the product's users."
  )
}}
```
