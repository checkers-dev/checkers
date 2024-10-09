# Custom Checks

This section of the documentation describes how to create a custom check which validates all of the models in a dbt project define an `owner` property in their meta configuration. Ie, all models should have a config block similar to the following.

```sql
{{
    config(
        meta={'owner': 'marketing'}
    )
}}
```

## Creating a check

To get started, create a new file in the root of your dbt project called `linter.py`.

```
touch linter.py
```

Then open the file and add the following code. We'll explain how this works shortly.


```py
# linter.py
from checkers import Model

def check_model_has_owner(model: Model):
    assert 'owner' in model.meta, "Model must specify an `owner` field in its `meta` block"

```

We can run this check against all the models in the dbt project by using the `checkers run` command.

```
dbt parse
checkers run
```

!!! Note

    Make sure that you have _parsed_ the dbt project before using `checkers run`. This will produce dbt's `manifest.json` artifact, which Checkers relies on to understand the structure of your dbt project.

You should see output similar to the following.

```
PASS check_model_has_owner my_first_dbt_model
PASS check_model_has_owner my_second_dbt_model
```

Next, let's explore how this works, so that you can write more complex rules as needed.

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