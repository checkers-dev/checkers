::: checkers.checks.check_model_has_description
    options:
      show_root_toc_entry: false


## Reason to flag

Model descriptions are a key part of your project's documentation. They provide a high level summary of the purpose and contents of the model. We recommend that every model in your project has meaningful description.

## Fixing

Add a description to the model's config block, or update the model's yaml entry.

Example config block:

```sql
{{
  config(
    description="A model representing all the product's users."
  )
}}
```

Example yaml entry:

```yaml
models:
  - name: user
    description: A model representing all the product's users
```

## Parameters

- `minimum_description_length`: The minimum number of characters in the description
- `minimum_description_words`: The minimum number of words in the description
