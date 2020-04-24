import datetime
import json
import praw
import sys
import time
import traceback


class Bot():
    def botcode(self):
        for subreddit_configuration in self.subreddit_configurations():
            post_timedelta = self.calculate_timedelta(subreddit_configuration)

            if self.now_to_timestamp() >= post_timedelta:
                username = subreddit_configuration['bot_username']
                subreddit = subreddit_configuration['subreddit']
                reddit = self.reddit_instance_for(username)
                post_template = self.post_template_for_account(username)
                title = post_template['post_title']

                if post_template['is_self']:
                    post_body = post_template['post_body']
                    reddit.subreddit(subreddit).submit(
                        title=title, selftext=post_body)
                else:
                    url = post_template['url']
                    reddit.subreddit(subreddit).submit(title=title, url=url)

                self.write_last_updated_date_for(subreddit_configuration)

    def parse_last_post_date(self, config):
        date = config['last_posted_on']
        if date == None:
            return date
        else:
            converted_date = datetime.datetime.fromtimestamp(float(date))

            return self.timestamp_for(converted_date)

    def calculate_timedelta(self, config):
        post_date = config['last_posted_on']

        if post_date == None:
            return -1
        else:
            time = config['time']
            years = time['years']
            months = time['months']
            days = time['days'] + (years * 365) + (months * 30)
            hours = time['hours']
            minutes = time['hours']
            seconds = time['seconds']

            timedelta = datetime.timedelta(
                days=days, hours=hours, minutes=minutes, seconds=seconds)
            last_post_date = self.date_from(post_date)

        return self.timestamp_for(last_post_date + timedelta)

    def now_to_timestamp(self):
        return self.timestamp_for(datetime.datetime.now())

    def timestamp_for(self, date):
        return datetime.datetime.timestamp(date)

    def date_from(self, timestamp):
        return datetime.datetime.fromtimestamp(timestamp)

    def subreddit_configurations(self):
        data = self.load_json('subreddit_configurations.json')

        return data

    def reddit_instance_for(self, bot_username):
        account_details = self.bot_account_details_for(bot_username)
        reddit = praw.Reddit(username=bot_username,
                             password=account_details['bot_password'],
                             client_id=account_details['bot_client_id'],
                             client_secret=account_details['bot_client_secret'],
                             user_agent=account_details['bot_user_agent'])

        return reddit

    def bot_account_details_for(self, bot_username):
        data = self.load_json('accounts.json')

        return data[bot_username]

    def post_template_for_account(self, username):
        templates = self.load_json('post_templates.json')
        accounts = self.load_json('accounts.json')
        template_name = accounts[username]['use_template']

        try:
            data = [template for template in templates if template['template_name'] == template_name][0]
        except IndexError:
            data = templates[0]

        return data

    def write_last_updated_date_for(self, config):
        configurations = self.load_json('subreddit_configurations.json')

        for configuration in configurations:
            if configuration == config:
                configuration_index = configurations.index(config)
                config['last_posted_on'] = self.now_to_timestamp()
                configurations[configuration_index] = config

                with open('subreddit_configurations.json', 'w') as json_file:
                    json.dump(configurations, json_file, indent=2)

                return

    def load_json(self, path):
        with open(path) as f:
            data = json.load(f)

        return data


if __name__ == '__main__':
    while True:
        try:
            with open('bot_settings.json') as f:
                settings = json.load(f)

            if settings['sleep_enabled'] == True:
                t = settings['sleep_time']
                hours = t['hours']
                minutes = t['minutes']
                seconds = t['seconds']

                sleep_time = (hours * 3600) + (minutes * 60) + seconds
            else:
                sleep_time = 0

            Bot().botcode()
            time.sleep(sleep_time)
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception:
            traceback.print_exc()
