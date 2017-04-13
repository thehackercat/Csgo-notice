#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'LexusLee'

import json
import time
import random
import requests

from wxbot import *

# Steam API Key
steam_key = '522EA4B8554541FE7E200AB913788726'
# poupou's steam id
target_steam_id = '76561198148355194'

agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36(KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html) ',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
]

header = {
    'Content-type': 'text/json'
}

class SteamSpider():
    def __init__(self):
        self.steam_key = steam_key
        self.target_steam_id = target_steam_id
        self.player_info_url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/' \
                        '?key={key}&steamids={steam_id}'.format(key=steam_key, steam_id=target_steam_id)
        self.recent_played_game_url = 'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/' \
                         '?key={key}&steamid={steam_id}&format=json'.format(key=steam_key, steam_id=target_steam_id)

    # auto change user-agent
    def change_ua(self, header, agent_list):
        agent = random.choice(agent_list)
        header['user-agent'] = agent


    def get_page(self, url):
        self.change_ua(header, agent_list)
        r = requests.get(url, headers=header)
        return r.content


    def check_online(self, player_info):
        return True if player_info['response']['players'][0]['personastate'] == 1 else False


    def check_played_csgo(self, recent_played_game):
        games = recent_played_game['response']['games']
        for game in games:
            if game['name'] == 'Counter-Strike: Global Offensive':
                return True
        return False

class CsgoBot(WXBot):
    def __init__(self):
        super().__init__()
        steam_spider = SteamSpider()

    def handle_msg_all(self, msg):
        if msg['msg_type_id'] == 4 and msg['content']['type'] == 0 and msg['user']['id'] == 'delete2me':
            if msg['content']['data'] == u'来':
                self.send_msg_by_uid(u'等我上线', msg['user']['id'])
            if msg['content']['data'] == u'不来':
                self.send_msg_by_uid(u'过会再问', msg['user']['id'])

    def schedule(self):
        if self.get_csgo_status():
            self.send_msg_by_uid(u'来不来Go?', u'delete2me')
        time.sleep(5)

    def get_csgo_status(self):
        player_info = json.loads(self.steam_spider.get_page(self.steam_spider.player_info_url))
        recent_played_game = json.loads(self.steam_spider.get_page(self.steam_spider.recent_played_game_url))
        if player_info is not None and recent_played_game is not None:
            if self.steam_spider.check_online(player_info) and self.steam_spider.check_played_csgo(recent_played_game):
                print '检测到poupou正在Csgo'
                return True
        print 'poupou没在Csgo你等等吧'
        return False

def main():
    csgo_bot = CsgoBot()
    csgo_bot.DEBUG = True
    csgo_bot.run()

if __name__ == '__main__':
    main()



