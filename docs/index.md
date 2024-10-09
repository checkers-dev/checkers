# Checkers

Checkers is an extendable dbt linter that scans your dbt project and alerts you of any misalignments with your team's best practices. It's similar to other tools like [dbt-project-evaluator](https://github.com/dbt-labs/dbt-project-evaluator/tree/main) (created by dbt-labs), among others.

By _extendable_, we mean that we want to make it easy to define **your own** best practices. This makes it possible to validate that your team's dbt projects follow the standards you decide, without needing to completely refactor your project to a new system. We also provide numerous "out of the box" checks that are aligned with dbt lab's recommendations, so that you don't need to re-invent the wheel either.

Checkers is easy to integrate with any CI system, so that changes to your project which introduce new issues are automatically flagged, and potentially blocked. It's simple to use `checkers` with pre-commit, GitHub actions, or any other CI system you're using.

## Installation

Install the `checkers` command line interface with pip.

```
pip install checkers-cli
```

To view the documentation for all available commands, use the `--help` flag.

```
checkers --help
```

## Quickstart

Navigate to your dbt project's directory. This should be a folder that contains a `dbt_project.yml` file.

```
cd path/to/dbt/project
```


Parse your dbt project to generate a `manifest.json` artifact. (Many other dbt commands generate a `manifest.json`, including `dbt build`, `dbt test`, etc. But we recommend using `dbt parse` as it usually takes just a few seconds).

```
dbt parse
```

Run the checkers.

```
checkers run
```

The results of the check will print to your console, and look similar to the following.

```
PASS   check_model_has_description my_first_dbt_model
PASS   check_model_has_description my_second_dbt_model
```

## Next steps

- Review the list of [builtin checks](/docs/checks/check_model_has_description)
- Learn how to enable, disable, and customize the builtin checks via the [configuration file](/docs/configuration)
- Learn how to write [custom checks](/docs/custom_checks)

For any questions or to get help, please open an issue on our [GitHub repo](https://github.com/checkers-dev/checkers).
