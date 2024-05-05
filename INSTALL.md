# Installation Instructions

## Ubuntu Based Distributions (PopOS)

```bash
sudo apt-get install '^libxcb.*-dev' libx11-xcb-dev libglu1-mesa-dev libxrender-dev libxi-dev libxkbcommon-dev libxkbcommon-x11-dev blueman
```

## Mac OS

Para que se pueda cargar correctamente la biblioteca plux.so hay que deshabilitar el demonio de seguridad
de MacOs utilizando el siguiente comando:

```bash
sudo spctl --master-disable
```
