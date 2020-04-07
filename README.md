# Bulk Post Bot

Bulk Post Bot is a completely configurable Reddit bot that can post a message to an arbitrary number of subreddits over a variety of bot accounts.

# Configuration

Bulk Post Bot has 3 main config files, each using JSON. They are: `accounts.json`, `subreddit_configurations.json`, and `post_template.json`.

# `accounts.json`:

Here, you'll need to define each of your bot accounts that you intend to use:

```json
{
  "bot_username": { // Your bot username will need to be defined here.
                   "bot_password": "BOT_PASSWORD",
                    "bot_client_id": "BOT_CLIENT_ID",
                    "bot_client_secret": "BOT_CLIENT_SECRET",
                    "bot_user_agent": "BOT_USER_AGENT"
                   },

  . . .

}
```

If you need help setting up a bot account or registering your script with Reddit, check out the post[here](https: // www.reddit.com/r/RequestABot/comments/cyll80/a_comprehensive_guide_to_running_your_reddit_bot/).

# `post_template.json`:

Here is where you'll define your post:

```json
{
    "post_title": "Test Title",
    "is_self": true,
    "url": "https://www.example.com",
    "post_body": "This is a test."
}
```

If `is_self` is set to `true`, then your post will be a link post and reference the `post_title` and `url` parameters. Otherwise, it'll be a self post and reference the `post_body` parameter instead.

# `subreddit_configurations.json`:

Here you'll define each of the subreddits you intend to make your post to, the duration between posts, and the account that you want to use to make the post:

```json
[
    {
        "subreddit": "testingground4bots",
        "bot_username": "BOT_USERNAME",
        "time": {
            "years": 0,
            "months": 0,
            "days": 7,
            "hours": 0,
            "minutes": 0,
            "seconds": 0
        },
        "last_posted_on": null
    },

    . . .

]
```

Worth noting that the bot username that you select MUST be present in `accounts.json`, else nothing will happpen.

In the above example, the bot would make the post every week beginning at the time you start the bot. You can add an arbitrary number of subreddits here, and it will loop through each one.

# Important!

You can set the time duration to a low(or zero!) number, but this is likely to cause errors at best and an annoyance at worst.

# Usage

After configuration, simply run `python bot.py` and watch your bot work!

You can edit any of the parameters in any of the configuration files and the bot will hot reload and use the new config on the next available post time.
