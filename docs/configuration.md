# Configuration

Checkers provides two types of configuration.

The first type is _check parameters_. These are variables that control the behaviour of individual checks. For example, you might want to run a specific check only on certain directories in your dbt project.

The second type is _runner parameters_. These variables control the behaviour of the runner, and generally apply to every check that gets run. For example, you might want to have all checks only ever raise a warning, rather than fail.

Both check parameters and runner parameters can be set via a `linter.toml` configuration file. We recommend generating the `linter.toml` using the `init` command, as it will include all default configuration values for all checks.

```
checkers init
```

## Check Parameters

The parameters of an individual check are located in a specific section of the configuration file. Here's what that looks like for two checks `check_model_has_description` and `check_model_has_primary_key_test`.

```toml
[checks.check_model_has_description]
enabled = true
exclude_paths = []
include_paths = []
minimum_description_length = 10
minimum_description_words = 4

[checks.check_model_has_primary_key_test]
enabled = true
exclude_paths = []
include_paths = []
```

Notice that some configuration options appear for both checks, such as the `exclude_paths` field. Other options are unique to a specific check, such as `minimum_description_word_length`, which is only relevant for the model description checks.

In the rest of this section we'll describe the check parameters that are common to all checks. For more information about the parameters available for individual checks, you can consult the documentation for that specific check. For example, here's [the documentation for the `check_model_has_description`](checks/check_model_has_description.md).

### `enabled`

This flag can be used to completely disable the check. Disabled checks are never ran.

### `exclude_paths`

A set of paths that the check should skip. The paths must be relative to the dbt project directory.

!!! Info
    Currently Checkers does not support regexes here.

### `include_paths`

A set of paths that the check should target, so that any node which lives _outside_ of these paths will be skipped. The paths must be relative to the dbt project directory.

!!! Info
    If a path is defined in both include and exclude paths, then the model will be skipped. Ie, `exclude_paths` takes priority over `include_paths`.

!!! Info
    Currently Checkers does not support regexes here.

## Runner parameters

The runner can be configured in three ways:

- The `linter.toml` file
- Command line options specified when using the `checkers` cli.
- Environment variables

Command line options take precedence over environment variables, and environment variables take precedence over values in the `linter.toml` file.

The runner current supports the following parameters.

### dbt_project_dir

- `checkers --dbt-project-dir ./path/to/project [COMMAND]`
- Environment variable: `DBT_PROJECT_DIR`.

The path to a dbt project containing the models to lint.
