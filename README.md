# Ambush Aftermath Fix

After the Netwatch convoy ambush in Phantom Liberty, the street in Pacifica can stay stuck in its ambush state: fires and smoke that never go out, Blackwall sparks, blacked-out street lights, leftover combat lighting, and a catwalk with billboards that disappears and never comes back.

This mod puts the area back once the quest is done with it. It uses the same switches the quest itself uses, so nothing is deleted from the map and the ambush plays exactly as normal.

## What causes it

The street is built with switchable versions of its parts, and quests flip those switches to change the area. The ambush cutscene switches on the fires, smoke, Blackwall sparks, storm effects and special lighting, and swaps the catwalk for a wrecked one. Later in the chase the quest hides the wreck again, because it comes with debris across the road, and that leaves an empty gap where the catwalk was.

These switches are stored in your save. Phantom Liberty has a step meant to tidy the area up afterwards, but it only runs on some playthroughs. When it doesn't, the effects and lighting stay switched on for good.

## How it works

This mod adds a small quest step that waits until the convoy chase is over (or the quest is finished), then:

- turns off the explosion fires, car-wreck smoke and Blackwall effects
- turns off the leftover thunderstorm effects
- restores the normal street lighting and removes the leftover ambush and cutscene lighting
- puts the trash-barrel fires back to their normal look
- restores the catwalk and billboards above the street (or leaves it out, in the No Catwalk version)

The turrets and Militech crates left from the ambush stay where they are.

## Two versions: pick one

- **Ambush Aftermath Fix**: the full cleanup, and the catwalk and billboards come back as they were before the ambush.
- **Ambush Aftermath Fix - No Catwalk**: the same cleanup, but the catwalk stays gone, the way the game leaves it after the quest. The wrecked catwalk isn't an option because it comes with debris across the road.

Install only one. They use the same file names, so a mod manager will flag a conflict if both are installed.

Whichever version you use, its changes are kept in your save once you save the game. Uninstalling the mod afterwards does not bring the effects back or change the catwalk. Switching to the other version does: it runs once on your next load and applies its own catwalk choice.

It also fixes saves that are already past the ambush: the cleanup runs as soon as you load.

## Requirements

- Cyberpunk 2077 2.x with Phantom Liberty
- [ArchiveXL](https://www.nexusmods.com/cyberpunk2077/mods/4198)

## Install

Install with a mod manager, or extract the zip into your Cyberpunk 2077 folder.

If you use a mod that deletes these effects from the map, you don't need it alongside this one.

## Building

`tools\make_questphase.py` writes a quest step as WolvenKit JSON: `main` for the main version, `no-catwalk` for the No Catwalk version. Convert it with the WolvenKit command-line tool (`convert deserialize`) and pack the folder (`pack`):

- main: `ambush_aftermath_fix\quest\cleanup_4.questphase` into `archive\pc\mod\AmbushAftermathFix.archive`
- No Catwalk: `ambush_aftermath_fix\quest\cleanup_no_catwalk.questphase` into `no-catwalk\archive\pc\mod\AmbushAftermathFix.archive`

Both versions use the same archive and `.xl` file names so only one can be installed, but their quest steps have different names.

When a new version changes what the main step does, give the step a new file name (and update the `.xl`), so it runs again on saves where the old one already ran.

## Credits

- [ArchiveXL](https://www.nexusmods.com/cyberpunk2077/mods/4198) by psiberx, which adds the quest step to the game
- [WolvenKit](https://github.com/WolvenKit/WolvenKit), used to read the game data and build the mod

Built it with Claude (the AI).

## Licence

MIT
