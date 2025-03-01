# Important Files

This document provides a brief overview of key files in the KBL Bot project. Each file serves a specific purpose and is tailored for the KBL Server. If you wish to adapt these files for your own server, please read the notes carefully.

## 1. admin.py
This file contains commands specifically designed for the KBL Server, including:
- `ma`, `mb`, `mc`: Commands related to member management.
- `ba`, `bb`, `bc`: Commands for handling specific roles.
- `setlp`, `clearlp`: Commands for managing Ligtas Points.

**Note**: If you wish to use this in your own server, you will need to tweak it and replace some objects with your own. You must be fluent in reading Python and understanding Discord development. Otherwise, feel free to remove or comment out this file.

## 2. background_process.py
This file handles all events and background processes catered to the KBL Server.

**Note**: If you wish to use this in your own server, you will need to tweak it and replace some objects with your own. You must be fluent in reading Python and understanding Discord development. Otherwise, feel free to remove or comment out this file.

## 3. monthly_awards.py
This file manages the monthly awards system for the KBL Server.

**Note**: If you wish to use this in your own server, you will need to tweak it and replace some objects with your own. You must be fluent in reading Python and understanding Discord development. Otherwise, feel free to remove or comment out this file.

**P.S.** For current issues relating to this, check [ERRORS.md](../ERRORS.md).

## 4. rankings.py
This file contains commands related to user rankings on the KBL Server.

**Note**: If you wish to use this in your own server, you will need to tweak it and replace some objects with your own. You must be fluent in reading Python and understanding Discord development. Otherwise, feel free to remove or comment out this file.

**P.S.** Shop & Ranksettings are currently disabled due to recent deletion of assets.

## 5. utility.py
This file includes various utility commands for the KBL Server, such as:
- `botstats`: Displays bot statistics.
- `channels`: Provides information about channels.
- `minecraft`: Commands related to Minecraft.

**Note**: If you wish to use this in your own server, you will need to tweak it and replace some objects with your own. You must be fluent in reading Python and understanding Discord development. Otherwise, feel free to remove or comment out this file.

**P.S.** The `channels` command is initially commented out due to the fact that it generates too much processing, potentially overwhelming your server or computer. Re-enabling this might crash your computer, so use it with caution.