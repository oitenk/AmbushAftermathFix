# Ambush Aftermath Fix

After the Netwatch convoy ambush in Phantom Liberty, the street in Pacifica can stay stuck in its ambush state: fires and smoke that never go out, Blackwall sparks, blacked-out street lights, leftover combat lighting, and a catwalk with billboards that disappears and never comes back.

This mod puts the area back once the quest is done with it. It uses the same switches the quest itself uses, so nothing is deleted from the map and the ambush plays exactly as normal.

## How it works

The ambush cutscene changes several parts of the street that the quest never changes back. This mod adds a small quest step that waits until the convoy chase is over (or the quest is finished), then:

- turns off the explosion fires, car-wreck smoke and Blackwall effects
- turns off the leftover thunderstorm effects
- restores the normal street lighting and removes the leftover ambush and cutscene lighting
- puts the trash-barrel fires back to their normal look
- restores the catwalk and billboards above the street

The turrets and Militech crates left from the ambush stay where they are.

It also fixes saves that are already past the ambush: the cleanup runs as soon as you load.

## Requirements

- Cyberpunk 2077 2.x with Phantom Liberty
- [ArchiveXL](https://www.nexusmods.com/cyberpunk2077/mods/4198)

## Install

Install with a mod manager, or extract the zip into your Cyberpunk 2077 folder.

If you use a mod that deletes these effects from the map, you don't need it alongside this one.

## Building

`tools\make_questphase.py` writes the quest step as WolvenKit JSON. Convert it with the WolvenKit command-line tool (`convert deserialize`) into `ambush_aftermath_fix\quest\cleanup_2.questphase` and pack that folder (`pack`) into `archive\pc\mod\AmbushAftermathFix.archive`.

## Credits

Built it with Claude (the AI).

## Licence

MIT
