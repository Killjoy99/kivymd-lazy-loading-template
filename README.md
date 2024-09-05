# Kivy Lazy Loading - Template

Enhance the performance of your Kivy app 🚀 with lazy loading.

By implementing this template, you can enhance the performance of your Kivy app through the technique of lazy loading screens. Rather than loading all the screens at startup, this approach ensures that screens are loaded only when they are actively switched to. As a result, the startup time of your app can be significantly reduced.

This template also features a **screen navigation system** that simplifies handling the back button.

## Navigation

The [`Root`](https://github.com/kulothunganug/kivy-lazy-loading-template/blob/main/libs/uix/root.py) is based on [`screen`](https://kivy.org/doc/stable/api-kivy.uix.screen.html) and additionally provides a few navigation methods: `push(screen_name, side, transition_type)`, `push_replacement(screen_name, side, transition_type)` and `back()`.

Also `load_screen(screen_name)` method can be used to load the screen and the kv file without setting it as the current screen.

To incorporate additional screens into your app, follow these steps:

1. Create `screen_file.py` in the `libs/uix/baseclass/` directory.
2. Create `screen_file.kv` in the `libs/uix/kv/` directory.
3. Add the screen details to `screens.json` as shown below:

```json
{
    ...,
    "screen_name": {
        "module": "libs.uix.baseclass.screen_file",
        "class": "ClassName",
        "kv": "libs/uix/kv/screen_file.kv"
    }
}
```

This template already contains three screens as example which uses all the navigation methods.

## Buildozer

To use this template for mobile devices, make sure to add **json** to your `buildozer.spec` file, such as

```spec
# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,gif,json
```

## Hot Reloading

Run the app with python -m kvhot . --top 40 --left 1016

### Further details are documented within the code itself
