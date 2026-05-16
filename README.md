# DungeonAscend

Roguelike dungeon crawler.

## Project layout

```
DungeonAscend/
├── assets/     # Sprites, audio, fonts
├── src/        # Source files (.cpp)
├── include/    # Headers (.h, .hpp)
├── docs/       # Documentation
├── data/       # Game data (levels, configs, balance)
├── CMakeLists.txt
└── README.md
```

## Build

```bash
cmake -B build
cmake --build build
```

## Run

```bash
./build/DungeonAscend
```

On Windows:

```bash
build\Debug\DungeonAscend.exe
```
