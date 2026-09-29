# Crimson Court — Siege & Town-Screen Coordinate Plan

Coordinates remain production placeholders until final 800x374-compatible town composition and siege canvases are locked. The purpose of this file is to prevent art from being produced without runtime placement requirements.

## Town composition zones
- rear center: First Bloodwood / Grail transformation
- upper left: Mage Guild / Red Moon Observatory
- upper right: Heart Aviary
- middle left: Thorn Gallery / Scarlet Lodge
- middle center: Court of Veins / Hall of First Chalice
- middle right: Gorewing Roost / Moonlit Menagerie
- lower left: Hall of Veins
- lower center: Town/City/Capitol palace line
- lower right: Fort/Citadel/Castle + Thorn Tribunal
- foreground: ritual channels and navigable UI-negative space

## Z-order policy
Foreground architecture must not hide clickable building silhouettes. Upgrades replace/extend the same visual footprint where possible. The Bloodwood may overlap buildings only with translucent/sparse branches.

## Siege identity
Crimson Court siege should look like black-marble terraces grown through thorn roots rather than a generic European castle.
- walls: black marble with red mineral seams
- towers: narrow thorn-crown silhouettes
- gate: split bloodwood-and-stone doors
- moat: shallow ritual channel / thorn trench, mechanically a normal moat unless a validated custom moat effect is later introduced
- tower shooter: Scarlet Huntress/Bloodstalker visual family

## Required siege coordinate groups
- static background/top/bottom
- top, keep, bottom tower: tower + battlement + creature points
- four destructible wall sections
- gate arch + gate
- moat + bank
- defender hero placement validation
- projectile-origin visual QA

## Production rule
No custom moat mechanic enters v0.1. First playable build uses an engine-safe standard-damage moat behavior with original Crimson visuals. Unique behavior can be considered after baseline siege QA.
