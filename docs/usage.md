# Inspector usage

## Resource inspector

Display a single resource in a window.

![image of the resource inspector](https://raw.githubusercontent.com/jakobhellermann/bevy-inspector-egui/main/docs/images/resource_inspector.png)

```rust
use bevy::prelude::*;
use bevy_inspector_egui::prelude::*;
use bevy_inspector_egui::bevy_egui::EguiPlugin;
use bevy_inspector_egui::quick::ResourceInspectorPlugin;

// `InspectorOptions` are completely optional
#[derive(Reflect, Resource, Default, InspectorOptions)]
#[reflect(Resource, InspectorOptions)]
struct Configuration {
    name: String,
    #[inspector(min = 0.0, max = 1.0)]
    option: f32,
}

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .init_resource::<Configuration>() // `ResourceInspectorPlugin` won't initialize the resource
        .register_type::<Configuration>() // you need to register your type to display it
        .add_plugins(EguiPlugin::default())
        .add_plugins(ResourceInspectorPlugin::<Configuration>::default())
        // also works with built-in resources, as long as they are `Reflect`
        .add_plugins(ResourceInspectorPlugin::<Time>::default())
        .run();
}
```

<hr>

There is also the [`StateInspectorPlugin`](../crates/bevy-inspector-egui/src/quick.rs) and the [`AssetInspectorPlugin`](../crates/bevy-inspector-egui/src/quick.rs).

## Manual UI

The [quick] plugins don't allow customization of the egui window or its content, but you can easily build your own UI:

```rust
use bevy::prelude::*;
use bevy_inspector_egui::egui;
use bevy_inspector_egui::prelude::*;
use bevy_inspector_egui::bevy_egui::{EguiPlugin, EguiContext, EguiPrimaryContextPass, PrimaryEguiContext};

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_plugins(EguiPlugin::default())
        .add_plugins(bevy_inspector_egui::DefaultInspectorConfigPlugin) // adds default options and `InspectorEguiImpl`s
        .add_systems(EguiPrimaryContextPass, inspector_ui)
        .run();
}

fn inspector_ui(world: &mut World) {
    let Ok(egui_context) = world
        .query_filtered::<&mut EguiContext, With<PrimaryEguiContext>>()
        .single(world)
    else {
        return;
    };
    let mut egui_context = egui_context.clone();

    egui::Window::new("UI").show(egui_context.get_mut(), |ui| {
        egui::ScrollArea::vertical().show(ui, |ui| {
            // equivalent to `WorldInspectorPlugin`
            bevy_inspector_egui::bevy_inspector::ui_for_world(world, ui);

            egui::CollapsingHeader::new("Materials").show(ui, |ui| {
                bevy_inspector_egui::bevy_inspector::ui_for_assets::<StandardMaterial>(world, ui);
            });

            ui.heading("Entities");
            bevy_inspector_egui::bevy_inspector::ui_for_entities(world, ui);
        });
    });
}
```

Pair this with a crate like [`egui_dock`](https://docs.rs/egui_dock/latest/egui_dock/) and you have your own editor in less than 100 lines: [`examples/egui_dock.rs`](https://github.com/BoysGameStudio/bevy-inspector-egui/blob/bevy-egui-0.41/crates/bevy-inspector-egui/examples/integrations/egui_dock.rs).

## Cargo features

Default features are `documentation`, `bevy` and `egui_clipboard`. The `bevy`
collection enables 2D, 3D and gizmo inspection; select `2d` or `3d` explicitly for
narrower integration. `documentation` displays reflected documentation on hover;
`highlight_changes` colors changed components. Optional `bevy_*` features register
inspectors for their types. See the [manifest](../crates/bevy-inspector-egui/Cargo.toml)
for dependency implications and [validation](../LOCAL_VALIDATION.md) for feature checks.

## FAQ

**Q: How do I change the names of the entities in the world inspector?**

**A:** You can insert the [`Name`](https://docs.rs/bevy_ecs/0.19.1/bevy_ecs/name/struct.Name.html) component.

**Q: What if I just want to display a single value without passing in the whole `&mut World`?**

**A:** You can use `reflect_inspector::ui_for_value`. Note that displaying things like `Handle<StandardMaterial>` won't be able to display the asset's value.

**Q:** Can I change how exactly my type is displayed?

**A:** Implement `InspectorPrimitive` and call `app.register_type_data::<T, InspectorEguiImpl>`.

[reflect_inspector]: https://docs.rs/bevy-inspector-egui/latest/bevy_inspector_egui/reflect_inspector
[inspector_options]: https://docs.rs/bevy-inspector-egui/latest/bevy_inspector_egui/inspector_options
[quick]: https://docs.rs/bevy-inspector-egui/latest/bevy_inspector_egui/quick
[bevy_inspector]: https://docs.rs/bevy-inspector-egui/latest/bevy_inspector_egui/bevy_inspector


The docs.rs references describe the upstream API family; the maintained fork
source and its locally generated rustdoc own exact behavior.
