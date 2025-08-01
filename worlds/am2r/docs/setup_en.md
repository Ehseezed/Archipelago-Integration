# AM2R Archipelago Setup Guide

## Required Software
- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases/latest)
- Legacy Mods (Old Trap Behavior)
  - [AM2R Multiworld](https://github.com/DodoBirby/AM2R-Multiworld-Mod/releases/latest) 
  - [AM2R Multisquared](https://github.com/rm-steele/AM2R-Multisquared/releases/tag/1.0.0)
  - [AM2R Multiworld: Resplashed](https://github.com/AbyssalCreature/AM2R-Re-Splashed/releases/tag/v1.3.2-M)
- Current Mods (New Trap Behavior)
  - [AM2R Multiworld(²)](https://github.com/rm-steele/AM2R-Multisquared/releases/latest)
  - [AM2R Multiworld: Resplashed](https://github.com/AbyssalCreature/AM2R-Re-Splashed/releases?q=multiworld&expanded=true)
- [AM2R Launcher](https://github.com/AM2R-Community-Developers/AM2RLauncher/releases/latest)
- Your self provided copy of AM2R 1.1 for the launcher

## Optional Software
- [Sublime Text](https://www.sublimetext.com/) or [Notepad++](https://notepad-plus-plus.org/downloads/) for easy editing of `.yaml` files
- [Poptracker](https://github.com/black-sliver/PopTracker/releases) and the [AM2R Tracker](https://github.com/Ehseezed/AM2R-Tracker/releases) pack for a map tracker 
- [Universal Tracker](https://github.com/FarisTheAncient/Archipelago/releases?q=Tracker&expanded=true) for an updating list of available checks

## Installation Process

### Installing Multiworld Mod

Download and set up the latest release of [AM2R Launcher](https://github.com/AM2R-Community-Developers/AM2RLauncher/releases) using your copy of AM2R 1.1 then in the launcher you can
under the `Mod Settings` tab, hit the `ADD NEW MOD` button, and select Multiworld mod `.zip` file from either of the Multiworld Mod downloads.

Finally, from the `Play` tab select the `Multiworld` profile and hit `Install` and then play to load up the mod.


### Installing `am2r.apworld`

After downloading the `am2r.apworld` file you can either run the `am2r.apworld` file directly, use the 
`ArchipelagoLauncher` executable from your [Archipelago Install](https://github.com/ArchipelagoMW/Archipelago/releases/latest) and the `Install APWorld` button, 
or you can move it to `custom_worlds` manually in the Archipelago installation root directory. 

From there you can use the `Archipelago Launcher` to find and open `AM2R Client` in the future steps.

## Hosting a Multiworld Session

After collecting all the players `.yaml` files and placing them into the `/players` folder you can run `Archipelago Generate`
at which point it may ask you for roms if needed. If you do not have the roms you cannot generate the seed, and you will
need somebody else with all the roms to generate the seed for the group.

After the generation is complete there will be a `.zip` file in the `/output` folder of the Archipelago installation 
that you can then upload directly to the [Archipelago Website](https://archipelago.gg/uploads) to host the session, or 
you can utilize the `Archipelago Server` to host the session yourself.

## Joining a Multiworld Session

### Creating a `.yaml` file

In the `Archipelago Launcher` hit the `Generate Template Settings` button which will generate a default `.yaml` file
for all your currently installed worlds, this will add a `am2r.yaml` file to the `/players/templates` folder of the
Archipelago installation.

The `.yaml` file is a special text file that can be edited in any text editor including your OS's default text editor.
I would recommend installing at least [Sublime Text](https://www.sublimetext.com/) or [Notepad++](https://notepad-plus-plus.org/downloads/) for the easiest experience.

The `.yaml` file will look something like this:
```yaml
AM2R:
  setting 1:
    option 1: 50
    option 2: 0
    option 3: 0
    option 4: 0
    
  setting 2:
    option 1: 50
    option 2: 25
    option 3: 10
    option 4: 0
```
To make a setting guaranteed it needs to be the only one with any value other than 0 but if you wanted it to be random
you can add values to multiple options, and it will pick one at random with the formula of `option_value/total_setting_values`.  
So for `setting 1` it would always pick `option 1` and for `setting 2` it would pick `option 1` `50/85` of the time, `option 2` `25/85` of the time, and `option 3` `10/85` of the time.

After setting up the `.yaml` file you can save it and then send it to the host.

### Joining the Session

After the host has generated the seed and has given you the connection information you can use the `Archipelago Launcher` 
to run the `AM2R Client` after that run the AM2R Multiworld Mod and go to the settings to find the `Multiworld` menu to enter 
the slot name (player name) and hit `Connect to Python Client` the client will then show `Successfully Connected to AM2R`
at which point you can run /connect [IP]:[PORT] or use the address bar at the top with the same formatting to connect to the
multiworld session at which point you can start a new save file or continue a save file.

# Things are subject to change at developer discretion

### Seeds should be beatable but its possible there are still logical errors

## Bug Reporting/Feature Requests

If you are playing this mod and are encountering bugs **DO NOT** report them to the Archipelago server this is not official support from them, and they may or may not know what to do instead you can report them to the dedicated mod thread on the [AM2R Server](https://discord.gg/YTQnkAJ) or on the [Modding Server](https://discord.gg/Fdq3MSXEDb) and you can always open an issue on the GitHub.

### Help I don't have enough energy to do this check with 100% trap fill on fusion mode

Fuck you, if the testers can do it you can too, and if you cant do it play on an easier difficulty.

> "no one plays on hard dude" - a tester

## Randomizer Information

### What is randomized?

All items both majors and minors are randomized together in one pool with the option to add in the metroids as checks too.

### What is the goal?

The goal of this AM2R randomizer implementation is to kill or collect the self specified number of metroids to reach the queen metroid and save the baby metroid.

This message is sponsored by "The Galactic Federation"

### I softlocked myself

Don't worry all items are saved by the server, but you should in theory never need to softlock yourself to beat the game unless I messed up
