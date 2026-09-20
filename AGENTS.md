# Agent instructions

Read README.md for project context and docs/usage.md and LOCAL_VALIDATION.md for the affected task.

- Preserve RestrictedWorldView permission partitions: selected and remaining
  views must be disjoint, including duplicate selections and shared-state iterators.
  Do not use unrestricted mutable World access to bypass those boundaries.
- Keep derive field/variant/ignored-field behavior covered by owning tests.
- Root README is shared by two package symlinks. Keep package links valid and
  align minimal examples with crate rustdoc and the actual examples.
- Treat standalone dependency validation and game consumer checks as distinct graphs.
- Use local validation only; do not create, enable, dispatch or require remote CI.
- Choose checks for the affected behavior. Documentation-only edits use link,
  API/command-reference and packaging-input checks, without Cargo/GPU runs.
- Serialize Cargo/GPU work and set `CARGO_INCREMENTAL=0`. Report missing inputs
  and unexecuted platform checks; do not weaken tests or replace golden images.
- Preserve unrelated work and authoring inputs. Commit or publish only when asked.
