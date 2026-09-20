# bevy-inspector-egui

Bevy reflection and ECS inspection through egui: inspect resources, entities,
assets and custom values, or compose a custom editor from the inspection helpers.

This is the BoysGameStudio fork of
[jakobhellermann/bevy-inspector-egui](https://github.com/jakobhellermann/bevy-inspector-egui).
The maintained integration uses Bevy 0.19, egui 0.35 and bevy_egui 0.41.1;
Cargo manifests and the resolved lock determine exact source identities.
The package's 0.37.0 version alone does not identify these fork fixes.

## Start with a world inspector

Use this checkout's `crates/bevy-inspector-egui` package as a path dependency and
add the egui plugin before the inspector:

```toml
[dependencies]
bevy = "=0.19.1"
bevy-inspector-egui = { path = "../bevy-inspector-egui/crates/bevy-inspector-egui" }
```

```rust,no_run
use bevy::prelude::*;
use bevy_inspector_egui::{bevy_egui::EguiPlugin, quick::WorldInspectorPlugin};


fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_plugins(EguiPlugin::default())
        .add_plugins(WorldInspectorPlugin::new())
        .run();
}
```

The quick plugins are useful for simple inspection. Custom windows, resource
options and reflected values are covered by the usage guide and examples.

## Documentation

- [Usage guide](https://github.com/BoysGameStudio/bevy-inspector-egui/blob/bevy-egui-0.41/docs/usage.md).
- [Examples](https://github.com/BoysGameStudio/bevy-inspector-egui/blob/bevy-egui-0.41/crates/bevy-inspector-egui/examples/README.md).
- [Local validation](https://github.com/BoysGameStudio/bevy-inspector-egui/blob/bevy-egui-0.41/LOCAL_VALIDATION.md): feature/derive/permission checks and consumer boundaries.
- [Agent instructions](https://github.com/BoysGameStudio/bevy-inspector-egui/blob/bevy-egui-0.41/AGENTS.md).
- [MIT](https://github.com/BoysGameStudio/bevy-inspector-egui/blob/bevy-egui-0.41/LICENSE-MIT.md) / [Apache-2.0](https://github.com/BoysGameStudio/bevy-inspector-egui/blob/bevy-egui-0.41/LICENSE-APACHE.md) licenses.

Generate API documentation from this checkout with
`cargo doc -p bevy-inspector-egui --no-deps`; upstream docs.rs may differ.
