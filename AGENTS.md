<!-- rosentic:start -->
## Rosentic

Rosentic detects cross-branch compatibility conflicts on shared function
signatures, HTTP routes, and schemas.

- Before editing a shared surface, call `check_file` with the complete proposed
  file content. Validate the result and tell the user about any cross-branch risk
  before writing the change.
- Before pushing, call `check_conflicts` for the repository. Validate the result
  and tell the user which active branches need attention.
<!-- rosentic:end -->
