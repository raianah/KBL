# KBL Bot

Welcome to the KBL Bot! This bot is designed specifically for the KBL Discord server. You can join us at [discord.gg/kbl](https://discord.gg/kbl) or [discord.gg/sgFqQFy3v7](https://discord.gg/sgFqQFy3v7).

## Features

- **Easy Role Management**: The bot allows for easy addition of pre-set roles, granting specific access to channels based on user roles.
  
- **Open Source**: Previously a closed-source project, the bot is now open-source. The developer has made this decision due to challenges in maintaining the code consistently, stemming from a lack of commitment, busy schedules, and increasing projects that led this project to be abandoned.

- **Cloning & Re-configuring**: You can clone the bot and reconfigure it based on your specific conditions and requirements.

### Cloning and Reconfiguring the Bot

1. **Install Git**:
   - If you don't have Git installed, download and install it from [git-scm.com](https://git-scm.com/).

2. **Clone the Repository**:
   - Open your terminal (Command Prompt, PowerShell, or Terminal).
   - Navigate to the directory where you want to clone the bot.
   - Run the following command to clone the repository:
     ```bash
     git clone https://github.com/raianah/KBL.git
     ```

3. **Navigate to the Project Directory**:
   - Change into the cloned directory:
     ```bash
     cd KBL
     ```

4. **Set Up a Virtual Environment (Optional but Recommended)**:
   - It's a good practice to use a virtual environment to manage dependencies.
   - Run the following command to create a virtual environment:
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     - On Windows:
       ```bash
       venv\Scripts\activate
       ```
     - On macOS/Linux:
       ```bash
       source venv/bin/activate
       ```

5. **Install Required Dependencies**:
   - Make sure you have `pip` installed. Then, run:
     ```bash
     pip install -r requirements.txt
     ```
   - This command installs all the necessary packages listed in the `requirements.txt` file.

6. **Create a `.env` File**:
   - In the root directory of the project, create a file named `.env`.
   - Add the following lines to the `.env` file:
     ```
     MAIN_TOKEN=your_main_bot_token
     BETA_TOKEN=your_beta_bot_token

     DB_HOST=your_database_host
     DB_PORT=your_database_port
     DB_USER=your_database_user
     DB_PASS=your_database_password
     DB_NAME=your_database_name
     ```
   - Replace `your_main_bot_token`, `your_beta_bot_token`, and the database connection details with your actual tokens and database information.

7. **Run the Bot**:
   - You can now run the bot using the following command:
     ```bash
     python __main__.py
     ```
   - Make sure to replace `__main__.py` with the actual entry point of your bot if it's named differently.

## Cogs and Files

For specific information regarding cogs and files, head to [cogs/IMPORTANT.md](cogs/IMPORTANT.md).

## Getting Started

1. **Data Transfer**: If you need to transfer existing data, please [email](mailto:guadalupesy2017@gmail.com) me for assistance. To ensure a smooth and secure data transfer, please provide the following information:
   - **Discord Username / User ID**: The user ID must be associated with a user who has used this bot at least once.
   - **Screenshot**: A screenshot of the Discord app (desktop or mobile) showing your username and the KBL server.
   - **Admin Permission**: Permission from the admins (thethimteam, raianxh_, alterednoobie) approving your request for data transfer.

   If you do not need to transfer existing data, you can start fresh with a new setup.

2. **Environment Variables**: Create a `.env` file in the root directory of your project. This file should include the following variables:
   - `MAIN_TOKEN`: Your main bot token.
   - `BETA_TOKEN`: Your beta bot token (if applicable).
   - Database connection information (e.g., database type, host, user, password).