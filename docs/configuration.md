# Configuration

Checkers supports three ways of defining configuration.

1. Through a `linter.toml` file.
2. Through environment variables.
3. Through command line arguments.

The command line arguments take precedence over the environment variables, and the environment variables take precedence over the `linter.toml` file.

## Creating a `linter.toml` file

To generate a configuration file with the default configuration, use the `checkers init` command.

```
checkers init
```

This will generate a file in your current directory called `linter.toml`, and it will contain values similar to the following.

```toml
dbt_project_dir = "/workspaces/checkers/tests/mock"

[checks.check_model_has_description]
minimum_description_length = 10
minimum_description_words = 4
```

Note that file contains two sections. The first section defines the _configuration options_, which control the behaviour of Checkers. The second section defines _check parameters_, which are used by individual checks. Each of these sections is discussed in more detail below.

## Check Parameters

Checkers supports passing parameters to individual checks in order to customize their behaviour. These parameters can currently only be defined via the `linter.toml` file.

Here's an example parameter configuration for the check `check_model_has_description`.

```toml
[checks.check_model_has_description]
minimum_description_length = 10
minimum_description_words = 4
```

For more information about the parameters available for the builtin checks, see the documentation for that specific check. For example, here's the documentation for the [`check_model_has_description`](/docs/checks/check_model_has_description).

## Configuration Options

### dbt_project_dir

- Environment variable: `DBT_PROJECT_DIR`.

The path to a dbt project containing the models to lint.
