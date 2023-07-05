# Wallpaper Switcher
This program allows you to quickly bind a key to switch your wallpaper and organize your wallpapers depending on your mood

## Supported Operating Systems

At the moment just i3 desktops

## Prerequisites

Before using the Wallpaper Switcher, ensure that the following dependencies are installed on your system:

- `feh`: Used for setting the wallpaper.
- `rofi`: Used for selecting wallpaper folders and displaying error messages.

If these dependencies are not installed, the program will prompt you to install them.

## Installation
It's not a pretty install but it works....

```shell
git clone https://github.com/DeaSTL/wallpaperswitcher/tree/main
cp wallpaperswitcher.py .local/bin/wallpaperswitcher # or whatever you'd like to name it
chmod +x .local/bin/wallpaperswitcher
```

## Configuration

The program uses a JSON configuration file to customize its behavior. The default configuration file is located at `~/.config/wallpaperswitcher/wallpaperswitcher.json`. You can modify this file to suit your preferences.

The default configuration options are as follows:

```json
{
  "wallpaper_dir": "~/Pictures/wallpapers",
  "wallpaper_change_prefix": "feh --bg-scale ",
  "show_errors": false
}
```

- `wallpaper_dir`: Specifies the directory where your wallpaper images are stored.
- `wallpaper_change_prefix`: Specifies the command to set the wallpaper. The default command is `feh --bg-scale`.
- `show_errors`: Specifies whether error messages should be displayed using `rofi`. Default is `false`.

## Usage

**Make sure that you have sub folders in your wallpaper directory or the program will not work** 

To use the Wallpaper Switcher, open a terminal and navigate to the directory where the script is located. Then, run the following command:

```shell
wallpaperswitcher [options]
```
Available options:

- `-sf` or `--select-folder`: Select a wallpaper folder.
- `-nw` or `--next-wallpaper`: Select the next wallpaper in the current folder.
- `-pw` or `--prev-wallpaper`: Select the previous wallpaper in the current folder.
- `-nr` or `--next-random`: Select a random wallpaper in the current folder.
- `-r` or `--random`: Select a random wallpaper in a random folder.
- `-c` or `--current`: Print the current wallpaper.

**Note: If no option is provided, the program will set the wallpaper to the last wallpaper used.**

Optionally but more than likely you will also configure your i3 or awesomewm config file to work with this system

### i3wm Config
```config
#Initialization
exec --no-startup-id wallpaperswitcher


#Keybind section
bindsym Mod4+w exec wallpaperswitcher -nw

bindsym Mod4+Shift+w exec wallpaperswitcher -sf

```

### Awesome WM Config
```config
I'm gonna stick a pin in that one
```



## Future Features

The following features are planned for future versions of the Wallpaper Switcher:

- Wallpaper scheduling options (e.g., set wallpapers based on time of day).
- Support for other desktop environments that don't use feh for wallpaper switching
