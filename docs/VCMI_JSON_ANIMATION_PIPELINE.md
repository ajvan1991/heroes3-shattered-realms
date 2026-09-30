# VCMI JSON Animation Pipeline — Crimson Court

VCMI officially supports JSON animations backed by modern image files such as PNG. This gives Shattered Realms a clean production route without requiring legacy DEF authoring as the source format.

## Runtime shape
An animation JSON uses:
- optional `basepath`;
- `sequences`, each with numeric `group` and a list of frame filenames;
- optional automatic shadow/overlay generation.

Creature groups used by the first production wave:
0 movement; 2 idle; 3 hit; 4 defend; 5 death; 7/8 turning; 11/12/13 melee directions.

VCMI can derive group 22 Dead from the final Death frame and group 24 Resurrection by reversing Death when those groups are absent, so these are polish groups rather than first-boot blockers for the T1/T2 melee set.

## Repository workflow
1. Art direction and character turnaround.
2. Produce transparent PNG frames under `SPRITES/CRIMSON/frames/<creature>/gXX/`.
3. Run the scaffold/generator tooling.
4. Only after every required group has real frames, emit the runtime animation JSON at the resource path expected by creature config.
5. Run asset pipeline strict checks.
6. Run isolated candidate build.
7. Test animation timing and baseline in VCMI 1.7.5.
8. Mark CONVERTED, then VALIDATED_VCMI only after actual runtime evidence.

## Important naming transition
The current creature staging points at `*.DEF` resources. VCMI documentation confirms JSON is an alternative animation format, but we will not rewrite the master references until a populated JSON animation for that creature exists and has passed candidate validation. This avoids replacing one missing resource with another incomplete resource.

## Frame targets
`production/animation-frame-plan.crimson-v0.1.json` defines the first workload: 40 required animation groups across four T1/T2 creatures. Frame counts are our production targets, not engine requirements.

No empty scaffold is runtime content.
