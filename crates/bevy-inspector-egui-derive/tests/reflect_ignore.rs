use bevy_inspector_egui::{
    inspector_options::{std_options::NumberOptions, Target},
    InspectorOptions,
};
use bevy_reflect::{FromType, Reflect};

fn hidden_default() -> f32 {
    0.0
}

#[test]
fn combined_reflect_options_preserve_visible_struct_field_indexes() {
    #[derive(Reflect, InspectorOptions)]
    struct Test {
        #[reflect(ignore, default)]
        _first: f32,
        #[reflect(default = "hidden_default", ignore)]
        _second: f32,
        #[reflect(@true, ignore)]
        _third: f32,
        #[inspector(min = 2.0, max = 3.0)]
        visible: f32,
    }
    let options = <InspectorOptions as FromType<Test>>::from_type();
    assert_eq!(options.iter().count(), 1);
    let visible = options
        .get(Target::Field(0))
        .expect("first reflected field");
    assert_eq!(
        visible.downcast_ref::<NumberOptions<f32>>().unwrap().min,
        Some(2.0)
    );
}

#[test]
fn combined_reflect_options_preserve_visible_enum_field_indexes() {
    #[derive(Reflect, InspectorOptions)]
    enum Test {
        Variant {
            #[reflect(default, ignore)]
            _first: f32,
            #[reflect(ignore, default = "hidden_default")]
            _second: f32,
            #[inspector(min = 4.0)]
            visible: f32,
        },
    }
    let options = <InspectorOptions as FromType<Test>>::from_type();
    assert_eq!(options.iter().count(), 1);
    let visible = options
        .get(Target::VariantField {
            variant_index: 0,
            field_index: 0,
        })
        .expect("first reflected variant field");
    assert_eq!(
        visible.downcast_ref::<NumberOptions<f32>>().unwrap().min,
        Some(4.0)
    );
}

#[test]
fn check_options_ignore_struct() {
    #[derive(Reflect, InspectorOptions)]
    struct Test {
        #[reflect(ignore)]
        _a: f32,
        #[inspector(min = 2.0, max = 3.0)]
        b: f32,
    }

    let options = <InspectorOptions as FromType<Test>>::from_type();
    assert_eq!(options.iter().count(), 1);

    let b_options = options
        .get(Target::Field(0))
        .unwrap()
        .downcast_ref::<NumberOptions<f32>>()
        .unwrap();
    assert_eq!(b_options.min, Some(2.0));
}

#[test]
fn check_options_ignore_enum() {
    #[derive(Reflect, InspectorOptions)]
    enum Test {
        Variant {
            #[reflect(ignore)]
            _ignored: f32,
            #[inspector(min = 0.0)]
            no_ignored: f32,
        },
    }

    let options = <InspectorOptions as FromType<Test>>::from_type();
    assert_eq!(options.iter().count(), 1);

    let field_options = options
        .get(Target::VariantField {
            variant_index: 0,
            field_index: 0,
        })
        .unwrap()
        .downcast_ref::<NumberOptions<f32>>()
        .unwrap();
    assert_eq!(field_options.min, Some(0.0));
}
