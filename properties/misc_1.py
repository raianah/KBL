import asyncio, datetime
from typing import List, Dict, Any, Optional
from mizuki.db import db
from disnake import Embed, Color, File, ButtonStyle, File, Interaction, ApplicationCommandInteraction, Message
from disnake.ui import View, button, select, Select, Button
from disnake.ext.menus import PageSource, ListPageSource
from disnake.utils import maybe_coroutine
from easy_pil import Editor, load_image_async, Font
from millify import millify

def tc_check_ownership(interaction):
    tc1, tc2, tc3, tc4, tc5, tc6, tc7, tc8, tc9 = db.record("SELECT TextColor1, TextColor2, TextColor3, TextColor4, TextColor5, TextColor6, TextColor7, TextColor8, TextColor9 FROM colors WHERE UserID = ?", interaction.author.id)
    if tc1 == 0:
        price_1 = "Price: <:money_icon:1075986284461445140> **500**"
    else:
        price_1 = "Price: **Owned**"
    if tc2 == 0:
        price_2 = "Price: <:money_icon:1075986284461445140> **500**"
    else:
        price_2 = "Price: **Owned**"
    if tc3 == 0:
        price_3 = "Price: <:money_icon:1075986284461445140> **500**"
    else:
        price_3 = "Price: **Owned**"
    if tc4 == 0:
        price_4 = "Price: <:money_icon:1075986284461445140> **500**"
    else:
        price_4 = "Price: **Owned**"
    if tc5 == 0:
        price_5 = "Price: <:money_icon:1075986284461445140> **500**"
    else:
        price_5 = "Price: **Owned**"
    if tc6 == 0:
        price_6 = "Price: <:money_icon:1075986284461445140> **500**"
    else:
        price_6 = "Price: **Owned**"
    if tc7 == 0:
        price_7 = "Price: <:money_icon:1075986284461445140> **500**"
    else:
        price_7 = "Price: **Owned**"
    if tc8 == 0:
        price_8 = "Price: <:money_icon:1075986284461445140> **500**"
    else:
        price_8 = "Price: **Owned**"
    if tc9 == 0:
        price_9 = "Price: <:money_icon:1075986284461445140> **500**"
    else:
        price_9 = "Price: **Owned**"
    return [price_1, price_2, price_3, price_4, price_5, price_6, price_7, price_8, price_9]

def bn_check_ownership(interaction):
    bn1, bn2 = db.record("SELECT Banner1, Banner2 FROM items WHERE UserID = ?", interaction.author.id)
    if bn1 == 0:
        price_1 = "Price: <:money_icon:1075986284461445140> **750**"
    else:
        price_1 = "Price: **Owned**"
    if bn2 == 0:
        price_2 = "Price: <:money_icon:1075986284461445140> **750**"
    else:
        price_2 = "Price: **Owned**"
    return [price_1, price_2]

def ol_check_ownership(interaction):
    ol1, ol2, ol3, ol4, ol5, ol6 = db.record("SELECT OutlineColor1, OutlineColor2, OutlineColor3, OutlineColor4, OutlineColor5, OutlineColor6 FROM colors WHERE UserID = ?", interaction.author.id)
    if ol1 == 0:
        price_1 = "Price: <:money_icon:1075986284461445140> **500**"
    else:
        price_1 = "Price: **Owned**"
    if ol2 == 0:
        price_2 = "Price: <:money_icon:1075986284461445140> **500**"
    else:
        price_2 = "Price: **Owned**"
    if ol3 == 0:
        price_3 = "Price: <:money_icon:1075986284461445140> **500**"
    else:
        price_3 = "Price: **Owned**"
    if ol4 == 0:
        price_4 = "Price: <:money_icon:1075986284461445140> **500**"
    else:
        price_4 = "Price: **Owned**"
    if ol5 == 0:
        price_5 = "Price: <:money_icon:1075986284461445140> **500**"
    else:
        price_5 = "Price: **Owned**"
    if ol6 == 0:
        price_6 = "Price: <:money_icon:1075986284461445140> **500**"
    else:
        price_6 = "Price: **Owned**"
    return [price_1, price_2, price_3, price_4, price_5, price_6]

def rank_banner_check(value):
    if value == "":
        profile_banner = Editor("./properties/assets/cyber_banner.png").resize((464, 1010))
    elif value == "Banner1":
        profile_banner = Editor("./properties/assets/glory_banner.png").resize((464, 1010))
    elif value == "Banner2":
        profile_banner = Editor("./properties/assets/nature_banner.png").resize((464, 1010))
    return profile_banner

def rank_text_color_check(value):
    if value == "":
        color = "#FFFFFF"
    elif value == "TextColor1":
        color = "#F88379"
    elif value == "TextColor2":
        color = "#FFF44F"
    elif value == "TextColor3":
        color = "#F5DEB3"
    elif value == "TextColor4":
        color = "#CD7F32"
    elif value == "TextColor5":
        color = "#40E0D0"
    elif value == "TextColor6":
        color = "#6A5ACD"
    elif value == "TextColor7":
        color = "#50C878"
    return color
    
def rank_outline_color_check(value):
    if value == "":
        color1, color2 = "#000000", "#FFFFFF"
    elif value == "OutlineColor1":
        color1, color2 = "#482882", "#0E081A"
    elif value == "OutlineColor2":
        color1, color2 = "#2E5793", "#09111D"
    elif value == "OutlineColor3":
        color1, color2 = "#277145", "#07160D"
    elif value == "OutlineColor4":
        color1, color2 = "#C4A705", "#272101"
    elif value == "OutlineColor5":
        color1, color2 = "#C96112", "#281303"
    elif value == "OutlineColor6":
        color1, color2 = "#C1301C", "#260905"
    return color1, color2

def check_new_username(user):
    if user.discriminator == "#0":
        return user.name
    else:
        return user

async def help_(command, ctx):
    if command == None:
        new_list, inv_list, admin_list, acc_list, utility_list, leveling_list, commands = [], [], [], [], [], [], []

        for role in ctx.author.roles:
            if role.id == 1001430287143669800:
                # ACC_LIST
                acc_list.append("• ` ba `\n<:reply:1094561143911100447> *Accepts <@&961964769772961822> members (w/ <@&962169029601144862> role) role to **Lapagan Category** only.*")
                acc_list.append("• ` bb `\n<:reply:1094561143911100447> *Accepts <@&961964769772961822> members (w/ <@&962169029601144862> role) role to **Lipunan Category** only.*")
                acc_list.append("• ` bc `\n<:reply:1094561143911100447> *Accepts <@&961964769772961822> members (w/ <@&962169029601144862> role) role to **Both Categories**.*")
                acc_list.append("• ` ma `\n<:reply:1094561143911100447> *Accepts <@&961964769772961822> members (w/ <@&962169020151394394> role) role to **Lapagan Category** only.*")
                acc_list.append("• ` mb `\n<:reply:1094561143911100447> *Accepts <@&961964769772961822> members (w/ <@&962169020151394394> role) role to **Lipunan Category** only.*")
                acc_list.append("• ` mc `\n<:reply:1094561143911100447> *Accepts <@&961964769772961822> members (w/ <@&962169020151394394> role) role to **Both Categories** only.*")
                acc_list.sort()
                inv_list.extend(acc_list)
                commands.append("• Tanod Commands")

        if ctx.author.guild_permissions.administrator:
            # ADMIN_LIST
            admin_list.append("• ` set-level `\n<:reply:1094561143911100447> *Manually sets a user's level according to choice of category. Use `.help set-level` to view more usage.*")
            admin_list.append("• ` set-xp `\n<:reply:1094561143911100447> *Manually sets a user's xp according to choice of category. Use `.help set-xp` to view more usage.*")
            admin_list.append("• ` set-lp `\n<:reply:1094561143911100447> *Manually sets a user's **Ligtas Points (LP)**.*")
            admin_list.append("• ` clear-lp `\n<:reply:1094561143911100447> *Clears a user's **Ligtas Points (LP)**.  Use `.help clear-lp` to view more usage.*")
            admin_list.append("• ` approve `\n<:reply:1094561143911100447> *Approves a starboard entry to be posted in <#1048837480700465202>.*")
            admin_list.append("• ` reject `\n<:reply:1094561143911100447> *Rejects a starboard entry.*")
            admin_list.sort()
            inv_list.extend(admin_list)
            commands.append("• Admin Commands")

        # UTILITY_LIST
        utility_list.append("• ` avatar `\n<:reply:1094561143911100447> *Shows your avatar or member's avatar.*")
        utility_list.append("• ` bots `\n<:reply:1094561143911100447> *View bot lists, bot category, or bot information in the server.*")
        utility_list.append("• ` channels `\n<:reply:1094561143911100447> *View channel information. Use `.help channels` to view more usage.*")
        utility_list.append("• ` events `\n<:reply:1094561143911100447> *View current, and future events in the server.*")
        utility_list.append("• ` help `\n<:reply:1094561143911100447> ***You are here***")
        utility_list.append("• ` minecraft `\n<:reply:1094561143911100447> *View minecraft-related stuffs here. Use `.help minecraft` to view more usage.*")
        utility_list.append("• ` ping `\n<:reply:1094561143911100447> *Pong!*")
        utility_list.append("• ` roles `\n<:reply:1094561143911100447> *View role information. Use `.help roles` to view more usage.*")
        utility_list.append("• ` serverinfo `\n<:reply:1094561143911100447> *View server information.*")
        utility_list.append("• ` botstats `\n<:reply:1094561143911100447> *View bot-related stuffs here.*")
        utility_list.append("• ` userinfo `\n<:reply:1094561143911100447> *Shows your user information or member's user information.*")
        utility_list.append("• ` starboard `\n<:reply:1094561143911100447> *Shows a starboard entry based on the input key. Key must be valid.*")
        utility_list.append("• ` partnership `\n<:reply:1094561143911100447> *Views list of partnered servers. Use `.help partnership` to view more usage.*")
        utility_list.sort()
        commands.append("• Utility Commands")

        # LEVELING_LIST
        leveling_list.append("~~• ` rank `\n<:reply:1094561143911100447> *Shows your rank or member's rank.*~~")
        leveling_list.append("~~• ` shop `\n<:reply:1094561143911100447> *Enter the shop to purchase items and emblems.*~~")
        leveling_list.append("~~• ` ranksettings `\n<:reply:1094561143911100447> *Customize your rank card here.*~~")
        leveling_list.append("• ` leaderboards `\n<:reply:1094561143911100447> *Shows rankings according to given category. Use `.help leaderboards` to view more usage.*")
        leveling_list.append("~~• ` vote `\n<:reply:1094561143911100447> *Vote KBL in exchange for vote-exclusive goodies!*~~")
        leveling_list.append("~~• ` stats `\n<:reply:1094561143911100447> *Shows your current stats or member's current stats.*~~")
        leveling_list.append("• ` points `\n<:reply:1094561143911100447> *Shows your current **Solid Points (SP)** and **Ligtas Points (LP)**.*")
        leveling_list.append("• ` trophy `\n<:reply:1094561143911100447> *Shows your or user's trophy collection.*")
        leveling_list.append("• ` solidpoints `\n<:reply:1094561143911100447> *Shows SP rankings according to given category. Use `.help solidpoints` to view more usage.*")
        leveling_list.sort()
        commands.append("• Leveling Commands")

        inv_list.extend(utility_list)
        inv_list.extend(leveling_list)
        #print(len(inv_list))
        categories = "\n".join([item for item in commands])

        embed = Embed(description=f"Use `.help` for general help and provide with `query` to give examples on command usage.", color=0x2f3136).set_author(name="KBL BOT - HELP COMMAND", url="https://docs.porcopion.xyz/", icon_url=ctx.author.avatar)
        embed.add_field(name="Command Categories:", value=f"{categories}")
        embed.add_field(name="Links:", value="• [top.gg](https://top.gg/servers/961502956195303494)\n• [discord.io](https://discord.io/kblipunan)\n• [<:fb:992030569716252822> Facebook](https://www.facebook.com/kblipunan)\n• [<:yt:992030607720845373> Youtube](https://www.youtube.com/kblipunan)").set_footer(text=f"Command executed by: {ctx.author}", icon_url=ctx.author.avatar).set_thumbnail(url=ctx.guild.icon)

        commands0 = "\n\n".join([item for item in inv_list[:7]])
        commands1 = "\n\n".join([item for item in inv_list[7:14]])
        embed0 = Embed(description=commands0, color=0x2f3136).set_footer(text="To view usage of commands, use .help <command>", icon_url=ctx.author.avatar)
        embed1 = Embed(description=commands1, color=0x2f3136).set_footer(text="To view usage of commands, use .help <command>", icon_url=ctx.author.avatar)
        new_list.extend([embed0, embed1])
        if len(inv_list) >= 14:
            commands2 = "\n\n".join([item for item in inv_list[14:21]])
            embed2 = Embed(description=commands2, color=0x2f3136).set_footer(text="To view usage of commands, use .help <command>", icon_url=ctx.author.avatar)
            new_list.append(embed2)
            if len(inv_list) >= 21:
                commands3 = "\n\n".join([item for item in inv_list[21:28]])
                embed3 = Embed(description=commands3, color=0x2f3136).set_footer(text="To view usage of commands, use .help <command>", icon_url=ctx.author.avatar)
                new_list.append(embed3)
                if len(inv_list) >= 28:
                    commands4 = "\n\n".join([item for item in inv_list[28:35]])
                    embed4 = Embed(description=commands4, color=0x2f3136).set_footer(text="To view usage of commands, use .help <command>", icon_url=ctx.author.avatar)
                    new_list.append(embed4)
        await ctx.send(embed=embed, view=HelpView(ctx, new_list))
    else:
        embed=Embed(color=0x2f3136).set_author(name=f"Help Command • Prefix: .", icon_url=ctx.guild.me.avatar)
        embed.set_footer(text=f"[] = required | <> = optional • Use .help for all commands.", icon_url=ctx.author.display_avatar)
        # TANOD
        if command.lower() == "ba":
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mTanod (Moderator)[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35mN/A[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36m[user] <suffix>[0;0m```")
            embed.add_field(name="Description:", value="```yaml\nSuffix: --fix\n\nAccepts \"Baguhan\" members (w/ \"Bata\" role) role to Lapagan Category only.```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.ba @thethimteam\n.ba @thethimteam --fix[0;0m```", inline=False)
        elif command.lower() == "bb":
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mTanod (Moderator)[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35mN/A[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36m[user] <suffix>[0;0m```")
            embed.add_field(name="Description:", value="```yaml\nSuffix: --fix\n\nAccepts \"Baguhan\" members (w/ \"Bata\" role) role to Lipunan Category only.```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.bb @thethimteam\n.bb @thethimteam --fix[0;0m```", inline=False)
        elif command.lower() == "bc":
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mTanod (Moderator)[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35mN/A[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36m[user] <suffix>[0;0m```")
            embed.add_field(name="Description:", value="```yaml\nSuffix: --fix\n\nAccepts \"Baguhan\" members (w/ \"Bata\" role) role to Both Categories.```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.bc @thethimteam\n.bc @thethimteam --fix[0;0m```", inline=False)
        elif command.lower() == "ma":
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mTanod (Moderator)[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35mN/A[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36m[user] <suffix>[0;0m```")
            embed.add_field(name="Description:", value="```yaml\nSuffix: --fix\n\nAccepts \"Baguhan\" members (w/ \"Matanda\" role) role to Lapagan Category only.```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.ma @thethimteam\n.ma @thethimteam --fix[0;0m```", inline=False)
        elif command.lower() == "mb":
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mTanod (Moderator)[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35mN/A[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36m[user] <suffix>[0;0m```")
            embed.add_field(name="Description:", value="```yaml\nSuffix: --fix\n\nAccepts \"Baguhan\" members (w/ \"Matanda\" role) role to Lipunan Category only.```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.mb @thethimteam\n.mb @thethimteam --fix[0;0m```", inline=False)
        elif command.lower() == "mc":
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mTanod (Moderator)[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35mN/A[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36m[user] <suffix>[0;0m```")
            embed.add_field(name="Description:", value="```yaml\nSuffix: --fix\n\nAccepts \"Baguhan\" members (w/ \"Matanda\" role) role to Both Categories.```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.mc @thethimteam\n.mc @thethimteam --fix[0;0m```", inline=False)
        # ADMIN
        elif command.lower() in ["setxp", "sxp", "set-xp"]:
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mAdmin[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35msetxp, sxp[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36m[user] [amount/suffix] <suffix>[0;0m```")
            embed.add_field(name="Description:", value="```yaml\nSuffix: --memes\n\nManually sets a user's xp according to choice of category.```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.set-xp @thethimteam 30\n		↳ Lipunan Category\n.set-xp @thethimteam 30 --memes\n		↳ Lapagan Category[0;0m```", inline=False)
        elif command.lower() in ["slvl", "set-level"]:
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mAdmin[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35mslvl[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36m[user] [amount/suffix] <suffix>[0;0m```")
            embed.add_field(name="Description:", value="```yaml\nSuffix: --memes\n\nManually sets a user's level according to choice of category.```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.set-level @thethimteam 3\n		↳ Lipunan Category\n.set-level @thethimteam 3 --memes\n		↳ Lapagan Category[0;0m```", inline=False)
        elif command.lower() in ["setlp", "set-lp", "slp"]:
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mAdmin[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35msetlp, slp[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36m[user] <amount>[0;0m```")
            embed.add_field(name="Description:", value="```yaml\nManually sets a user's Ligtas Points (LP).```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.set-lp @thethimteam\n		↳ +1 LP\n.set-lp @thethimteam 5\n		↳ +5 LP[0;0m```", inline=False)
        elif command.lower() in ["clearlp", "clear-lp", "clp"]:
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mAdmin[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35mclearlp, clp[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36m[user/suffix][0;0m```")
            embed.add_field(name="Description:", value="```yaml\nSuffix: --all, --everyone\n\nClears a user's Ligtas Points (LP).```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.clear-lp @thethimteam\n.clear-lp --all[0;0m```", inline=False)
        elif command.lower() in ["approve", "approved", "apr"]:
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mAdmin[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35mapproved, apr[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36m[key] <remarks>[0;0m```")
            embed.add_field(name="Description:", value="```yaml\nApproves a starboard entry to be posted in #『🤪』kblastugan. Use .starboard to view valid keys.```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.approve abcd1\n.approve abcd1 Cool meme![0;0m```", inline=False)
        elif command.lower() in ["reject", "rejected", "rej"]:
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mAdmin[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35mrejected, rej[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36m[key] <remarks>[0;0m```")
            embed.add_field(name="Description:", value="```yaml\nRejects a starboard entry.```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.reject abcd1\n.reject abcd1 Not funny.[0;0m```", inline=False)
        # UTILITY
        elif command.lower() in ["avatar", "av"]:
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mUtility[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35mavatar, av[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36m<user>[0;0m```")
            embed.add_field(name="Description:", value="```yaml\nShows your avatar or member's avatar.```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.avatar\n.av @thethimteam[0;0m```", inline=False)
        elif command.lower() in ["bots", "bot"]:
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mUtility[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35mbot[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36m<bot_user/category>[0;0m```")
            embed.add_field(name="Description:", value="```yaml\nCategories: Moderation, Leveling, Game, Music, Others\n\nView bot lists, bot category, or bot information in the server.```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.bots\n.bot moderation\n.bot @KBL Bot[0;0m```", inline=False)
        elif command.lower() in ["channels", "channel", "ch"]:
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mUtility[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35mchannel, ch[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36m<channel>[0;0m```")
            embed.add_field(name="Description:", value="```yaml\nView channel information. Use .help channels to view more usage.```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.channels\n.channel #『🗣』bulwagan[0;0m```", inline=False)
        elif command.lower() in ["events", "event"]:
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mUtility[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35mevent[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36m<num>[0;0m```")
            embed.add_field(name="Description:", value="```yaml\nView current, and future events in the server.```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.events\n.event 1[0;0m```", inline=False)
        elif command.lower() in ["help"]:
            return await ctx.send("Congratulations, you helped yourself.")
        elif command.lower() in ["minecraft", "mcc", "mca"]:
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mUtility[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35mmcc, mca[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36m<suffix>[0;0m```")
            embed.add_field(name="Description:", value="```yaml\nSuffixes: --status, --start, --version\n\nView minecraft-related stuffs here.```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.minecraft\n.mcc --status[0;0m```", inline=False)
        elif command.lower() in ["ping"]:
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mUtility[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35mN/A[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36mN/A[0;0m```")
            embed.add_field(name="Description:", value="```yaml\nPong!```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.ping[0;0m```", inline=False)
        elif command.lower() in ["roles", "role"]:
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mUtility[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35mrole[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36m<role/category>[0;0m```")
            embed.add_field(name="Description:", value="```yaml\nCategories: Lipunan, Lapagan, Mod, GNL, Custom Roles, Subjects, Games, Interest, Age\n\nView role information. Use `.help channels` to view more usage.```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.roles\n.role @Baguhan\n.role lipunan[0;0m```", inline=False)
        elif command.lower() in ["serverinfo", "si"]:
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mUtility[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35msi[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36mN/A[0;0m```")
            embed.add_field(name="Description:", value="```yaml\n*View server information.```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.serverinfo\n.si[0;0m```", inline=False)
        elif command.lower() in ["botstats", "botstat"]:
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mUtility[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35mbotstat[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36mN/A[0;0m```")
            embed.add_field(name="Description:", value="```yaml\n*View bot-related stuffs here.```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.botstats\n.botstat[0;0m```", inline=False)
        elif command.lower() in ["userinfo", "ui", "ako"]:
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mUtility[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35mui, ako[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36m<user>[0;0m```")
            embed.add_field(name="Description:", value="```yaml\nShows your user information or member's user information.```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.userinfo\n.ui @thethimteam\n.ako[0;0m```", inline=False)
        elif command.lower() in ["starboard", "str"]:
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mUtility[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35mstr[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36m<key>[0;0m```")
            embed.add_field(name="Description:", value="```yaml\nShows a starboard entry based on the input key. Key must be valid.```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.starboard\n.str abcd1[0;0m```", inline=False)
        elif command.lower() in ["partnership", "partnered", "partner"]:
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mUtility[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35mpartnered, partner[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36m<user> <server_name> <server_link> <description>[0;0m```")
            embed.add_field(name="Description:", value="```yaml\nUser Permission (default): Views list of partnered servers.\nAdmin Permission: Creates a new partnership information. Use --remove on <server_name> to remove the partnership!```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.partnership\n.partner @thethimteam\n.partner @thethimteam \"Bobong Lipunan\" https://discord.gg/kbl \"Your description here...\"[0;0m```", inline=False)
        # RANK
        elif command.lower() in ["leaderboards", "lb", "top"]:
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mRanking[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35mlb, top[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36m<suffix>[0;0m```")
            embed.add_field(name="Description:", value="```yaml\nSuffixes: --meme, --message, --ligtas, --coins\n\nShows rankings according to given category.```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.leaderboards\n.lb --meme[0;0m```", inline=False)
        elif command.lower() in ["points", "point", "pt"]:
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mRanking[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35mpoint, pt[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36m<user>[0;0m```")
            embed.add_field(name="Description:", value="```yaml\nShows your current Solid Points (SP) and Ligtas Points (LP)```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.points\n.pt @thethimteam[0;0m```", inline=False)
        elif command.lower() in ["trophy", "tro", "c"]:
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mRanking[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35mtro, c[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36m<user>[0;0m```")
            embed.add_field(name="Description:", value="```yaml\nShows your or user's trophy collection.```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.trophy\n.c @thethimteam[0;0m```", inline=False)
        elif command.lower() in ["solidpoints", "sp"]:
            embed.add_field(name="Category:", value="```ansi\n[0;40;33mRanking[0;0m```").add_field(name="Alias/es:", value="```ansi\n[0;35msp[0;0m```")
            embed.add_field(name="Parameters:", value="```ansi\n[0;36m<suffix>[0;0m```")
            embed.add_field(name="Description:", value="```yaml\nSuffixes: --yearly, --monthly\n\nShows SP rankings according to given category.```")
            embed.add_field(name="Usage", value=f"```ansi\n[0;34m.solidpoints\n.sp --yearly[0;0m```", inline=False)
        else:
            return await ctx.send(f"`.{command}` does not exist in the official list. Try `.help` instead.")
        await ctx.send(embed=embed)

class ShortPagination(View):
    def __init__(self, ctx: ApplicationCommandInteraction, embeds: List[Embed]):
        super().__init__(timeout=None)
        #self.ctx = ctx
        self.embeds = embeds
        self.count = 0

        self.button_1.disabled = True

    @button(style=ButtonStyle.green, label="<")
    async def button_1(self, button: Button, interaction: Interaction):
        self.count -= 1
        self.button_3.disabled = False
        if self.count == 0:
            self.button_1.disabled = True
        await interaction.response.edit_message(embed=self.embeds[self.count], view=self)

    @button(style=ButtonStyle.red, emoji="<:crossmark:895850018035101757>")
    async def button_2(self, button: Button, interaction: Interaction):
        await interaction.response.edit_message(embed=self.embeds[self.count], view=None)
        self.stop()
    
    @button(style=ButtonStyle.green, label=">")
    async def button_3(self, button: Button, interaction: Interaction):
        self.count += 1
        self.button_1.disabled = False
        if self.count == len(self.embeds) - 1:
            self.button_3.disabled = True
        await interaction.response.edit_message(embed=self.embeds[self.count], view=self)

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.author.id == self.ctx.author.id:
            return True
        await interaction.response.send_message(content="It is not your command.", ephemeral=True)
        return False

class LongPagination(View):
    def __init__(self, ctx: ApplicationCommandInteraction, embeds: List[Embed]):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.embeds = embeds
        self.count = 0

        self.button_1.disabled = True
        self.button_2.disabled = True
        self.button_1.style = ButtonStyle.red
        self.button_2.style = ButtonStyle.red

        if len(self.embeds) > 5:
            self.button_5.disabled = False
            self.button_5.style = ButtonStyle.green
        else:
            self.button_5.disabled = True
            self.button_5.style = ButtonStyle.red

    @button(style=ButtonStyle.green, label="≪")
    async def button_1(self, button: Button, interaction: Interaction):
        self.count -= 5
        if self.count > len(self.embeds) - 6: # ≫
            self.button_5.disabled = True
            self.button_5.style = ButtonStyle.red
        else:
            self.button_5.disabled = False
            self.button_5.style = ButtonStyle.green
        if self.count == len(self.embeds) - 1: # >
            self.button_4.disabled = True
            self.button_4.style = ButtonStyle.red
        else:
            self.button_4.disabled = False
            self.button_4.style = ButtonStyle.green
        if self.count == 0: # <
            self.button_2.disabled = True
            self.button_2.style = ButtonStyle.red
        else:
            self.button_2.disabled = False
            self.button_2.style = ButtonStyle.green
        if self.count < 5: # ≪
            self.button_1.disabled = True
            self.button_1.style = ButtonStyle.red
        else:
            self.button_1.disabled = False
            self.button_1.style = ButtonStyle.green
        await interaction.response.edit_message(embed=self.embeds[self.count], view=self)

    @button(style=ButtonStyle.green, label="<")
    async def button_2(self, button: Button, interaction: Interaction):
        self.count -= 1
        if self.count > len(self.embeds) - 6: # ≫
            self.button_5.disabled = True
            self.button_5.style = ButtonStyle.red
        else:
            self.button_5.disabled = False
            self.button_5.style = ButtonStyle.green
        if self.count == len(self.embeds) - 1: # >
            self.button_4.disabled = True
            self.button_4.style = ButtonStyle.red
        else:
            self.button_4.disabled = False
            self.button_4.style = ButtonStyle.green
        if self.count == 0: # <
            self.button_2.disabled = True
            self.button_2.style = ButtonStyle.red
        else:
            self.button_2.disabled = False
            self.button_2.style = ButtonStyle.green
        if self.count < 5: # ≪
            self.button_1.disabled = True
            self.button_1.disabled = ButtonStyle.red
        else:
            self.button_1.disabled = False
            self.button_1.style = ButtonStyle.green
        await interaction.response.edit_message(embed=self.embeds[self.count], view=self)

    @button(style=ButtonStyle.red, label="❌")
    async def button_3(self, button: Button, interaction: Interaction):
        await interaction.response.edit_message(embed=self.embeds[self.count], view=None)
        self.stop()

    @button(style=ButtonStyle.green, label=">")
    async def button_4(self, button: Button, interaction: Interaction):
        self.count += 1
        if self.count > len(self.embeds) - 6: # ≫
            self.button_5.disabled = True
            self.button_5.style = ButtonStyle.red
        else:
            self.button_5.disabled = False
            self.button_5.style = ButtonStyle.green
        if self.count == len(self.embeds) - 1: # >
            self.button_4.disabled = True
            self.button_4.style = ButtonStyle.red
        else:
            self.button_4.disabled = False
            self.button_4.style = ButtonStyle.green
        if self.count == 0: # <
            self.button_2.disabled = True
            self.button_2.style = ButtonStyle.red
        else:
            self.button_2.disabled = False
            self.button_2.style = ButtonStyle.green
        if self.count < 5: # ≪
            self.button_1.disabled = True
            self.button_1.disabled = ButtonStyle.red
        else:
            self.button_1.disabled = False
            self.button_1.style = ButtonStyle.green
        await interaction.response.edit_message(embed=self.embeds[self.count], view=self)

    @button(style=ButtonStyle.green, label="≫")
    async def button_5(self, button: Button, interaction: Interaction):
        self.count += 5
        if self.count > len(self.embeds) - 6: # ≫
            self.button_5.disabled = True
            self.button_5.style = ButtonStyle.red
        else:
            self.button_5.disabled = False
            self.button_5.style = ButtonStyle.green
        if self.count == len(self.embeds) - 1: # >
            self.button_4.disabled = True
            self.button_4.style = ButtonStyle.red
        else:
            self.button_4.disabled = False
            self.button_4.style = ButtonStyle.green
        if self.count == 0: # <
            self.button_2.disabled = True
            self.button_2.style = ButtonStyle.red
        else:
            self.button_2.disabled = False
            self.button_2.style = ButtonStyle.green
        if self.count < 5: # ≪
            self.button_1.disabled = True
            self.button_1.disabled = ButtonStyle.red
        else:
            self.button_1.disabled = False
            self.button_1.style = ButtonStyle.green
        await interaction.response.edit_message(embed=self.embeds[self.count], view=self)

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.author.id == self.ctx.author.id:
            return True
        await interaction.response.send_message(content="It is not your command.", ephemeral=True)
        return False

class HelpView(View):
    def __init__(self, ctx: ApplicationCommandInteraction, embeds: List[Embed]):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.embeds = embeds
        self.count = 0

        self.button_1.disabled = True
        self.button_2.disabled = True
        self.button_1.style = ButtonStyle.red
        self.button_2.style = ButtonStyle.red

        for role in self.ctx.author.roles:
            if role.id == 1001430287143669800:
                self.select_1.add_option(label="Tanod Commands", value="Tanod")
        if self.ctx.author.guild_permissions.administrator:
            self.select_1.add_option(label="Admin Commands", value="Admin")
        self.select_1.add_option(label="Leveling Commands", value="Leveling")
        self.select_1.add_option(label="Utility Commands", value="Utility")
        self.select_1.add_option(label="All Commands", value="Overall")
        self.select_1.add_option(label="Exit", value="x", emoji="❌")

        self.select_1.max_values = 4

    @select(min_values=1)
    async def select_1(self, select: Select, interaction: Interaction):
        coms = ", ".join([f"{item}" for item in select.values])
        self.embeds = []
        select.placeholder = coms
        if "x" in select.values:
            await interaction.response.edit_message(view=None)
            self.stop()
        if "Overall" in select.values:
            self.count = 0
            new_list, inv_list, admin_list, acc_list, utility_list, leveling_list, commands = [], [], [], [], [], [], []

            for role in self.ctx.author.roles:
                if role.id == 1001430287143669800:
                    # ACC_LIST
                    acc_list.append("• ` ba `\n<:reply:1094561143911100447> *Accepts <@&961964769772961822> members (w/ <@&962169029601144862> role) role to **Lapagan Category** only.*")
                    acc_list.append("• ` bb `\n<:reply:1094561143911100447> *Accepts <@&961964769772961822> members (w/ <@&962169029601144862> role) role to **Lipunan Category** only.*")
                    acc_list.append("• ` bc `\n<:reply:1094561143911100447> *Accepts <@&961964769772961822> members (w/ <@&962169029601144862> role) role to **Both Categories**.*")
                    acc_list.append("• ` ma `\n<:reply:1094561143911100447> *Accepts <@&961964769772961822> members (w/ <@&962169020151394394> role) role to **Lapagan Category** only.*")
                    acc_list.append("• ` mb `\n<:reply:1094561143911100447> *Accepts <@&961964769772961822> members (w/ <@&962169020151394394> role) role to **Lipunan Category** only.*")
                    acc_list.append("• ` mc `\n<:reply:1094561143911100447> *Accepts <@&961964769772961822> members (w/ <@&962169020151394394> role) role to **Both Categories** only.*")
                    acc_list.sort()
                    inv_list.extend(acc_list)
                    commands.append("• Tanod Commands")

            if self.ctx.author.guild_permissions.administrator:
                # ADMIN_LIST
                admin_list.append("• ` set-level `\n<:reply:1094561143911100447> *Manually sets a user's level according to choice of category. Use `.help set-level` to view more usage.*")
                admin_list.append("• ` set-xp `\n<:reply:1094561143911100447> *Manually sets a user's xp according to choice of category. Use `.help set-xp` to view more usage.*")
                admin_list.append("• ` set-lp `\n<:reply:1094561143911100447> *Manually sets a user's **Ligtas Points (LP)**.*")
                admin_list.append("• ` clear-lp `\n<:reply:1094561143911100447> *Clears a user's **Ligtas Points (LP)**.  Use `.help clear-lp` to view more usage.*")
                admin_list.append("• ` approve `\n<:reply:1094561143911100447> *Approves a starboard entry to be posted in <#1048837480700465202>.*")
                admin_list.append("• ` reject `\n<:reply:1094561143911100447> *Rejects a starboard entry.*")
                admin_list.sort()
                inv_list.extend(admin_list)
                commands.append("• Admin Commands")

            # UTILITY_LIST
            utility_list.append("• ` avatar `\n<:reply:1094561143911100447> *Shows your avatar or member's avatar.*")
            utility_list.append("• ` bots `\n<:reply:1094561143911100447> *View bot lists, or bot information in the server.*")
            utility_list.append("• ` channels `\n<:reply:1094561143911100447> *View channel information. Use `.help channels` to view more usage.*")
            utility_list.append("• ` events `\n<:reply:1094561143911100447> *View current, and future events in the server.*")
            utility_list.append("• ` help `\n<:reply:1094561143911100447> ***You are here***")
            utility_list.append("• ` minecraft `\n<:reply:1094561143911100447> *View minecraft-related stuffs here. Use `.help minecraft` to view more usage.*")
            utility_list.append("• ` ping `\n<:reply:1094561143911100447> *Pong!*")
            utility_list.append("• ` roles `\n<:reply:1094561143911100447> *View role information. Use `.help roles` to view more usage.*")
            utility_list.append("• ` serverinfo `\n<:reply:1094561143911100447> *View server information.*")
            utility_list.append("• ` botstats `\n<:reply:1094561143911100447> *View bot-related stuffs here.*")
            utility_list.append("• ` userinfo `\n<:reply:1094561143911100447> *Shows your user information or member's user information.*")
            utility_list.append("• ` starboard `\n<:reply:1094561143911100447> *Shows a starboard entry based on the input key. Key must be valid.*")
            utility_list.append("• ` partnership `\n<:reply:1094561143911100447> *Views list of partnered servers. Use `.help partnership` to view more usage.*")
            utility_list.sort()
            commands.append("• Utility Commands")

            # LEVELING_LIST
            leveling_list.append("~~• ` rank `\n<:reply:1094561143911100447> *Shows your rank or member's rank.*~~")
            leveling_list.append("~~• ` shop `\n<:reply:1094561143911100447> *Enter the shop to purchase items and emblems.*~~")
            leveling_list.append("~~• ` ranksettings `\n<:reply:1094561143911100447> *Customize your rank card here.*~~")
            leveling_list.append("• ` leaderboards `\n<:reply:1094561143911100447> *Shows rankings according to given category. Use `.help leaderboards` to view more usage.*")
            leveling_list.append("~~• ` vote `\n<:reply:1094561143911100447> *Vote KBL in exchange for vote-exclusive goodies!*~~")
            leveling_list.append("~~• ` stats `\n<:reply:1094561143911100447> *Shows your current stats or member's current stats.*~~")
            leveling_list.append("• ` points `\n<:reply:1094561143911100447> *Shows your current **Solid Points (SP)** and **Ligtas Points (LP)**.*")
            leveling_list.sort()
            commands.append("• Leveling Commands")

            inv_list.extend(utility_list)
            inv_list.extend(leveling_list)
            categories = "\n".join([item for item in commands])

            embed = Embed(description=f"Use `.help` for general help and provide with `query` to give examples on command usage.", color=0x2f3136).set_author(name="KBL BOT - HELP COMMAND", url="https://docs.porcopion.xyz/", icon_url=self.ctx.author.avatar)
            embed.add_field(name="Command Categories:", value=f"{categories}")
            embed.add_field(name="Links:", value="• [top.gg](https://top.gg/servers/961502956195303494)\n• [discord.io](https://discord.io/kblipunan)\n• [<:fb:992030569716252822> Facebook](https://www.facebook.com/kblipunan)\n• [<:yt:992030607720845373> Youtube](https://www.youtube.com/kblipunan)").set_footer(text=f"Command executed by: {self.ctx.author}", icon_url=self.ctx.author.avatar).set_thumbnail(url=self.ctx.guild.icon)

            commands0 = "\n\n".join([item for item in inv_list[:7]])
            commands1 = "\n\n".join([item for item in inv_list[7:14]])
            embed0 = Embed(description=commands0, color=0x2f3136).set_footer(text="To view usage of commands, use .help <command>", icon_url=self.ctx.author.avatar)
            embed1 = Embed(description=commands1, color=0x2f3136).set_footer(text="To view usage of commands, use .help <command>", icon_url=self.ctx.author.avatar)
            self.embeds = [embed, embed0, embed1]
            if len(inv_list) >= 14:
                commands2 = "\n\n".join([item for item in inv_list[14:21]])
                embed2 = Embed(description=commands2, color=0x2f3136).set_footer(text="To view usage of commands, use .help <command>", icon_url=self.ctx.author.avatar)
                self.embeds.append(embed2)
                if len(inv_list) >= 21:
                    commands3 = "\n\n".join([item for item in inv_list[21:28]])
                    embed3 = Embed(description=commands3, color=0x2f3136).set_footer(text="To view usage of commands, use .help <command>", icon_url=self.ctx.author.avatar)
                    new_list.append(embed3)
                    if len(inv_list) >= 28:
                        commands4 = "\n\n".join([item for item in inv_list[28:35]])
                        embed4 = Embed(description=commands4, color=0x2f3136).set_footer(text="To view usage of commands, use .help <command>", icon_url=self.ctx.author.avatar)
                        new_list.append(embed4)
        else:
            if "Tanod" in select.values:
                self.count = 0
                acc_list = []
                acc_list.append("• ` ba `\n<:reply:1094561143911100447> *Accepts <@&961964769772961822> members (w/ <@&962169029601144862> role) role to **Lapagan Category** only.*")
                acc_list.append("• ` bb `\n<:reply:1094561143911100447> *Accepts <@&961964769772961822> members (w/ <@&962169029601144862> role) role to **Lipunan Category** only.*")
                acc_list.append("• ` bc `\n<:reply:1094561143911100447> *Accepts <@&961964769772961822> members (w/ <@&962169029601144862> role) role to **Both Categories**.*")
                acc_list.append("• ` ma `\n<:reply:1094561143911100447> *Accepts <@&961964769772961822> members (w/ <@&962169020151394394> role) role to **Lapagan Category** only.*")
                acc_list.append("• ` mb `\n<:reply:1094561143911100447> *Accepts <@&961964769772961822> members (w/ <@&962169020151394394> role) role to **Lipunan Category** only.*")
                acc_list.append("• ` mc `\n<:reply:1094561143911100447> *Accepts <@&961964769772961822> members (w/ <@&962169020151394394> role) role to **Both Categories** only.*")
                acc_list.sort()
                embed = Embed(description=f"Use `.help` for general help and provide with `query` to give examples on command usage.", color=0x2f3136).set_author(name="KBL BOT - HELP COMMAND", url="https://docs.porcopion.xyz/", icon_url=self.ctx.author.avatar)
                embed.add_field(name="Command Categories:", value=f"• Tanod Commands")
                embed.add_field(name="Links:", value="• [top.gg](https://top.gg/servers/961502956195303494)\n• [discord.io](https://discord.io/kblipunan)\n• [<:fb:992030569716252822> Facebook](https://www.facebook.com/kblipunan)\n• [<:yt:992030607720845373> Youtube](https://www.youtube.com/kblipunan)").set_footer(text=f"Command executed by: {self.ctx.author}", icon_url=self.ctx.author.avatar).set_thumbnail(url=self.ctx.guild.icon)
                commands0 = "\n\n".join([item for item in acc_list[:7]])
                embed0 = Embed(description=commands0, color=0x2f3136).set_footer(text="To view usage of commands, use .help <command>", icon_url=self.ctx.author.avatar)
                self.embeds = [embed, embed0]
            if "Admin" in select.values:
                self.count = 0
                admin_list = []
                admin_list.append("• ` set-level `\n<:reply:1094561143911100447> *Manually sets a user's level according to choice of category. Use `.help set-level` to view more usage.*")
                admin_list.append("• ` set-xp `\n<:reply:1094561143911100447> *Manually sets a user's xp according to choice of category. Use `.help set-xp` to view more usage.*")
                admin_list.append("• ` set-lp `\n<:reply:1094561143911100447> *Manually sets a user's **Ligtas Points (LP)**.*")
                admin_list.append("• ` clear-lp `\n<:reply:1094561143911100447> *Clears a user's **Ligtas Points (LP)**.  Use `.help clear-lp` to view more usage.*")
                admin_list.append("• ` approve `\n<:reply:1094561143911100447> *Approves a starboard entry to be posted in <#1048837480700465202>.*")
                admin_list.append("• ` reject `\n<:reply:1094561143911100447> *Rejects a starboard entry.*")
                admin_list.sort()
                embed = Embed(description=f"Use `.help` for general help and provide with `query` to give examples on command usage.", color=0x2f3136).set_author(name="KBL BOT - HELP COMMAND", url="https://docs.porcopion.xyz/", icon_url=self.ctx.author.avatar)
                embed.add_field(name="Command Categories:", value=f"• Admin Commands")
                embed.add_field(name="Links:", value="• [top.gg](https://top.gg/servers/961502956195303494)\n• [discord.io](https://discord.io/kblipunan)\n• [<:fb:992030569716252822> Facebook](https://www.facebook.com/kblipunan)\n• [<:yt:992030607720845373> Youtube](https://www.youtube.com/kblipunan)").set_footer(text=f"Command executed by: {self.ctx.author}", icon_url=self.ctx.author.avatar).set_thumbnail(url=self.ctx.guild.icon)
                commands0 = "\n\n".join([item for item in admin_list[:7]])
                embed0 = Embed(description=commands0, color=0x2f3136).set_footer(text="To view usage of commands, use .help <command>", icon_url=self.ctx.author.avatar)
                self.embeds = [embed, embed0]
            if "Utility" in select.values:
                self.count = 0
                utility_list = []
                utility_list.append("• ` avatar `\n<:reply:1094561143911100447> *Shows your avatar or member's avatar.*")
                utility_list.append("• ` bots `\n<:reply:1094561143911100447> *View bot lists, or bot information in the server.*")
                utility_list.append("• ` channels `\n<:reply:1094561143911100447> *View channel information. Use `.help channels` to view more usage.*")
                utility_list.append("• ` events `\n<:reply:1094561143911100447> *View current, and future events in the server.*")
                utility_list.append("• ` help `\n<:reply:1094561143911100447> ***You are here***")
                utility_list.append("• ` minecraft `\n<:reply:1094561143911100447> *View minecraft-related stuffs here. Use `.help minecraft` to view more usage.*")
                utility_list.append("• ` ping `\n<:reply:1094561143911100447> *Pong!*")
                utility_list.append("• ` roles `\n<:reply:1094561143911100447> *View role information. Use `.help roles` to view more usage.*")
                utility_list.append("• ` serverinfo `\n<:reply:1094561143911100447> *View server information.*")
                utility_list.append("• ` botstats `\n<:reply:1094561143911100447> *View bot-related stuffs here.*")
                utility_list.append("• ` userinfo `\n<:reply:1094561143911100447> *Shows your user information or member's user information.*")
                utility_list.append("• ` starboard `\n<:reply:1094561143911100447> *Shows a starboard entry based on the input key. Key must be valid.*")
                utility_list.append("• ` partnership `\n<:reply:1094561143911100447> *Views list of partnered servers. Use `.help partnership` to view more usage.*")
                utility_list.sort()
                embed = Embed(description=f"Use `.help` for general help and provide with `query` to give examples on command usage.", color=0x2f3136).set_author(name="KBL BOT - HELP COMMAND", url="https://docs.porcopion.xyz/", icon_url=self.ctx.author.avatar)
                embed.add_field(name="Command Categories:", value=f"• Utility Commands")
                embed.add_field(name="Links:", value="• [top.gg](https://top.gg/servers/961502956195303494)\n• [discord.io](https://discord.io/kblipunan)\n• [<:fb:992030569716252822> Facebook](https://www.facebook.com/kblipunan)\n• [<:yt:992030607720845373> Youtube](https://www.youtube.com/kblipunan)").set_footer(text=f"Command executed by: {self.ctx.author}", icon_url=self.ctx.author.avatar).set_thumbnail(url=self.ctx.guild.icon)
                commands0 = "\n\n".join([item for item in utility_list[:7]])
                commands1 = "\n\n".join([item for item in utility_list[7:14]])
                embed0 = Embed(description=commands0, color=0x2f3136).set_footer(text="To view usage of commands, use .help <command>", icon_url=self.ctx.author.avatar)
                embed1 = Embed(description=commands1, color=0x2f3136).set_footer(text="To view usage of commands, use .help <command>", icon_url=self.ctx.author.avatar)
                self.embeds = [embed, embed0, embed1]
            if "Leveling" in select.values:
                self.count = 0
                leveling_list = []
                leveling_list.append("~~• ` rank `\n<:reply:1094561143911100447> *Shows your rank or member's rank.*~~")
                leveling_list.append("~~• ` shop `\n<:reply:1094561143911100447> *Enter the shop to purchase items and emblems.*~~")
                leveling_list.append("~~• ` ranksettings `\n<:reply:1094561143911100447> *Customize your rank card here.*~~")
                leveling_list.append("• ` leaderboards `\n<:reply:1094561143911100447> *Shows rankings according to given category. Use `.help leaderboards` to view more usage.*")
                leveling_list.append("~~• ` vote `\n<:reply:1094561143911100447> *Vote KBL in exchange for vote-exclusive goodies!*~~")
                leveling_list.append("~~• ` stats `\n<:reply:1094561143911100447> *Shows your current stats or member's current stats.*~~")
                leveling_list.append("• ` points `\n<:reply:1094561143911100447> *Shows your current **Solid Points (SP)** and **Ligtas Points (LP)**.*")
                leveling_list.sort()
                embed = Embed(description=f"Use `.help` for general help and provide with `query` to give examples on command usage.", color=0x2f3136).set_author(name="KBL BOT - HELP COMMAND", url="https://docs.porcopion.xyz/", icon_url=self.ctx.author.avatar)
                embed.add_field(name="Command Categories:", value=f"• Leveling Commands")
                embed.add_field(name="Links:", value="• [top.gg](https://top.gg/servers/961502956195303494)\n• [discord.io](https://discord.io/kblipunan)\n• [<:fb:992030569716252822> Facebook](https://www.facebook.com/kblipunan)\n• [<:yt:992030607720845373> Youtube](https://www.youtube.com/kblipunan)").set_footer(text=f"Command executed by: {self.ctx.author}", icon_url=self.ctx.author.avatar).set_thumbnail(url=self.ctx.guild.icon)
                commands0 = "\n\n".join([item for item in leveling_list[:7]])
                embed0 = Embed(description=commands0, color=0x2f3136).set_footer(text="To view usage of commands, use .help <command>", icon_url=self.ctx.author.avatar)
                self.embeds = [embed, embed0]
        self.button_1.disabled = True
        self.button_2.disabled = True
        self.button_1.style = ButtonStyle.red
        self.button_2.style = ButtonStyle.red
        if len(self.embeds) < 5:
            self.button_5.disabled = True
            self.button_5.style = ButtonStyle.red
        await interaction.response.edit_message(embed=self.embeds[0], view=self)

    @button(style=ButtonStyle.green, label="≪")
    async def button_1(self, button: Button, interaction: Interaction):
        self.count -= 5
        if self.count > len(self.embeds) - 6: # ≫
            self.button_5.disabled = True
            self.button_5.style = ButtonStyle.red
        else:
            self.button_5.disabled = False
            self.button_5.style = ButtonStyle.green
        if self.count == len(self.embeds) - 1: # >
            self.button_4.disabled = True
            self.button_4.style = ButtonStyle.red
        else:
            self.button_4.disabled = False
            self.button_4.style = ButtonStyle.green
        if self.count == 0: # <
            self.button_2.disabled = True
            self.button_2.style = ButtonStyle.red
        else:
            self.button_2.disabled = False
            self.button_2.style = ButtonStyle.green
        if self.count < 5: # ≪
            self.button_1.disabled = True
            self.button_1.style = ButtonStyle.red
        else:
            self.button_1.disabled = False
            self.button_1.style = ButtonStyle.green
        await interaction.response.edit_message(embed=self.embeds[self.count], view=self)

    @button(style=ButtonStyle.green, label="<")
    async def button_2(self, button: Button, interaction: Interaction):
        self.count -= 1
        if self.count > len(self.embeds) - 6: # ≫
            self.button_5.disabled = True
            self.button_5.style = ButtonStyle.red
        else:
            self.button_5.disabled = False
            self.button_5.style = ButtonStyle.green
        if self.count == len(self.embeds) - 1: # >
            self.button_4.disabled = True
            self.button_4.style = ButtonStyle.red
        else:
            self.button_4.disabled = False
            self.button_4.style = ButtonStyle.green
        if self.count == 0: # <
            self.button_2.disabled = True
            self.button_2.style = ButtonStyle.red
        else:
            self.button_2.disabled = False
            self.button_2.style = ButtonStyle.green
        if self.count < 5: # ≪
            self.button_1.disabled = True
            self.button_1.disabled = ButtonStyle.red
        else:
            self.button_1.disabled = False
            self.button_1.style = ButtonStyle.green
        await interaction.response.edit_message(embed=self.embeds[self.count], view=self)

    @button(style=ButtonStyle.red, label="❌")
    async def button_3(self, button: Button, interaction: Interaction):
        await interaction.response.edit_message(embed=self.embeds[self.count], view=None)
        self.stop()

    @button(style=ButtonStyle.green, label=">")
    async def button_4(self, button: Button, interaction: Interaction):
        self.count += 1
        if self.count > len(self.embeds) - 6: # ≫
            self.button_5.disabled = True
            self.button_5.style = ButtonStyle.red
        else:
            self.button_5.disabled = False
            self.button_5.style = ButtonStyle.green
        if self.count == len(self.embeds) - 1: # >
            self.button_4.disabled = True
            self.button_4.style = ButtonStyle.red
        else:
            self.button_4.disabled = False
            self.button_4.style = ButtonStyle.green
        if self.count == 0: # <
            self.button_2.disabled = True
            self.button_2.style = ButtonStyle.red
        else:
            self.button_2.disabled = False
            self.button_2.style = ButtonStyle.green
        if self.count < 5: # ≪
            self.button_1.disabled = True
            self.button_1.disabled = ButtonStyle.red
        else:
            self.button_1.disabled = False
            self.button_1.style = ButtonStyle.green
        await interaction.response.edit_message(embed=self.embeds[self.count], view=self)

    @button(style=ButtonStyle.green, label="≫")
    async def button_5(self, button: Button, interaction: Interaction):
        self.count += 5
        if self.count > len(self.embeds) - 6: # ≫
            self.button_5.disabled = True
            self.button_5.style = ButtonStyle.red
        else:
            self.button_5.disabled = False
            self.button_5.style = ButtonStyle.green
        if self.count == len(self.embeds) - 1: # >
            self.button_4.disabled = True
            self.button_4.style = ButtonStyle.red
        else:
            self.button_4.disabled = False
            self.button_4.style = ButtonStyle.green
        if self.count == 0: # <
            self.button_2.disabled = True
            self.button_2.style = ButtonStyle.red
        else:
            self.button_2.disabled = False
            self.button_2.style = ButtonStyle.green
        if self.count < 5: # ≪
            self.button_1.disabled = True
            self.button_1.disabled = ButtonStyle.red
        else:
            self.button_1.disabled = False
            self.button_1.style = ButtonStyle.green
        await interaction.response.edit_message(embed=self.embeds[self.count], view=self)

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.author.id == self.ctx.author.id:
            return True
        await interaction.response.send_message(content="It is not your command.", ephemeral=True)
        return False

class ShopView(View):
    def __init__(self, ctx: ApplicationCommandInteraction):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.embeds = []
        self.category = 0
        self.count = 0

        self.remove_item(self.button_1)
        self.remove_item(self.button_2)
        self.remove_item(self.button_3)
        self.remove_item(self.button_4)
        self.remove_item(self.button_5)

        self.select_1.add_option(label="Rank Themes", description="View background themes for rank cards.", value="1")
        self.select_1.add_option(label="Level Up Themes", description="View background themes for level up cards.", value="2")
        self.select_1.add_option(label="Profile Banners", description="View profile banners.", value="3")
        self.select_1.add_option(label="Text Colors", description="View available text colors.", value="4")
        self.select_1.add_option(label="Outline Colors", description="View available outline colors.", value="5")
        self.select_1.add_option(label="Items", description="View available items for display.", value="6")
        self.select_1.add_option(label="Exit", description="Exit the shop.", value="x", emoji="❌")

    @select(max_values=1)
    async def select_1(self, select: Select, interaction: Interaction):
        self.remove_item(self.button_1)
        self.remove_item(self.button_2)
        self.remove_item(self.button_3)
        self.remove_item(self.button_4)
        self.remove_item(self.button_5)
        self.add_item(self.button_1)
        self.add_item(self.button_2)
        self.add_item(self.button_3)
        self.add_item(self.button_4)
        self.add_item(self.button_5)
        if "x" in select.values:
            await interaction.response.edit_message(view=None)
            self.stop()
        elif "1" in select.values:
            await interaction.response.send_message(content="🖼️ **Rank Themes** will arrive soon!", ephemeral=True)
        elif "2" in select.values:
            await interaction.response.send_message(content="🖼️ **Level Up Themes** will arrive soon!", ephemeral=True)
        elif "3" in select.values:
            self.button_1.disabled = False
            self.button_2.disabled = False
            self.button_3.disabled = False
            self.button_4.disabled = False
            self.button_5.disabled = False
            self.select_1.placeholder = "Text Colors"
            self.category = 3
            self.count = 0
            self.embeds.clear()
            self.button_1.disabled = True
            self.button_2.disabled = True
            self.button_5.disabled = True
            prices = bn_check_ownership(interaction)
            embed0=Embed(title="Profile Border: Red-Gold", description=f"{prices[0]}\nUsage: `.ranksettings`", color=0x2f3136).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1076397294678724658/rank.png?width=840&height=473").set_footer(text="Purchase an item/theme by pressing '✅' button!", icon_url=self.ctx.author.avatar)
            embed1=Embed(title="Profile Border: Green", description=f"{prices[1]}\nUsage: `.ranksettings`", color=0x2f3136).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1076397944355426334/rank.png?width=840&height=473").set_footer(text="Purchase an item/theme by pressing '✅' button!", icon_url=self.ctx.author.avatar)
            self.embeds = [embed0, embed1]
            await interaction.response.edit_message(embed=self.embeds[self.count], view=self)
        elif "4" in select.values:
            self.button_1.disabled = False
            self.button_2.disabled = False
            self.button_3.disabled = False
            self.button_4.disabled = False
            self.button_5.disabled = False
            self.select_1.placeholder = "Text Colors"
            self.category = 4
            self.count = 0
            self.embeds.clear()
            self.button_1.disabled = True
            self.button_2.disabled = True
            self.button_5.disabled = False
            prices = tc_check_ownership(interaction)
            embed0=Embed(title="Text Color: Coral Red", description=f"{prices[0]}\nUsage: `.ranksettings`", color=0x2f3136).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1076056649036472350/rank.png?width=840&height=473").set_footer(text="Purchase an item/theme by pressing '✅' button!", icon_url=self.ctx.author.avatar)
            embed1=Embed(title="Text Color: Lemon Yellow", description=f"{prices[1]}\nUsage: `.ranksettings`", color=0x2f3136).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1076057058614452224/rank.png?width=840&height=473").set_footer(text="Purchase an item/theme by pressing '✅' button!", icon_url=self.ctx.author.avatar)
            embed2=Embed(title="Text Color: Wheat", description=f"{prices[2]}\nUsage: `.ranksettings`", color=0x2f3136).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1076057990714626069/rank.png?width=840&height=473").set_footer(text="Purchase an item/theme by pressing '✅' button!", icon_url=self.ctx.author.avatar)
            embed3=Embed(title="Text Color: Bronze", description=f"{prices[3]}\nUsage: `.ranksettings`", color=0x2f3136).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1076058602164457483/rank.png?width=840&height=473").set_footer(text="Purchase an item/theme by pressing '✅' button!", icon_url=self.ctx.author.avatar)
            embed4=Embed(title="Text Color: Turquiose", description=f"{prices[4]}\nUsage: `.ranksettings`", color=0x2f3136).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1076060099061235732/rank.png?width=840&height=473").set_footer(text="Purchase an item/theme by pressing '✅' button!", icon_url=self.ctx.author.avatar)
            embed5=Embed(title="Text Color: Slate Blue", description=f"{prices[5]}\nUsage: `.ranksettings`", color=0x2f3136).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1076060953025712168/rank.png?width=840&height=473").set_footer(text="Purchase an item/theme by pressing '✅' button!", icon_url=self.ctx.author.avatar)
            embed6=Embed(title="Text Color: Emerald Green", description=f"{prices[6]}\nUsage: `.ranksettings`", color=0x2f3136).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1076318753748430948/rank.png?width=840&height=473").set_footer(text="Purchase an item/theme by pressing '✅' button!", icon_url=self.ctx.author.avatar)
            embed7=Embed(title="Text Color: Amethyst Purple", description=f"{prices[7]}\nUsage: `.ranksettings`", color=0x2f3136).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1076063196688961576/rank.png?width=840&height=473").set_footer(text="Purchase an item/theme by pressing '✅' button!", icon_url=self.ctx.author.avatar)
            embed8=Embed(title="Text Color: Lilac", description=f"{prices[8]}", color=0x2f3136).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1076063473244573798/rank.png?width=840&height=473").set_footer(text="Purchase an item/theme by pressing '✅' button!", icon_url=self.ctx.author.avatar)
            self.embeds = [embed0, embed1, embed2, embed3, embed4, embed5, embed6, embed7, embed8]
            await interaction.response.edit_message(embed=self.embeds[self.count], view=self)
        elif "5" in select.values:
            self.button_1.disabled = False
            self.button_2.disabled = False
            self.button_3.disabled = False
            self.button_4.disabled = False
            self.button_5.disabled = False
            self.select_1.placeholder = "Outline Colors"
            self.category = 5
            self.count = 0
            self.embeds.clear()
            self.button_1.disabled = True
            self.button_2.disabled = True
            self.button_5.disabled = False
            prices = ol_check_ownership(interaction)
            embed0=Embed(title="Outline Color: Meteorite", description=f"{prices[0]}\nUsage: `.ranksettings`", color=0x2f3136).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1078485371563814973/rank.png?width=840&height=473").set_footer(text="Purchase an item/theme by pressing '✅' button!", icon_url=self.ctx.author.avatar)
            embed1=Embed(title="Outline Color: Bdazzled Blue", description=f"{prices[1]}\nUsage: `.ranksettings`", color=0x2f3136).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1078489933016219670/rank.png?width=840&height=473").set_footer(text="Purchase an item/theme by pressing '✅' button!", icon_url=self.ctx.author.avatar)
            embed2=Embed(title="Outline Color: Green Pea", description=f"{prices[2]}\nUsage: `.ranksettings`", color=0x2f3136).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1078490623402844180/rank.png?width=840&height=473").set_footer(text="Purchase an item/theme by pressing '✅' button!", icon_url=self.ctx.author.avatar)
            embed3=Embed(title="Outline Color: Buddha Gold", description=f"{prices[3]}\nUsage: `.ranksettings`", color=0x2f3136).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1078491958655340654/rank.png?width=840&height=473").set_footer(text="Purchase an item/theme by pressing '✅' button!", icon_url=self.ctx.author.avatar)
            embed4=Embed(title="Outline Color: Alloy Orange", description=f"{prices[4]}\nUsage: `.ranksettings`", color=0x2f3136).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1078492622647205960/rank.png?width=840&height=473").set_footer(text="Purchase an item/theme by pressing '✅' button!", icon_url=self.ctx.author.avatar)
            embed5=Embed(title="Outline Color: Thunderbird", description=f"{prices[5]}\nUsage: `.ranksettings`", color=0x2f3136).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1078493322483613726/rank.png?width=840&height=473").set_footer(text="Purchase an item/theme by pressing '✅' button!", icon_url=self.ctx.author.avatar)
            self.embeds = [embed0, embed1, embed2, embed3, embed4, embed5]
            await interaction.response.edit_message(embed=self.embeds[self.count], view=self)
        elif "6" in select.values:
            await interaction.response.send_message(content="🖼️ **Items/Accolades** will arrive soon!", ephemeral=True)

    @button(style=ButtonStyle.blurple, label="≪")
    async def button_1(self, button: Button, interaction: Interaction):
        self.count -= 5
        if self.count > len(self.embeds) - 6: # ≫
            self.button_5.disabled = True
        else:
            self.button_5.disabled = False
        if self.count == len(self.embeds) - 1: # >
            self.button_4.disabled = True
        else:
            self.button_4.disabled = False
        if self.count == 0: # <
            self.button_2.disabled = True
        else:
            self.button_2.disabled = False
        if self.count < 5: # ≪
            self.button_1.disabled = True
        else:
            self.button_1.disabled = False
        await interaction.response.edit_message(embed=self.embeds[self.count], view=self)

    @button(style=ButtonStyle.blurple, label="<")
    async def button_2(self, button: Button, interaction: Interaction):
        self.count -= 1
        if self.count > len(self.embeds) - 6: # ≫
            self.button_5.disabled = True
        else:
            self.button_5.disabled = False
        if self.count == len(self.embeds) - 1: # >
            self.button_4.disabled = True
        else:
            self.button_4.disabled = False
        if self.count == 0: # <
            self.button_2.disabled = True
        else:
            self.button_2.disabled = False
        if self.count < 5: # ≪
            self.button_1.disabled = True
        else:
            self.button_1.disabled = False
        await interaction.response.edit_message(embed=self.embeds[self.count], view=self)

    @button(style=ButtonStyle.green, label="✅")
    async def button_3(self, button: Button, interaction: Interaction):
        money = db.field("SELECT Points FROM main WHERE UserID = ?", interaction.author.id)
        if self.category == 3:
            bn1, bn2 = db.record("SELECT Banner1, Banner2 FROM items WHERE UserID = ?", interaction.author.id)
            if self.count == 0:
                if money < 750:
                    await interaction.response.send_message(content=f"You don't have enough <:money_icon:1075986284461445140> **Money** to purchase this banner! Earn more money by sending messages on available channels.", ephemeral=True)
                elif bn1 == 1:
                    await interaction.response.send_message(content=f"You already have 🖼️ **Red-Gold Banner**! You can purchase only once per banner! To use this color, do `.ranksettings`. To change color of your banner, use `.morph`.", ephemeral=True)
                else:
                    db.execute("UPDATE main SET Points = Points - 750 WHERE UserID = ?", interaction.author.id)
                    db.execute("UPDATE items SET Banner1 = 1 WHERE UserID = ?", interaction.author.id)
                    embed=Embed(title="Successfully Bought: Red-Gold Banner", description="Price: **Owned**\nUsage: `.ranksettings`", color=Color.green()).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1076397294678724658/rank.png?width=840&height=473").set_footer(text="You bought Red-Gold Banner! Use your new text color via .ranksettings!", icon_url=self.ctx.author.avatar)
                    await interaction.response.edit_message(embed=embed, view=self)
            elif self.count == 1:
                if money < 750:
                    await interaction.response.send_message(content=f"You don't have enough <:money_icon:1075986284461445140> **Money** to purchase this banner! Earn more money by sending messages on available channels.", ephemeral=True)
                elif bn2 == 1:
                    await interaction.response.send_message(content=f"You already have 🖼️ **Green Banner**! You can purchase only once per banner! To use this color, do `.ranksettings`. To change color of your banner, use `.morph`.", ephemeral=True)
                else:
                    db.execute("UPDATE main SET Points = Points - 750 WHERE UserID = ?", interaction.author.id)
                    db.execute("UPDATE items SET Banner2 = 1 WHERE UserID = ?", interaction.author.id)
                    embed=Embed(title="Successfully Bought: Green Banner", description="Price: **Owned**\nUsage: `.ranksettings`", color=Color.green()).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1076397944355426334/rank.png?width=840&height=473").set_footer(text="You bought Green Banner! Use your new text color via .ranksettings!", icon_url=self.ctx.author.avatar)
                    await interaction.response.edit_message(embed=embed, view=self)
        if self.category == 4:
            tc1, tc2, tc3, tc4, tc5, tc6, tc7, tc8, tc9 = db.record("SELECT TextColor1, TextColor2, TextColor3, TextColor4, TextColor5, TextColor6, TextColor7, TextColor8, TextColor9 FROM colors WHERE UserID = ?", interaction.author.id)
            if self.count == 0:
                if money < 500:
                    await interaction.response.send_message(content=f"You don't have enough <:money_icon:1075986284461445140> **Money** to purchase this color! Earn more money by sending messages on available channels.", ephemeral=True)
                elif tc1 == 1:
                    await interaction.response.send_message(content=f"You already have 🖼️ **Coral Red** text color! You can purchase only once per text color! To use this color, do `.ranksettings`.", ephemeral=True)
                else:
                    db.execute("UPDATE main SET Points = Points - 500 WHERE UserID = ?", interaction.author.id)
                    db.execute("UPDATE colors SET TextColor1 = 1 WHERE UserID = ?", interaction.author.id)
                    embed=Embed(title="Successfully Bought: Coral Red", description="Price: **Owned**\nUsage: `.ranksettings`", color=Color.green()).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1076056649036472350/rank.png?width=840&height=473").set_footer(text="You bought Coral Red! Use your new text color via .ranksettings!", icon_url=self.ctx.author.avatar)
                    await interaction.response.edit_message(embed=embed, view=self)
            elif self.count == 1:
                if money < 500:
                    await interaction.response.send_message(content=f"You don't have enough <:money_icon:1075986284461445140> **Money** to purchase this color! Earn more money by sending messages on available channels.", ephemeral=True)
                elif tc2 == 1:
                    await interaction.response.send_message(content=f"You already have 🖼️ **Lemon Yellow** text color! You can purchase only once per text color! To use this color, do `.ranksettings`.", ephemeral=True)
                else:
                    db.execute("UPDATE main SET Points = Points - 500 WHERE UserID = ?", interaction.author.id)
                    db.execute("UPDATE colors SET TextColor2 = 1 WHERE UserID = ?", interaction.author.id)
                    embed=Embed(title="Successfully Bought: Lemon Yellow", description="Price: **Owned**\nUsage: `.ranksettings`", color=Color.green()).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1076057058614452224/rank.png?width=840&height=473").set_footer(text="You bought Lemon Yellow! Use your new text color via .ranksettings!", icon_url=self.ctx.author.avatar)
                    await interaction.response.edit_message(embed=embed, view=self)
            elif self.count == 2:
                if money < 500:
                    await interaction.response.send_message(content=f"You don't have enough <:money_icon:1075986284461445140> **Money** to purchase this color! Earn more money by sending messages on available channels.", ephemeral=True)
                elif tc3 == 1:
                    await interaction.response.send_message(content=f"You already have 🖼️ **Wheat** text color! You can purchase only once per text color! To use this color, do `.ranksettings`.", ephemeral=True)
                else:
                    db.execute("UPDATE main SET Points = Points - 500 WHERE UserID = ?", interaction.author.id)
                    db.execute("UPDATE colors SET TextColor3 = 1 WHERE UserID = ?", interaction.author.id)
                    embed=Embed(title="Successfully Bought: Wheat", description="Price: **Owned**\nUsage: `.ranksettings`", color=Color.green()).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1076057990714626069/rank.png?width=840&height=473").set_footer(text="You bought Wheat! Use your new text color via .ranksettings!", icon_url=self.ctx.author.avatar)
                    await interaction.response.edit_message(embed=embed, view=self)
            elif self.count == 3:
                if money < 500:
                    await interaction.response.send_message(content=f"You don't have enough <:money_icon:1075986284461445140> **Money** to purchase this color! Earn more money by sending messages on available channels.", ephemeral=True)
                elif tc4 == 1:
                    await interaction.response.send_message(content=f"You already have 🖼️ **Bronze** text color! You can purchase only once per text color! To use this color, do `.ranksettings`.", ephemeral=True)
                else:
                    db.execute("UPDATE main SET Points = Points - 500 WHERE UserID = ?", interaction.author.id)
                    db.execute("UPDATE colors SET TextColor4 = 1 WHERE UserID = ?", interaction.author.id)
                    embed=Embed(title="Successfully Bought: Bronze", description="Price: **Owned**\nUsage: `.ranksettings`", color=Color.green()).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1076058602164457483/rank.png").set_footer(text="You bought Bronze! Use your new text color via .ranksettings!", icon_url=self.ctx.author.avatar)
                    await interaction.response.edit_message(embed=embed, view=self)
            elif self.count == 4:
                if money < 500:
                    await interaction.response.send_message(content=f"You don't have enough <:money_icon:1075986284461445140> **Money** to purchase this theme! Earn more money by sending messages on available channels.", ephemeral=True)
                elif tc5 == 1:
                    await interaction.response.send_message(content=f"You already have 🖼️ **Turquiose** text color! You can purchase only once per text color! To use this color, do `.ranksettings`.", ephemeral=True)
                else:
                    db.execute("UPDATE main SET Points = Points - 500 WHERE UserID = ?", interaction.author.id)
                    db.execute("UPDATE colors SET TextColor5 = 1 WHERE UserID = ?", interaction.author.id)
                    embed=Embed(title="Successfully Bought: Turquiose", description="Price: **Owned**\nUsage: `.ranksettings`", color=Color.green()).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1076060099061235732/rank.png").set_footer(text="You bought Turquiose! Use your new text color via .ranksettings!", icon_url=self.ctx.author.avatar)
                    await interaction.response.edit_message(embed=embed, view=self)
            elif self.count == 5:
                if money < 500:
                    await interaction.response.send_message(content=f"You don't have enough <:money_icon:1075986284461445140> **Money** to purchase this theme! Earn more money by sending messages on available channels.", ephemeral=True)
                elif tc6 == 1:
                    await interaction.response.send_message(content=f"You already have 🖼️ **Slate Blue** text color! You can purchase only once per text color! To use this color, do `.ranksettings`.", ephemeral=True)
                else:
                    db.execute("UPDATE main SET Points = Points - 500 WHERE UserID = ?", interaction.author.id)
                    db.execute("UPDATE colors SET TextColor6 = 1 WHERE UserID = ?", interaction.author.id)
                    embed=Embed(title="Successfully Bought: Slate Blue", description="Price: **Owned**\nUsage: `.ranksettings`", color=Color.green()).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1076060953025712168/rank.png").set_footer(text="You bought Slate Blue! Use your new text color via .ranksettings!", icon_url=self.ctx.author.avatar)
                    await interaction.response.edit_message(embed=embed, view=self)
            elif self.count == 6:
                if money < 500:
                    await interaction.response.send_message(content=f"You don't have enough <:money_icon:1075986284461445140> **Money** to purchase this theme! Earn more money by sending messages on available channels.", ephemeral=True)
                elif tc7 == 1:
                    await interaction.response.send_message(content=f"You already have 🖼️ **Emerald Green** text color! You can purchase only once per text color! To use this color, do `.ranksettings`.", ephemeral=True)
                else:
                    db.execute("UPDATE main SET Points = Points - 500 WHERE UserID = ?", interaction.author.id)
                    db.execute("UPDATE colors SET TextColor7 = 1 WHERE UserID = ?", interaction.author.id)
                    embed=Embed(title="Successfully Bought: Emerald Green", description="Price: **Owned**\nUsage: `.ranksettings`", color=Color.green()).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1076318753748430948/rank.png").set_footer(text="You bought Emerald Green! Use your new text color via .ranksettings!", icon_url=self.ctx.author.avatar)
                    await interaction.response.edit_message(embed=embed, view=self)
            elif self.count == 7:
                if money < 500:
                    await interaction.response.send_message(content=f"You don't have enough <:money_icon:1075986284461445140> **Money** to purchase this theme! Earn more money by sending messages on available channels.", ephemeral=True)
                elif tc8 == 1:
                    await interaction.response.send_message(content=f"You already have 🖼️ **Amethyst Purple** text color! You can purchase only once per text color! To use this color, do `.ranksettings`.", ephemeral=True)
                else:
                    db.execute("UPDATE main SET Points = Points - 500 WHERE UserID = ?", interaction.author.id)
                    db.execute("UPDATE colors SET TextColor8 = 1 WHERE UserID = ?", interaction.author.id)
                    embed=Embed(title="Successfully Bought: Amethyst Purple", description="Price: **Owned**\nUsage: `.ranksettings`", color=Color.green()).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1076063196688961576/rank.png").set_footer(text="You bought Amethyst Purple! Use your new text color via .ranksettings!", icon_url=self.ctx.author.avatar)
                    await interaction.response.edit_message(embed=embed, view=self)
            elif self.count == 8:
                if money < 500:
                    await interaction.response.send_message(content=f"You don't have enough <:money_icon:1075986284461445140> **Money** to purchase this theme! Earn more money by sending messages on available channels.", ephemeral=True)
                elif tc8 == 1:
                    await interaction.response.send_message(content=f"You already have 🖼️ **Lilac** text color! You can purchase only once per text color! To use this color, do `.ranksettings`.", ephemeral=True)
                else:
                    db.execute("UPDATE main SET Points = Points - 500 WHERE UserID = ?", interaction.author.id)
                    db.execute("UPDATE colors SET TextColor9 = 1 WHERE UserID = ?", interaction.author.id)
                    embed=Embed(title="Successfully Bought: Lilac", description="Price: **Owned**\nUsage: `.ranksettings`", color=Color.green()).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1076063473244573798/rank.png").set_footer(text="You bought Lilac! Use your new text color via .ranksettings!", icon_url=self.ctx.author.avatar)
                    await interaction.response.edit_message(embed=embed, view=self)
        if self.category == 5:
            ol1, ol2, ol3, ol4, ol5, ol6 = db.record("SELECT OutlineColor1, OutlineColor2, OutlineColor3, OutlineColor4, OutlineColor5, OutlineColor6 FROM colors WHERE UserID = ?", interaction.author.id)
            if self.count == 0:
                if money < 500:
                    await interaction.response.send_message(content=f"You don't have enough <:money_icon:1075986284461445140> **Money** to purchase this color! Earn more money by sending messages on available channels.", ephemeral=True)
                elif ol1 == 1:
                    await interaction.response.send_message(content=f"You already have 🖼️ **Meteorite** outline color! You can purchase only once per outline color! To use this color, do `.ranksettings`.", ephemeral=True)
                else:
                    db.execute("UPDATE main SET Points = Points - 500 WHERE UserID = ?", interaction.author.id)
                    db.execute("UPDATE colors SET OutlineColor1 = 1 WHERE UserID = ?", interaction.author.id)
                    embed=Embed(title="Successfully Bought: Meteorite", description="Price: **Owned**\nUsage: `.ranksettings`", color=Color.green()).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1078485371563814973/rank.png?width=840&height=473").set_footer(text="You bought Meteorite! Use your new outline color via .ranksettings!", icon_url=self.ctx.author.avatar)
                    await interaction.response.edit_message(embed=embed, view=self)
            elif self.count == 1:
                if money < 500:
                    await interaction.response.send_message(content=f"You don't have enough <:money_icon:1075986284461445140> **Money** to purchase this color! Earn more money by sending messages on available channels.", ephemeral=True)
                elif ol2 == 1:
                    await interaction.response.send_message(content=f"You already have 🖼️ **Bdazzled Blue** outline color! You can purchase only once per outline color! To use this color, do `.ranksettings`.", ephemeral=True)
                else:
                    db.execute("UPDATE main SET Points = Points - 500 WHERE UserID = ?", interaction.author.id)
                    db.execute("UPDATE colors SET OutlineColor2 = 1 WHERE UserID = ?", interaction.author.id)
                    embed=Embed(title="Successfully Bought: Bdazzled Blue", description="Price: **Owned**\nUsage: `.ranksettings`", color=Color.green()).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1078489933016219670/rank.png?width=840&height=473").set_footer(text="You bought Bdazzled Blue! Use your new outline color via .ranksettings!", icon_url=self.ctx.author.avatar)
                    await interaction.response.edit_message(embed=embed, view=self)
            elif self.count == 2:
                if money < 500:
                    await interaction.response.send_message(content=f"You don't have enough <:money_icon:1075986284461445140> **Money** to purchase this color! Earn more money by sending messages on available channels.", ephemeral=True)
                elif ol3 == 1:
                    await interaction.response.send_message(content=f"You already have 🖼️ **Green Pea** outline color! You can purchase only once per outline color! To use this color, do `.ranksettings`.", ephemeral=True)
                else:
                    db.execute("UPDATE main SET Points = Points - 500 WHERE UserID = ?", interaction.author.id)
                    db.execute("UPDATE colors SET OutlineColor3 = 1 WHERE UserID = ?", interaction.author.id)
                    embed=Embed(title="Successfully Bought: Green Pea", description="Price: **Owned**\nUsage: `.ranksettings`", color=Color.green()).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1078490623402844180/rank.png?width=840&height=473").set_footer(text="You bought Green Pea! Use your new outline color via .ranksettings!", icon_url=self.ctx.author.avatar)
                    await interaction.response.edit_message(embed=embed, view=self)
            elif self.count == 3:
                if money < 500:
                    await interaction.response.send_message(content=f"You don't have enough <:money_icon:1075986284461445140> **Money** to purchase this color! Earn more money by sending messages on available channels.", ephemeral=True)
                elif ol4 == 1:
                    await interaction.response.send_message(content=f"You already have 🖼️ **Buddha Gold** outline color! You can purchase only once per outline color! To use this color, do `.ranksettings`.", ephemeral=True)
                else:
                    db.execute("UPDATE main SET Points = Points - 500 WHERE UserID = ?", interaction.author.id)
                    db.execute("UPDATE colors SET OutlineColor4 = 1 WHERE UserID = ?", interaction.author.id)
                    embed=Embed(title="Successfully Bought: Buddha Gold", description="Price: **Owned**\nUsage: `.ranksettings`", color=Color.green()).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1078491958655340654/rank.png?width=840&height=473").set_footer(text="You bought Buddha Gold! Use your new outline color via .ranksettings!", icon_url=self.ctx.author.avatar)
                    await interaction.response.edit_message(embed=embed, view=self)
            elif self.count == 4:
                if money < 500:
                    await interaction.response.send_message(content=f"You don't have enough <:money_icon:1075986284461445140> **Money** to purchase this theme! Earn more money by sending messages on available channels.", ephemeral=True)
                elif ol5 == 1:
                    await interaction.response.send_message(content=f"You already have 🖼️ **Alloy Orange** outline color! You can purchase only once per outline color! To use this color, do `.ranksettings`.", ephemeral=True)
                else:
                    db.execute("UPDATE main SET Points = Points - 500 WHERE UserID = ?", interaction.author.id)
                    db.execute("UPDATE colors SET OutlineColor5 = 1 WHERE UserID = ?", interaction.author.id)
                    embed=Embed(title="Successfully Bought: Alloy Orange", description="Price: **Owned**\nUsage: `.ranksettings`", color=Color.green()).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1078492622647205960/rank.png?width=840&height=473").set_footer(text="You bought Alloy Orange! Use your new outline color via .ranksettings!", icon_url=self.ctx.author.avatar)
                    await interaction.response.edit_message(embed=embed, view=self)
            elif self.count == 5:
                if money < 500:
                    await interaction.response.send_message(content=f"You don't have enough <:money_icon:1075986284461445140> **Money** to purchase this theme! Earn more money by sending messages on available channels.", ephemeral=True)
                elif ol6 == 1:
                    await interaction.response.send_message(content=f"You already have 🖼️ **Thunderbird** outline color! You can purchase only once per outline color! To use this color, do `.ranksettings`.", ephemeral=True)
                else:
                    db.execute("UPDATE main SET Points = Points - 500 WHERE UserID = ?", interaction.author.id)
                    db.execute("UPDATE colors SET OutlineColor6 = 1 WHERE UserID = ?", interaction.author.id)
                    embed=Embed(title="Successfully Bought: Thunderbird", description="Price: **Owned**\nUsage: `.ranksettings`", color=Color.green()).set_image(url="https://media.discordapp.net/attachments/961530361119121408/1078493322483613726/rank.png?width=840&height=473").set_footer(text="You bought Thunderbird! Use your new outline color via .ranksettings!", icon_url=self.ctx.author.avatar)
                    await interaction.response.edit_message(embed=embed, view=self)

    @button(style=ButtonStyle.blurple, label=">")
    async def button_4(self, button: Button, interaction: Interaction):
        self.count += 1
        if self.count > len(self.embeds) - 6: # ≫
            self.button_5.disabled = True
        else:
            self.button_5.disabled = False
        if self.count == len(self.embeds) - 1: # >
            self.button_4.disabled = True
        else:
            self.button_4.disabled = False
        if self.count == 0: # <
            self.button_2.disabled = True
        else:
            self.button_2.disabled = False
        if self.count < 5: # ≪
            self.button_1.disabled = True
        else:
            self.button_1.disabled = False
        await interaction.response.edit_message(embed=self.embeds[self.count], view=self)

    @button(style=ButtonStyle.blurple, label="≫")
    async def button_5(self, button: Button, interaction: Interaction):
        self.count += 5
        if self.count > len(self.embeds) - 6: # ≫
            self.button_5.disabled = True
        else:
            self.button_5.disabled = False
        if self.count == len(self.embeds) - 1: # >
            self.button_4.disabled = True
        else:
            self.button_4.disabled = False
        if self.count == 0: # <
            self.button_2.disabled = True
        else:
            self.button_2.disabled = False
        if self.count < 5: # ≪
            self.button_1.disabled = True
        else:
            self.button_1.disabled = False
        await interaction.response.edit_message(embed=self.embeds[self.count], view=self)

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.author.id == self.ctx.author.id:
            return True
        await interaction.response.send_message(content="It is not your command.", ephemeral=True)
        return False

class RankSettings(View):
    def __init__(self, ctx: ApplicationCommandInteraction):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.banner = ""
        self.text_color = ""
        self.outline_color = ""

        self.banner_count = 0
        self.text_color_count = 0
        self.outline_color_count = 0

        self.remove_item(self.button_1)
        self.remove_item(self.button_2)
        self.remove_item(self.button_3)

        bn1, bn2 = db.record("SELECT Banner1, Banner2 FROM items WHERE UserID = ?", self.ctx.author.id)
        tc1, tc2, tc3, tc4, tc5, tc6, tc7, tc8, tc9 = db.record("SELECT TextColor1, TextColor2, TextColor3, TextColor4, TextColor5, TextColor6, TextColor7, TextColor8, TextColor9 FROM colors WHERE UserID = ?", self.ctx.author.id)
        ol1, ol2, ol3, ol4, ol5, ol6 = db.record("SELECT OutlineColor1, OutlineColor2, OutlineColor3, OutlineColor4, OutlineColor5, OutlineColor6 FROM colors WHERE UserID = ?", self.ctx.author.id)

        # BANNERS
        self.select_1.add_option(label="Reset Banner", value="reset1")
        if bn1 == 1:
            self.banner_count += 1
            self.select_1.add_option(label="Red-Gold Banner", value="Banner1")
        if bn2 == 1:
            self.banner_count += 1
            self.select_1.add_option(label="Green Banner", value="Banner2")
        if self.banner_count == 0:
            self.select_1.disabled = True
        # TEXT COLORS
        self.select_2.add_option(label="Reset Text Color", value="reset2")
        if tc1 == 1:
            self.text_color_count += 1
            self.select_2.add_option(label="Coral Red", value="TextColor1")
        if tc2 == 1:
            self.text_color_count += 1
            self.select_2.add_option(label="Lemon Yellow", value="TextColor2")
        if tc3 == 1:
            self.text_color_count += 1
            self.select_2.add_option(label="Wheat", value="TextColor3")
        if tc4 == 1:
            self.text_color_count += 1
            self.select_2.add_option(label="Bronze", value="TextColor4")
        if tc5 == 1:
            self.text_color_count += 1
            self.select_2.add_option(label="Turquiose", value="TextColor5")
        if tc6 == 1:
            self.text_color_count += 1
            self.select_2.add_option(label="Slate Blue", value="TextColor6")
        if tc7 == 1:
            self.text_color_count += 1
            self.select_2.add_option(label="Emerald Green", value="TextColor7")
        if self.text_color_count == 0:
            self.select_2.disabled = True
        # OUTLINE COLORS
        self.select_3.add_option(label="Reset Outline Color", value="reset3")
        if ol1 == 1:
            self.outline_color_count += 1
            self.select_3.add_option(label="Meteorite", value="OutlineColor1")
        if ol2 == 1:
            self.outline_color_count += 1
            self.select_3.add_option(label="Bdazzled Blue", value="OutlineColor2")
        if ol3 == 1:
            self.outline_color_count += 1
            self.select_3.add_option(label="Green Pea", value="OutlineColor3")
        if ol4 == 1:
            self.outline_color_count += 1
            self.select_3.add_option(label="Buddha Gold", value="OutlineColor4")
        if ol5 == 1:
            self.outline_color_count += 1
            self.select_3.add_option(label="Alloy Orange", value="OutlineColor5")
        if ol6 == 1:
            self.outline_color_count += 1
            self.select_3.add_option(label="Thunderbird", value="OutlineColor6")
        if self.outline_color_count == 0:
            self.select_3.disabled = True

    @select(max_values=1, placeholder="Pick a banner here")
    async def select_1(self, select: Select, interaction: Interaction):
        self.banner = select.values[0]
        if self.banner == "reset1":
            if self.banner == "" and self.text_color == "" and self.outline_color == "":
                self.remove_item(self.button_1)
                self.remove_item(self.button_2)
                self.remove_item(self.button_3)
            self.banner = ""
        else:
            self.add_item(self.button_1)
            self.add_item(self.button_2)
            self.add_item(self.button_3)
        # --- INITIALIZING IMAGES --- #
        if len(interaction.author.name) > 15:
            username = interaction.author.name.replace(interaction.author.name[15:], "...")
        else:
            username = interaction.author.name
        if len(interaction.author.display_name) > 15:
            nickname = interaction.author.display_name.replace(interaction.author.display_name[15:], "...")
        else:
            nickname = interaction.author.display_name
        image = Editor("./properties/assets/kbl_podcast_bg.png").resize((1920, 1080), crop=True).blur(amount=7).rounded_corners()
        if interaction.author.avatar is None:
            profile, avatar = await load_image_async(str(interaction.author.display_avatar.url)), await load_image_async(str(interaction.author.display_avatar.url))
        else:
            profile, avatar = await load_image_async(str(interaction.author.avatar.url)), await load_image_async(str(interaction.author.display_avatar.url))
        profile_, avatar_ = Editor(profile).resize((342, 342)).circle_image(), Editor(avatar).resize((55, 55)).circle_image()
        profile_banner, text_fill = rank_banner_check(self.banner), rank_text_color_check(self.text_color)
        outline_ol, outline_fill = rank_outline_color_check(self.outline_color)
        stats_icon, message_icon = Editor("./properties/assets/stats_icon.png").resize((80, 56)), Editor("./properties/assets/message_icon.png").resize((64, 54), crop=True)
        money_icon = Editor("./properties/assets/money_icon.png").resize((85, 64))
        status_icon, status = Editor("./properties/assets/online.png").resize((40, 40)), "Online"
        font, font1 = Font.montserrat(variant="bold", size=60), Font.montserrat(variant="bold", size=50)
        font2, font3 = Font.montserrat(variant="bold", size=104), Font.montserrat(variant="bold", size=47)
        font4, font5 = Font.montserrat(variant="bold", size=51), Font.montserrat(variant="bold", size=46)
        # --- PASTING FILES --- #
        image.paste(profile_banner.image, (53, 0))
        image.paste(profile_.image, (120, 90))
        image.paste(avatar_.image, (619, 167))
        image.paste(stats_icon.image, (165, 471))
        image.paste(message_icon.image, (174, 555))
        image.paste(money_icon.image, (1415, 399))
        image.paste(status_icon.image, (619, 403))
        # --- INSERTING SHAPES --- #
        image.ellipse((200, 666), width=167, height=167, outline=outline_ol, stroke_width=15)
        image.ellipse((120, 90), width=342, height=342, outline="#0000ff", stroke_width=10)
        image.rectangle((585, 731), width=293, height=296, outline=outline_ol, stroke_width=13, radius=60)
        image.rectangle((919, 731), width=293, height=296, outline=outline_ol, stroke_width=13, radius=60)
        image.rectangle((1252, 731), width=293, height=296, outline=outline_ol, stroke_width=13, radius=60)
        image.rectangle((1585, 731), width=293, height=296, outline=outline_ol, stroke_width=13, radius=60)
        image.rectangle((609, 554), width=402, height=113, outline=outline_ol, stroke_width=15, radius=90)
        image.text((681, 591), text=f"Daldalero", font=font1, color=text_fill, align="left")
        image.rectangle((909, 554), width=402, height=113, outline=outline_ol, stroke_width=15, radius=90)
        image.text((981, 591), text=f"Payaso", font=font1, color=text_fill, align="left")
        image.rectangle((603, 239), width=1259, height=137, outline=outline_ol, stroke_width=15, fill=outline_fill, radius=90)
        image.bar((603, 239), max_width=588, height=137, percentage=14, fill=outline_ol, radius=90)
        # --- APPLYING TEXT --- #
        image.text_stroke((655, 280), text=f"17 / 100 (Level 1) - Lipunan", font=font, stroke_width=4, stroke_fill="#000000", color=text_fill, align="left")
        image.text((691, 175), text=f"{username}#{interaction.author.discriminator}", font=font1, color=text_fill, align="left")
        image.text((620, 48), text=f"{nickname}", font=font2, color=text_fill, align="left")
        image.text((676, 403), text=f"{status}", font=font3, color=text_fill, align="left")
        image.text((676, 484), text=f"-", font=font3, color=text_fill, align="left")
        image.text((1509, 409), text=f"3.7k (+2)", font=font4, color=text_fill, align="left")
        image.text((281, 488), text=f"#1", font=font5, color=text_fill, align="left")
        image.text((314, 564), text=f"1.3k", font=font5, color=text_fill, align="center")
        card = File(fp=image.image_bytes, filename="rank.png")
        await interaction.response.edit_message(content="> If you are satisfied with your changes, press '✅'!", attachments=[], file=card, view=self)

    @select(max_values=1, placeholder="Pick a text color here")
    async def select_2(self, select: Select, interaction: Interaction):
        self.text_color = select.values[0]
        if self.text_color == "reset2":
            if self.banner == "" and self.text_color == "" and self.outline_color == "":
                self.remove_item(self.button_1)
                self.remove_item(self.button_2)
                self.remove_item(self.button_3)
            self.text_color = ""
        else:
            self.add_item(self.button_1)
            self.add_item(self.button_2)
            self.add_item(self.button_3)
        # --- INITIALIZING IMAGES --- #
        if len(interaction.author.name) > 15:
            username = interaction.author.name.replace(interaction.author.name[15:], "...")
        else:
            username = interaction.author.name
        if len(interaction.author.display_name) > 15:
            nickname = interaction.author.display_name.replace(interaction.author.display_name[15:], "...")
        else:
            nickname = interaction.author.display_name
        image = Editor("./properties/assets/kbl_podcast_bg.png").resize((1920, 1080), crop=True).blur(amount=7).rounded_corners()
        if interaction.author.avatar is None:
            profile, avatar = await load_image_async(str(interaction.author.display_avatar.url)), await load_image_async(str(interaction.author.display_avatar.url))
        else:
            profile, avatar = await load_image_async(str(interaction.author.avatar.url)), await load_image_async(str(interaction.author.display_avatar.url))
        profile_, avatar_ = Editor(profile).resize((342, 342)).circle_image(), Editor(avatar).resize((55, 55)).circle_image()
        profile_banner, text_fill = rank_banner_check(self.banner), rank_text_color_check(self.text_color)
        outline_ol, outline_fill = rank_outline_color_check(self.outline_color)
        stats_icon, message_icon = Editor("./properties/assets/stats_icon.png").resize((80, 56)), Editor("./properties/assets/message_icon.png").resize((64, 54), crop=True)
        money_icon = Editor("./properties/assets/money_icon.png").resize((85, 64))
        status_icon, status = Editor("./properties/assets/online.png").resize((40, 40)), "Online"
        font, font1 = Font.montserrat(variant="bold", size=60), Font.montserrat(variant="bold", size=50)
        font2, font3 = Font.montserrat(variant="bold", size=104), Font.montserrat(variant="bold", size=47)
        font4, font5 = Font.montserrat(variant="bold", size=51), Font.montserrat(variant="bold", size=46)
        # --- PASTING FILES --- #
        image.paste(profile_banner.image, (53, 0))
        image.paste(profile_.image, (120, 90))
        image.paste(avatar_.image, (619, 167))
        image.paste(stats_icon.image, (165, 471))
        image.paste(message_icon.image, (174, 555))
        image.paste(money_icon.image, (1415, 399))
        image.paste(status_icon.image, (619, 403))
        # --- INSERTING SHAPES --- #
        image.ellipse((200, 666), width=167, height=167, outline=outline_ol, stroke_width=15)
        image.ellipse((120, 90), width=342, height=342, outline="#0000ff", stroke_width=10)
        image.rectangle((585, 731), width=293, height=296, outline=outline_ol, stroke_width=13, radius=60)
        image.rectangle((919, 731), width=293, height=296, outline=outline_ol, stroke_width=13, radius=60)
        image.rectangle((1252, 731), width=293, height=296, outline=outline_ol, stroke_width=13, radius=60)
        image.rectangle((1585, 731), width=293, height=296, outline=outline_ol, stroke_width=13, radius=60)
        image.rectangle((609, 554), width=402, height=113, outline=outline_ol, stroke_width=15, radius=90)
        image.text((681, 591), text=f"Daldalero", font=font1, color=text_fill, align="left")
        image.rectangle((909, 554), width=402, height=113, outline=outline_ol, stroke_width=15, radius=90)
        image.text((981, 591), text=f"Payaso", font=font1, color=text_fill, align="left")
        image.rectangle((603, 239), width=1259, height=137, outline=outline_ol, stroke_width=15, fill=outline_fill, radius=90)
        image.bar((603, 239), max_width=588, height=137, percentage=14, fill=outline_ol, radius=90)
        # --- APPLYING TEXT --- #
        image.text_stroke((655, 280), text=f"17 / 100 (Level 1) - Lipunan", font=font, stroke_width=4, stroke_fill="#000000", color=text_fill, align="left")
        image.text((691, 175), text=f"{username}#{interaction.discriminator}", font=font1, color=text_fill, align="left")
        image.text((620, 48), text=f"{nickname}", font=font2, color=text_fill, align="left")
        image.text((676, 403), text=f"{status}", font=font3, color=text_fill, align="left")
        image.text((676, 484), text=f"-", font=font3, color=text_fill, align="left")
        image.text((1509, 409), text=f"3.7k (+2)", font=font4, color=text_fill, align="left")
        image.text((281, 488), text=f"#1", font=font5, color=text_fill, align="left")
        image.text((314, 564), text=f"1.3k", font=font5, color=text_fill, align="center")
        card = File(fp=image.image_bytes, filename="rank.png")
        await interaction.response.edit_message(content="> If you are satisfied with your changes, press '✅'!", attachments=[], file=card, view=self)

    @select(max_values=1, placeholder="Pick an outline color here")
    async def select_3(self, select: Select, interaction: Interaction):
        self.outline_color = select.values[0]
        if self.outline_color == "reset1":
            if self.banner == "" and self.text_color == "" and self.outline_color == "":
                self.remove_item(self.button_1)
                self.remove_item(self.button_2)
                self.remove_item(self.button_3)
            self.outline_color = ""
        else:
            self.add_item(self.button_1)
            self.add_item(self.button_2)
            self.add_item(self.button_3)
        # --- INITIALIZING IMAGES --- #
        if len(interaction.author.name) > 15:
            username = interaction.author.name.replace(interaction.author.name[15:], "...")
        else:
            username = interaction.author.name
        if len(interaction.author.display_name) > 15:
            nickname = interaction.author.display_name.replace(interaction.author.display_name[15:], "...")
        else:
            nickname = interaction.author.display_name
        image = Editor("./properties/assets/kbl_podcast_bg.png").resize((1920, 1080), crop=True).blur(amount=7).rounded_corners()
        if interaction.author.avatar is None:
            profile, avatar = await load_image_async(str(interaction.author.display_avatar.url)), await load_image_async(str(interaction.author.display_avatar.url))
        else:
            profile, avatar = await load_image_async(str(interaction.author.avatar.url)), await load_image_async(str(interaction.author.display_avatar.url))
        profile_, avatar_ = Editor(profile).resize((342, 342)).circle_image(), Editor(avatar).resize((55, 55)).circle_image()
        profile_banner, text_fill = rank_banner_check(self.banner), rank_text_color_check(self.text_color)
        outline_ol, outline_fill = rank_outline_color_check(self.outline_color)
        stats_icon, message_icon = Editor("./properties/assets/stats_icon.png").resize((80, 56)), Editor("./properties/assets/message_icon.png").resize((64, 54), crop=True)
        money_icon = Editor("./properties/assets/money_icon.png").resize((85, 64))
        status_icon, status = Editor("./properties/assets/online.png").resize((40, 40)), "Online"
        font, font1 = Font.montserrat(variant="bold", size=60), Font.montserrat(variant="bold", size=50)
        font2, font3 = Font.montserrat(variant="bold", size=104), Font.montserrat(variant="bold", size=47)
        font4, font5 = Font.montserrat(variant="bold", size=51), Font.montserrat(variant="bold", size=46)
        # --- PASTING FILES --- #
        image.paste(profile_banner.image, (53, 0))
        image.paste(profile_.image, (120, 90))
        image.paste(avatar_.image, (619, 167))
        image.paste(stats_icon.image, (165, 471))
        image.paste(message_icon.image, (174, 555))
        image.paste(money_icon.image, (1415, 399))
        image.paste(status_icon.image, (619, 403))
        # --- INSERTING SHAPES --- #
        image.ellipse((200, 666), width=167, height=167, outline=outline_ol, stroke_width=15)
        image.ellipse((120, 90), width=342, height=342, outline="#0000ff", stroke_width=10)
        image.rectangle((585, 731), width=293, height=296, outline=outline_ol, stroke_width=13, radius=60)
        image.rectangle((919, 731), width=293, height=296, outline=outline_ol, stroke_width=13, radius=60)
        image.rectangle((1252, 731), width=293, height=296, outline=outline_ol, stroke_width=13, radius=60)
        image.rectangle((1585, 731), width=293, height=296, outline=outline_ol, stroke_width=13, radius=60)
        image.rectangle((609, 554), width=402, height=113, outline=outline_ol, stroke_width=15, radius=90)
        image.text((681, 591), text=f"Daldalero", font=font1, color=text_fill, align="left")
        image.rectangle((909, 554), width=402, height=113, outline=outline_ol, stroke_width=15, radius=90)
        image.text((981, 591), text=f"Payaso", font=font1, color=text_fill, align="left")
        image.rectangle((603, 239), width=1259, height=137, outline=outline_ol, stroke_width=15, fill=outline_fill, radius=90)
        image.bar((603, 239), max_width=588, height=137, percentage=14, fill=outline_ol, radius=90)
        # --- APPLYING TEXT --- #
        image.text_stroke((655, 280), text=f"17 / 100 (Level 1) - Lipunan", font=font, stroke_width=4, stroke_fill="#000000", color=text_fill, align="left")
        image.text((691, 175), text=f"{username}#{interaction.discriminator}", font=font1, color=text_fill, align="left")
        image.text((620, 48), text=f"{nickname}", font=font2, color=text_fill, align="left")
        image.text((676, 403), text=f"{status}", font=font3, color=text_fill, align="left")
        image.text((676, 484), text=f"-", font=font3, color=text_fill, align="left")
        image.text((1509, 409), text=f"3.7k (+2)", font=font4, color=text_fill, align="left")
        image.text((281, 488), text=f"#1", font=font5, color=text_fill, align="left")
        image.text((314, 564), text=f"1.3k", font=font5, color=text_fill, align="center")
        card = File(fp=image.image_bytes, filename="rank.png")
        await interaction.response.edit_message(content="> If you are satisfied with your changes, press '✅'!", attachments=[], file=card, view=self)

    @button(style=ButtonStyle.red, emoji="🔁")
    async def button_1(self, button: Button, interaction: Interaction):
        self.banner, self.text_color, self.outline_color = "", "", ""
        # --- INITIALIZING IMAGES --- #
        if len(interaction.author.name) > 15:
            username = interaction.author.name.replace(interaction.author.name[15:], "...")
        else:
            username = interaction.author.name
        if len(interaction.author.display_name) > 15:
            nickname = interaction.author.display_name.replace(interaction.author.display_name[15:], "...")
        else:
            nickname = interaction.author.display_name
        image = Editor("./properties/assets/kbl_podcast_bg.png").resize((1920, 1080), crop=True).blur(amount=7).rounded_corners()
        if interaction.author.avatar is None:
            profile, avatar = await load_image_async(str(interaction.author.display_avatar.url)), await load_image_async(str(interaction.author.display_avatar.url))
        else:
            profile, avatar = await load_image_async(str(interaction.author.avatar.url)), await load_image_async(str(interaction.author.display_avatar.url))
        profile_, avatar_ = Editor(profile).resize((342, 342)).circle_image(), Editor(avatar).resize((55, 55)).circle_image()
        profile_banner, text_fill = rank_banner_check(self.banner), rank_text_color_check(self.text_color)
        outline_ol, outline_fill = rank_outline_color_check(self.outline_color)
        stats_icon, message_icon = Editor("./properties/assets/stats_icon.png").resize((80, 56)), Editor("./properties/assets/message_icon.png").resize((64, 54), crop=True)
        money_icon = Editor("./properties/assets/money_icon.png").resize((85, 64))
        status_icon, status = Editor("./properties/assets/online.png").resize((40, 40)), "Online"
        font, font1 = Font.montserrat(variant="bold", size=60), Font.montserrat(variant="bold", size=50)
        font2, font3 = Font.montserrat(variant="bold", size=104), Font.montserrat(variant="bold", size=47)
        font4, font5 = Font.montserrat(variant="bold", size=51), Font.montserrat(variant="bold", size=46)
        # --- PASTING FILES --- #
        image.paste(profile_banner.image, (53, 0))
        image.paste(profile_.image, (120, 90))
        image.paste(avatar_.image, (619, 167))
        image.paste(stats_icon.image, (165, 471))
        image.paste(message_icon.image, (174, 555))
        image.paste(money_icon.image, (1415, 399))
        image.paste(status_icon.image, (619, 403))
        # --- INSERTING SHAPES --- #
        image.ellipse((200, 666), width=167, height=167, outline=outline_ol, stroke_width=15)
        image.ellipse((120, 90), width=342, height=342, outline="#0000ff", stroke_width=10)
        image.rectangle((585, 731), width=293, height=296, outline=outline_ol, stroke_width=13, radius=60)
        image.rectangle((919, 731), width=293, height=296, outline=outline_ol, stroke_width=13, radius=60)
        image.rectangle((1252, 731), width=293, height=296, outline=outline_ol, stroke_width=13, radius=60)
        image.rectangle((1585, 731), width=293, height=296, outline=outline_ol, stroke_width=13, radius=60)
        image.rectangle((609, 554), width=402, height=113, outline=outline_ol, stroke_width=15, radius=90)
        image.text((681, 591), text=f"Daldalero", font=font1, color=text_fill, align="left")
        image.rectangle((909, 554), width=402, height=113, outline=outline_ol, stroke_width=15, radius=90)
        image.text((981, 591), text=f"Payaso", font=font1, color=text_fill, align="left")
        image.rectangle((603, 239), width=1259, height=137, outline=outline_ol, stroke_width=15, fill=outline_fill, radius=90)
        image.bar((603, 239), max_width=588, height=137, percentage=14, fill=outline_ol, radius=90)
        # --- APPLYING TEXT --- #
        image.text_stroke((655, 280), text=f"17 / 100 (Level 1) - Lipunan", font=font, stroke_width=4, stroke_fill="#000000", color=text_fill, align="left")
        image.text((691, 175), text=f"{username}#{interaction.discriminator}", font=font1, color=text_fill, align="left")
        image.text((620, 48), text=f"{nickname}", font=font2, color=text_fill, align="left")
        image.text((676, 403), text=f"{status}", font=font3, color=text_fill, align="left")
        image.text((676, 484), text=f"-", font=font3, color=text_fill, align="left")
        image.text((1509, 409), text=f"3.7k (+2)", font=font4, color=text_fill, align="left")
        image.text((281, 488), text=f"#1", font=font5, color=text_fill, align="left")
        image.text((314, 564), text=f"1.3k", font=font5, color=text_fill, align="center")
        card = File(fp=image.image_bytes, filename="rank.png")
        await interaction.response.edit_message(content="> Successfully reset all edited changes.", file=card, view=self)

    @button(style=ButtonStyle.green, emoji="✅")
    async def button_2(self, button: Button, interaction: Interaction):
        if self.banner == "":
            bc = 0
        elif self.banner == "Banner1":
            bc = 1
        elif self.banner == "Banner2":
            bc = 2
        text_fill = rank_text_color_check(self.text_color)
        outline_ol, outline_fill = rank_outline_color_check(self.outline_color)
        db.execute("UPDATE main SET BannerChoice = ?, TextBG = ?, PolyBG = ?, OutlineBG = ? WHERE UserID = ?", bc, text_fill, outline_fill, outline_ol, interaction.author.id)
        # --- INITIALIZING IMAGES --- #
        if len(interaction.author.name) > 15:
            username = interaction.author.name.replace(interaction.author.name[15:], "...")
        else:
            username = interaction.author.name
        if len(interaction.author.display_name) > 15:
            nickname = interaction.author.display_name.replace(interaction.author.display_name[15:], "...")
        else:
            nickname = interaction.author.display_name
        image = Editor("./properties/assets/kbl_podcast_bg.png").resize((1920, 1080), crop=True).blur(amount=7).rounded_corners()
        if interaction.author.avatar is None:
            profile, avatar = await load_image_async(str(interaction.author.display_avatar.url)), await load_image_async(str(interaction.author.display_avatar.url))
        else:
            profile, avatar = await load_image_async(str(interaction.author.avatar.url)), await load_image_async(str(interaction.author.display_avatar.url))
        profile_, avatar_ = Editor(profile).resize((342, 342)).circle_image(), Editor(avatar).resize((55, 55)).circle_image()
        profile_banner, text_fill = rank_banner_check(self.banner), rank_text_color_check(self.text_color)
        outline_ol, outline_fill = rank_outline_color_check(self.outline_color)
        stats_icon, message_icon = Editor("./properties/assets/stats_icon.png").resize((80, 56)), Editor("./properties/assets/message_icon.png").resize((64, 54), crop=True)
        money_icon = Editor("./properties/assets/money_icon.png").resize((85, 64))
        status_icon, status = Editor("./properties/assets/online.png").resize((40, 40)), "Online"
        font, font1 = Font.montserrat(variant="bold", size=60), Font.montserrat(variant="bold", size=50)
        font2, font3 = Font.montserrat(variant="bold", size=104), Font.montserrat(variant="bold", size=47)
        font4, font5 = Font.montserrat(variant="bold", size=51), Font.montserrat(variant="bold", size=46)
        # --- PASTING FILES --- #
        image.paste(profile_banner.image, (53, 0))
        image.paste(profile_.image, (120, 90))
        image.paste(avatar_.image, (619, 167))
        image.paste(stats_icon.image, (165, 471))
        image.paste(message_icon.image, (174, 555))
        image.paste(money_icon.image, (1415, 399))
        image.paste(status_icon.image, (619, 403))
        # --- INSERTING SHAPES --- #
        image.ellipse((200, 666), width=167, height=167, outline=outline_ol, stroke_width=15)
        image.ellipse((120, 90), width=342, height=342, outline="#0000ff", stroke_width=10)
        image.rectangle((585, 731), width=293, height=296, outline=outline_ol, stroke_width=13, radius=60)
        image.rectangle((919, 731), width=293, height=296, outline=outline_ol, stroke_width=13, radius=60)
        image.rectangle((1252, 731), width=293, height=296, outline=outline_ol, stroke_width=13, radius=60)
        image.rectangle((1585, 731), width=293, height=296, outline=outline_ol, stroke_width=13, radius=60)
        image.rectangle((609, 554), width=402, height=113, outline=outline_ol, stroke_width=15, radius=90)
        image.text((681, 591), text=f"Daldalero", font=font1, color=text_fill, align="left")
        image.rectangle((909, 554), width=402, height=113, outline=outline_ol, stroke_width=15, radius=90)
        image.text((981, 591), text=f"Payaso", font=font1, color=text_fill, align="left")
        image.rectangle((603, 239), width=1259, height=137, outline=outline_ol, stroke_width=15, fill=outline_fill, radius=90)
        image.bar((603, 239), max_width=588, height=137, percentage=14, fill=outline_ol, radius=90)
        # --- APPLYING TEXT --- #
        image.text_stroke((655, 280), text=f"17 / 100 (Level 1) - Lipunan", font=font, stroke_width=4, stroke_fill="#000000", color=text_fill, align="left")
        image.text((691, 175), text=f"{username}#{interaction.discriminator}", font=font1, color=text_fill, align="left")
        image.text((620, 48), text=f"{nickname}", font=font2, color=text_fill, align="left")
        image.text((676, 403), text=f"{status}", font=font3, color=text_fill, align="left")
        image.text((676, 484), text=f"-", font=font3, color=text_fill, align="left")
        image.text((1509, 409), text=f"3.7k (+2)", font=font4, color=text_fill, align="left")
        image.text((281, 488), text=f"#1", font=font5, color=text_fill, align="left")
        image.text((314, 564), text=f"1.3k", font=font5, color=text_fill, align="center")
        card = File(fp=image.image_bytes, filename="rank.png")
        await interaction.response.edit_message(content="> Saved!", file=card, view=self)

    @button(style=ButtonStyle.red, emoji="❌")
    async def button_3(self, button: Button, interaction: Interaction):
        self.select_1.disabled = True
        self.select_2.disabled = True
        self.select_3.disabled = True
        self.button_1.disabled = True
        self.button_2.disabled = True
        self.button_3.disabled = True
        await interaction.response.edit_message(content="> Cancelled the process.", view=self)
        self.stop()

class ViewPages(View): # GLOBAL USE
    def __init__(self, source: PageSource, *, ctx, check_embeds: bool = True, compact: bool = False, _type: str = None):
        super().__init__(timeout=None)
        self.source: PageSource = source
        self.check_embeds: bool = check_embeds
        self.ctx: ApplicationCommandInteraction = ctx
        self.message: Optional[Message] = None
        self._type: str = None
        self.current_page: int = 0
        self.compact: bool = compact
        self.input_lock = asyncio.Lock()
        self.clear_items()
        self.fill_items()

    def fill_items(self) -> None:

        if self.source.is_paginating():
            max_pages = self.source.get_max_pages()
            use_last_and_first = max_pages is not None and max_pages >= 2
            if use_last_and_first:
                self.add_item(self.go_to_first_page)
            self.add_item(self.go_to_previous_page)
            if not self.compact:
                self.add_item(self.go_to_current_page)
            self.add_item(self.go_to_next_page)
            if use_last_and_first:
                self.add_item(self.go_to_last_page)

    async def _get_kwargs_from_page(self, page: int) -> Dict[str, Any]:
        value = await maybe_coroutine(self.source.format_page, self, page)
        if isinstance(value, dict):
            return value
        elif isinstance(value, str):
            return {"content": value, "embed": None}
        elif isinstance(value, Embed):
            return {"embed": value, "content": None}
        else:
            return {}

    async def show_page(self, interaction: Interaction, page_number: int) -> None:
        page = await self.source.get_page(page_number)
        self.current_page = page_number
        kwargs = await self._get_kwargs_from_page(page)
        self._update_labels(page_number)
        if kwargs:
            if interaction.response.is_done():
                if self.message:
                    await self.message.edit(**kwargs, view=self)
            else:
                await interaction.response.edit_message(**kwargs, view=self)

    def _update_labels(self, page_number: int) -> None:
        self.go_to_first_page.disabled = page_number == 0
        max_pages = self.source.get_max_pages()
        if self.compact:
            self.go_to_last_page.disabled = (
                max_pages is None or (page_number + 1) >= max_pages
            )
            self.go_to_next_page.disabled = (
                max_pages is not None and (page_number + 1) >= max_pages
            )
            self.go_to_previous_page.disabled = page_number == 0
            return

        self.go_to_current_page.label = f"{str(page_number + 1)} / {max_pages}"
        self.go_to_next_page.disabled = False
        self.go_to_previous_page.disabled = False
        self.go_to_first_page.disabled = False

        if max_pages is not None:
            self.go_to_last_page.disabled = (page_number + 1) >= max_pages
            if (page_number + 1) >= max_pages:
                self.go_to_next_page.disabled = True
            if page_number == 0:
                self.go_to_first_page.disabled = True
                self.go_to_previous_page.disabled = True

    async def show_checked_page(self, interaction: Interaction, page_number: int) -> None:
        max_pages = self.source.get_max_pages()
        try:
            if max_pages is None:
                await self.show_page(interaction, page_number)
            elif max_pages > page_number >= 0:
                await self.show_page(interaction, page_number)
        except IndexError:
            pass

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user and interaction.user.id in (
            self.ctx.bot.owner_id,
            self.ctx.author.id,
        ):
            return True
        await interaction.response.send_message(
            "This is not your menu.", ephemeral=True
        )
        return False

    async def start(self) -> None:
        if (self.check_embeds and not self.ctx.channel.permissions_for(self.ctx.me).embed_links):
            await self.ctx.send("Bot does not have embed links permission in this channel. Reconfigure it first then try again.")
            return

        await self.source._prepare_once()
        page = await self.source.get_page(0)
        kwargs = await self._get_kwargs_from_page(page)
        self._update_labels(0)
        self.message = await self.ctx.send(**kwargs, view=self)

    @button(label="≪", style=ButtonStyle.blurple)
    async def go_to_first_page(self, button: Button, interaction: Interaction):
        await self.show_page(interaction, 0)

    @button(label="<", style=ButtonStyle.blurple)
    async def go_to_previous_page(self, button: Button, interaction: Interaction):
        await self.show_checked_page(interaction, self.current_page - 1)

    @button(label="Current", style=ButtonStyle.grey, disabled=True)
    async def go_to_current_page(self, button: Button, interaction: Interaction):
        pass

    @button(label=">", style=ButtonStyle.blurple)
    async def go_to_next_page(self, button: Button, interaction: Interaction):
        await self.show_checked_page(interaction, self.current_page + 1)

    @button(label="≫", style=ButtonStyle.blurple)
    async def go_to_last_page(self, button: Button, interaction: Interaction):
        await self.show_page(interaction, self.source.get_max_pages() - 1)

class LPage(ListPageSource):
    def __init__(self, ctx, data, _type, client):
        self.ctx = ctx
        self._type = _type
        self.client = client

        super().__init__(data, per_page=10)

    async def format_page(self, menu, entries):
        pages = []
        if self._type == "Messages":
            for index, entry in enumerate(entries, start=menu.current_page * self.per_page):
                user = await self.client.fetch_user(entry[0])
                _user = check_new_username(user)
                pages.append(f"{index + 1}. {_user}: **{entry[1]} 📧**")
        elif self._type == "Ligtas Points":
            for index, entry in enumerate(entries, start=menu.current_page * self.per_page):
                user = await self.client.fetch_user(entry[0])
                _user = check_new_username(user)
                pages.append(f"{index + 1}. {_user}: **{entry[1]} LP**")
        elif self._type in ["Solid Points (Monthly)", "Solid Points (Yearly)"]:
            for index, entry in enumerate(entries, start=menu.current_page * self.per_page):
                user = await self.client.fetch_user(entry[0])
                _user = check_new_username(user)
                pages.append(f"{index + 1}. {_user}: **{entry[1]:.2f} SP**")
        elif self._type == "Points":
            for index, entry in enumerate(entries, start=menu.current_page * self.per_page):
                user = await self.client.fetch_user(entry[0])
                _user = check_new_username(user)
                pages.append(f"{index + 1}. {_user}: <:money_icon:1075986284461445140> **{entry[1]}**")
        else:
            for index, entry in enumerate(entries, start=menu.current_page * self.per_page):
                user = await self.client.fetch_user(entry[0])
                pages.append(f"{index + 1}. {user}: **Level {entry[1]}** ({millify(entry[2], precision=2)} XP)")

        menu.embed.description = "\n".join(pages)
        return menu.embed

class LeaderboardPages(ViewPages):
    def __init__(self, entries, ctx, _type, client, users, per_page: int = 10):
        super().__init__(LPage(ctx, data=entries, _type=_type, client=client), ctx=ctx)
        self.embed = Embed(colour=0x2f3136, title=f"Server Leaderboards ({_type})").set_footer(text=f"You are #{users.index(ctx.author.id)+1} in the server leaderboards.", icon_url=self.ctx.author.avatar)

class PartnershipPage(ListPageSource):
    def __init__(self, ctx, data):
        self.ctx = ctx

        super().__init__(data, per_page=10)

    async def format_page(self, menu, entries):
        pages = []
        for index, entry in enumerate(entries, start=menu.current_page * self.per_page):
            pages.append(entry)

        menu.embed.description = "\n".join(pages)
        menu.embed.set_footer(text=f"There are a total of {len(pages)} partnered servers.", icon_url=self.ctx.guild.icon)
        return menu.embed

class PartnershipPages(ViewPages):
    def __init__(self, entries, ctx, per_page: int = 5):
        super().__init__(PartnershipPage(ctx, data=entries), ctx=ctx)
        self.embed = Embed(colour=0x2f3136, title=f"Server Partners", url="https://discord.gg/kbl")

class StarboardPage(ListPageSource):
    def __init__(self, ctx, data, _type, user):
        self.ctx = ctx
        self._type = _type
        self.user = user

        super().__init__(data, per_page=10)

    async def format_page(self, menu, entries):
        pages = []
        if self._type == "Global":
            for index, entry in enumerate(entries, start=menu.current_page * self.per_page):
                msg = await self.ctx.channel.fetch_message(entry[1])
                m = check_new_username(msg.author)
                pages.append(f"{index + 1}. `{entry[0]}` • {m} • [Click here!]({msg.jump_url})")
            menu.embed.description = "\n".join(pages) + f"\n\n**Use `.starboard @{m}` or `.starboard <key>` to view more details.**"
            menu.embed.set_footer(text=f"There are a total of {len(pages)} entries.", icon_url=self.ctx.guild.icon)
            return menu.embed
        elif self._type == "Member":
            for index, entry in enumerate(entries, start=menu.current_page * self.per_page):
                pages.append(entry)
            menu.embed.description = "\n".join(pages) + f"\n\n**Use `.starboard @{m}` or `.starboard <key>` to view more details.**"
            menu.embed.set_footer(text=f"There are a total of {len(pages)} entries.", icon_url=self.ctx.guild.icon)
            return menu.embed

class StarboardPages(ViewPages):
    def __init__(self, entries, ctx, _type, user, per_page: int = 5):
        super().__init__(StarboardPage(ctx, data=entries, _type=_type, user=user), ctx=ctx)
        if _type == "Global":
            self.embed = Embed(colour=0x2f3136, title=f"Starboard Lists (Global)", url="https://discord.gg/kbl")
        elif _type == "Member":
            m = check_new_username(user)
            self.embed = Embed(colour=0x2f3136, title=f"Starboard Lists ({m})", url="https://discord.gg/kbl")