# Checkers

Checkers is a dbt linter that's incrementally adoptable, extendable, and comes with "batteries included."

In short, Checkers scans your dbt project and alerts you of any misalignments with your team's best practices. It's similar to other tools like [dbt-project-evaluator](https://github.com/dbt-labs/dbt-project-evaluator/tree/main) from dbt-labs, [dbt-score](https://github.com/PicnicSupermarket/dbt-score) from Picnic, among others.

Checkers is easy to integrate with any CI system, so that changes to your project which introduce new issues are automatically flagged, and potentially blocked. It's simple to use `checkers` with pre-commit, GitHub actions, or any other CI system.

## Batteries included

Checkers comes with numerous checks built in, so that you don't need to reinvent the wheel. We're working towards equivalence with dbt-project evaluator, and we're frequently adding new checks as dbt evolves.


!!! Info
    You can see the full list of built-in checks [here](checks/_index.md).

## Extendable

Checkers is also highly customizable to your own team's way of working. We make it easy to add new checks using Python, and we also support modern code completion capabilities, making it fast and easy for your team to adapt as your project grows.

Using your own checks also means you can standardize your team's dbt projects around a coherent way of working without having to migrate to a completely new system. This provides your team with the benefits of standardization, without imposing aesthetic details like whether you use a `sources` directory or a `staging` directory.

!!! Info
    To learn more about writing custom checks, you can see [the user guide](custom_checks.md)

## Incrementally adoptable

Checkers can be incrementally added into any existing dbt project. This allows you to start adding useful requirements into your codebase and turning on CI checks immediately. This also ensures you prevent drift as you bring the project up to your team's best practices.

## Next steps

- [Install the checkers-cli](installation.md)
- [Review the quickstart to run your first checks](quickstart.md)
- [Browse the full list of builtin checks](checks/_index.md)
- [Learn how to write custom checks](custom_checks.md)
