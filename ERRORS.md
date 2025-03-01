# Errors and Issues

This document outlines known issues and errors related to the KBL Bot project. Please review the following points for troubleshooting and necessary actions.

## 1. monthly_awards.py

### Issue: Spamming Messages
- **Description**: As of February 28, 2025, at 8:00 PM, the bot is generating 7,000 instances of a message due to a bug in the `last_day` function.
- **Cause**: The `last_day` function is returning the Unix time for February 28, 2025, at 8:00 PM, instead of the last day of the following month at 8:00 PM.
- **Solution**: The `last_day` function should be modified to check for the last day of the next month and provide the Unix time for that date at 8:00 PM. Check `properties/funcs.py` and search for `last_day()` function there.

## 2. [easy_pil](https://github.com/raianah/easy-pil)

### Issue: Compatibility Problems
- **Description**: The `easy_pil` library being used by my fork may lead to more problems as updates are released.
- **Action Required**: Attention is needed to reconfigure the code with each update to prevent unnecessary errors. A long-term solution should be considered to ensure compatibility and stability to my fork of `easy_pil`. Other options are consider tranferring to `Pillow` (`pip install Pillow`) or `easy_pil` from the original creator.

## 3. rankings.py

### Issue: Disabled Features
- **Description**: The `shop` and `ranksettings` features are currently disabled due to the deletion of assets.
- **Reason**: The previous assets used in this project are implemented and owned by the previous developer (`raianxh_`), which may generate copyright claims.
- **Action Required**: Developers must provide their own assets for these features to function correctly. In fact, all assets referenced in this file must be provided by your own.

---

Please address these issues as soon as possible to ensure the smooth operation of the KBL Bot. If you have any questions or need further assistance, feel free to reach out.