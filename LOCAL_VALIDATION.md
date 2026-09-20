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

## Restricted world access regression

`cargo test --frozen -p bevy-inspector-egui --lib restricted_world_view::tests`
covers nested permission partitions, duplicate/empty selections, inaccessible
keys, and a Copy iterator whose copies share external state. Selection is
materialized once; the selected view and remainder must be disjoint. These tests
inspect permissions without creating overlapping mutable references.

## Maintained fork compatibility matrix

The package version remains 0.37.0; it does not identify this fork's Bevy/egui
compatibility or its permission-partition fixes. Record the commit, worktree delta
and lock identity. The current workspace selects egui 0.35 and bevy_egui 0.41.1;
Cargo manifests and the resolved lock remain authoritative.

Run these selective gates serially, retaining their feature identity:

```sh
CARGO_INCREMENTAL=0 cargo check --frozen -p bevy-inspector-egui --lib --no-default-features
CARGO_INCREMENTAL=0 cargo check --frozen -p bevy-inspector-egui --lib --no-default-features --features documentation
CARGO_INCREMENTAL=0 cargo check --frozen -p bevy-inspector-egui --lib --no-default-features --features 2d
CARGO_INCREMENTAL=0 cargo check --frozen -p bevy-inspector-egui --lib --no-default-features --features 3d
CARGO_INCREMENTAL=0 cargo test --frozen -p bevy-inspector-egui-derive --tests
python3 tools/check-consumer.py
```

The independent consumer creates only a temporary manifest/lock outside enclosing
Cargo configuration discovery, requires cached registry dependencies, checks that
engine packages are registry-sourced, and leaves this checkout's lock unchanged.
It is a separate graph from workbench integration. The actual game consumer also
needs its own `cargo check -p client-bevy --bin client-bevy --features inspector` in
the game's workspace. The Stylized showcase inspector uses bevy_egui directly and
must not be miscounted as this library's consumer.

Keep pure permission-partition regressions alongside the derive field/variant and
ignored-field tests. Reflect UI module moves must retain RestrictedWorldView access
proofs; do not replace bounded views with unrestricted mutable World access merely
to share drawing helpers. No upstream issue/PR is filed by these local checks.
