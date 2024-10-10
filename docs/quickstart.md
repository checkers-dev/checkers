# Quickstart

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

Next, we recommend reviewing the list of [builtin checks](checks/_index), and consulting the [configuration details](configuration)
