# What is this?

Nightfury-Assistant is a simple personal utility Discord bot, made to be used as a user app.
The functionality of this bot follows what I personally use it for, feature requests are however welcome
and will be considered, as long as they follow the general scheme of the bot.

---

# Self-Hosting

1. Create an application on https://discord.com/developers/applications
2. Generate an OAuth link and add install the bot to your Discord account (this bot is intended as a user app)
3. Clone your repository onto a VPS or your own PC with `git clone <your repo url.git>`
4. Make sure Python 3.12+ is installed
5. Run `pip install -r requirements.txt`
6. Use PM2 or a similar tool to run the bot (`pm2 start bot.py --name Paw --interpreter python3`)

#### ⚠ **Further support with self-hosting will not be provided.** ⚠

# License

This project is licensed under GPL-3.0. Forks and redistributions must remain open-source. See the LICENSE file for
further info