# Custom Checks

One of the key goals of Checkers is to make it easy to define custom validations for your dbt project.

For example, suppose you want to ensure that all of the models in your project define an `owner` property in their meta configuration. Ie, all models should have a config block similar to the following.

```sql
{{
    config(
        meta={'owner': 'marketing'}
    )
}}
```

Let's create a custom check that ensures all models include an `owner`.

## Creating a check

To get started, run the `checkers init` command. This will create a new file `linter.py` which includes a simple example.

```
checkers init
```

Then open the file and add the following code. Don't worry if the code here doesn't immediately make sense - we'll explain everything shortly.


```py
# linter.py
from checkers import Model

def check_model_has_owner(model: Model):
    assert 'owner' in model.meta, "Model must specify an `owner` field in its `meta` block"

```

Now let's run this check against all the models in your dbt project by using the `checkers run` command.

```
dbt parse
checkers run
```

You should see output similar to the following.

```
PASS   model my_first_dbt_model check_model_has_owner
FAIL   model my_second_dbt_model check_model_has_owner
```

!!! Warning

    Make sure that you have _parsed_ the dbt project before using `checkers run`. This will produce dbt's `manifest.json` artifact, which Checkers relies on to understand the structure of your dbt project.


Next, let's explore how this works, so that you can write more complex checks to specify your own project's rules.

## Use `assert` statements for validation

In Python, the `assert` keyword is a special way of checking if a value is "Truthy". If the value provided to the `assert` statement is `False` or `None`, the statement will raise an `AssertionError`.

Here's an example.

```py
>>> val = False
>>> assert val
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AssertionError

>>> val = True
>>> assert val  # No error is raised now
```

When Checkers runs your check, it catches any `AssertionError`s that are raised, and records them as a _check failure_. This provides a simple, expressive way of writing checks.

!!! Note
    You might notice that the design of using `assert` statements is very similar to how [pytest](https://docs.pytest.org/en/stable/) enables Python developers to write tests. That's because it is!

An `assert` statement can also receive an optional second parameter, which is an error message. You can use these messages to explain why the check failed. Here's an example with an assert statement.

```py
>>> description = "the user model"
>>> assert len(description) > 20, f"Description is too short - {len(description)} letters"
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AssertionError: Description is too short - 14 letters
```

Let's take another look at the `check_model_has_owner` we just created. Notice that:

- The check uses a single assert statement, `assert 'owner' in model.config`. If the `model.config` does _not_ contain an owner, then the expression `'owner' in model.config` will evaluate to `False`. So the assert statement will raise an error, and Checkers will log the model that is missing an owner definition.
- Additionally, the assert statement specified the string `"Model must specify an owner field in its meta block"`, which is the error message presented to the user when a check fail.

So if we run this check against a model that does not specify an owner, we'll see output similar to the following.

```
FAIL check_model_has_owner my_first_dbt_model / Model must specify an `owner` field in its `meta` block
```

## Skipping models

A common use case is to run checks on some models, but not others. Checkers supports this through providing a special `skip` function.

```py
from checkers import skip, Model

def check_model_has_owner(model: Model):
    if model.original_file_path.startswith('marts/'):
        skip()
    assert 'owner' in model.meta, "Model must specify an `owner` field in its `meta` block"
```

## Checking different resource types

Sometimes you want to check resource types other than models. For example, you might want to check the sources defined in your dbt project always specify a description.

Checkers supports this by changing the first argument passed to your check function.

```py
def check_sources_have_description(source: Source):
    assert source.description is not None
```

Checkers uses the name of the first argument supplied to your check function to pass the correct type of resource to the function. In thise case, because the function used `source` as the first argument, Checkers knew this check should only be ran against dbt sources, and it provided a `Source` object to the function.
