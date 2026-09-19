# Local validation

Remote CI workflows and Actions-only components were removed on 2026-09-19
at the user’s request. Do not recreate, dispatch or require remote jobs.
The removed definitions remain available in Git history, not as active runners.

Run relevant commands from this project directory; these are selectable checks,
not a mandatory full batch for every change. Keep Cargo and GPU runs serialized.
Frozen resolution requires already prepared dependencies and a matching lockfile.

```sh
CARGO_INCREMENTAL=0 cargo check --frozen -p bevy-inspector-egui --lib
CARGO_INCREMENTAL=0 cargo test --frozen -p bevy-inspector-egui-derive --lib
```

Use the existing README and domain runbooks for affected runtime, GPU, asset and
platform checks. A check on Linux does not qualify Windows, macOS or mobile.
Record the source revision, command, configuration, device where relevant, exit
status and evidence directory. Missing inputs are not passing results.

Deleting local workflow files does not change a remote branch until publication.
Actions were disabled and read back as disabled on all ten workbench repositories
on 2026-09-19. No queued or active runs were found. Recheck settings before any
authorized publication. Exact published revisions are recorded by the workbench.
