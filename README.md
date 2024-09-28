# `Kivy - KivyMD Lazy Loading Template`

Enhance the performance of your Kivy - KIvyMD app 🚀 with lazy loading.

By implementing this template, you can enhance the performance of your Kivy app through the technique of lazy loading screens.
Rather than loading all the screens at startup, this approach ensures that screens are loaded only when they are actively switched to or preloaded on request.
It is best to preload by scheduling the preload Clock.schedule_once(method)
As a result, the startup time of your app can be significantly reduced and screen transitions feel more smooth.

This template also features a **`screen navigation system`** that simplifies handling the back button.

## `Requirements`
`Kivy>=2.3.0"`
`KivyMD==2.0.1.dev0`

## `Navigation`

The [`Root`](https://github.com/kulothunganug/kivy-lazy-loading-template/blob/main/libs/uix/root.py) is based on [`screen`](https://kivy.org/doc/stable/api-kivy.uix.screen.html) and additionally provides a few navigation methods: `push(screen_name, side, transition_type)`, `push_replacement(screen_name, side, transition_type)` and `back()`.

Also `load_screen(screen_name, preload=True)` method can be used to load the screen and the kv file without setting it as the current screen.

To incorporate additional screens into your app, follow these steps:

1. Create `screen_file.py` in the `libs/uix/screens/` directory.
2. Create `screen_file.kv` in the `libs/uix/kv/screens/` directory.
3. Add the screen details to `screens.json` as shown below:

```json
{
    ...,
    "welcome": {
        "module": "libs.uix.baseclass.screens.welcome",
        "class": "WelcomeScreen",
        "kv": "libs/uix/kv/screens/welcome.kv"
    },
}
```

This template already contains three screens as example which uses all the crucial navigation methods.

## `Special Back Functionality`

The back method adds a two second delay to exit the application if there is no other screen to go back to.
This simulates the double clicking back button to exit on Android

## Buildozer

To use this template for mobile devices, make sure to add **json** to your `buildozer.spec` file, such as

```spec
# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,gif,json
```

### Further details are documented within the code itself
