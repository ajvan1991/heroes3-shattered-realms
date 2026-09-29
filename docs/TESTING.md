# Local VCMI Testing

Target: VCMI 1.7.x.

## Rule
A feature is not considered playable merely because its JSON parses. It must be tested in the VCMI client.

## Test loop
1. Install/copy the mod into the user's VCMI Mods location.
2. Enable Shattered Realms in VCMI Launcher.
3. Launch VCMI and inspect logs for schema/resource errors.
4. Start a controlled test map.
5. Verify town selection, recruitment, building prerequisites, hero generation and combat.
6. Record failures with exact log output.
7. Fix in repository and repeat.

## Balance telemetry to record
- starting army value
- day 1-7 build order and resource bottlenecks
- weekly recruit cost
- weekly army AI/fight value
- practical neutral-clearing strength
- losses against representative neutral stacks
- T6/T7 acquisition timing
- spell access
- PvP matchup notes against core factions

## Asset policy
Temporary development assets must be clearly marked. Final release must not ship copyrighted third-party art without permission.
