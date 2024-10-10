# Reference

This reference page documents the objects that can be passed to a custom check function.

For example, the `Model` object documented below is passed to all check functions. The custom check function can use the attributes of the model class to write assertions about the model.

```py
from checkers import Model

def check_model_descriptions(model: Model):
  assert model.description is not None
```

::: checkers.contracts.Model
    options:
      heading_level: 2
      inherited_members: true
      show_bases: false
      show_root_heading: true
      show_root_full_path: false
      show_source: false
      show_labels: false


::: checkers.contracts.Test
    options:
      heading_level: 2
      inherited_members: true
      show_bases: false
      show_root_heading: true
      show_root_full_path: false
      show_source: false
      show_labels: false


::: checkers.contracts.Manifest
    options:
      heading_level: 2
      inherited_members: true
      show_bases: false
      show_root_heading: true
      show_root_full_path: false
      show_source: false
      show_labels: false
