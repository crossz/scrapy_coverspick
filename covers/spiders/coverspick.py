# -*- coding: utf-8 -*-
import scrapy
import re

from covers.items import CoversItem

class CoverspickSpider(scrapy.Spider):
    name = 'coverspick'
    allowed_domains = ['covers.com']
    start_urls = ['https://www.covers.com/sports/nba/matchups/']

    date_string = ''

    def parse(self, response):
        # %% review purpose: yesterday game list
        previous_page = response.xpath('//*[@class="cmg_matchup_three_day_navigation"]/a[1]/@href').extract_first()
        # # '/Sports/NBA/Matchups?selectedDate=2018-03-09'
        page_yestoday = response.urljoin(previous_page)

        # %% predict analysis purpose: tomorrow game list
        next_page = response.xpath('//*[@class="cmg_matchup_three_day_navigation"]/a[3]/@href').extract_first()
        page_tmr = response.urljoin(next_page)

        # %% today: alive games (game finished or not determined by the time)
        current_page = response.xpath('//*[@class="cmg_matchup_three_day_navigation"]/a[2]/@href').extract_first()
        page_today = response.urljoin(current_page)


        # current date
        self.date_string = current_page[current_page.find('='):]


        # page to crawl
        the_page = page_yestoday
        yield scrapy.Request(the_page, callback=self.parse_gamelist)


    def parse_gamelist(self, response):
        '''
        follow links to consensus page for each game.
        '''
        for href in response.xpath('//*[@id="content"]//div//a[.="Consensus"]/@href'):
            yield response.follow(href, self.parse_consensus_page)


    def parse_consensus_page(self, response):
        '''
        find the real link to the expert lines api, then send requests.
        '''
        page_url = response.request.url
        # # 'https://contests.covers.com/Consensus/MatchupConsensusDetails/a80513f5-5ca8-47cc-ae21-a87e00f145d9?showExperts=False'
        searchObj = re.search(r'https://contests.covers.com/Consensus/MatchupConsensusDetails/(.*)\?showExperts.*', page_url)
        gameHash = searchObj.group(1)
        expertApi_prefix = 'https://contests.covers.com/Consensus/MatchupConsensusExpertDetails/'
        expert_api_url = expertApi_prefix + gameHash
        # print(' ------------------========================------------------------- ' + expert_api_url)

        yield scrapy.Request(expert_api_url, callback=self.parse_consensus_expertlines)
        

        # %% issues:
        '''
        # %% Covers' consensus using a dynamic api to retrieve expert lines, which scrapy can not directly crawl:

        # https://contests.covers.com/Consensus/MatchupConsensusDetails/a80513f5-5ca8-47cc-ae21-a87e00f145d9?showExperts=False

        # %% 抓不到: 因为这步是动态加载的另外一个接口, 需要用到 splash 的 js 渲染引擎.
        # //*[@id="expert_lines"]
        response.xpath('//*[@id="expert_lines"]').extract()
    
        # 截取第一个, 生成第二个:
        # https://contests.covers.com/Consensus/MatchupConsensusDetails/a80513f5-5ca8-47cc-ae21-a87e00f145d9?showExperts=False
        # https://contests.covers.com/Consensus/MatchupConsensusExpertDetails/e1bee5ea-2171-4e98-80d8-a87e00f1483f
        '''


    def parse_consensus_expertlines(self, response):
        '''
        find the real link to the expert lines api, then send requests.
        '''
        def prepare_item(this_game_string, pick_product):
            item = CoversItem()
            item['pick_product'] = pick_product

            item['date'] = self.date_string
            item['game'] = this_game_string

            item['leader'] = pick.xpath('td[1]//text()').extract_first()
            item['pick_team'] = pick.xpath('td[2]/div/a//text()').extract_first()
            item['pick_line'] = pick.xpath('td[2]/div/span//text()').extract_first()
            item['pick_desc'] = pick.xpath('td[3]//text()').extract_first()
            return item


        pick_options = response.css('div.covers-CoversConsensus-leagueHeader::text').extract()
        team_away = pick_options[0][pick_options[0].find('for ')+4:]
        team_home = pick_options[1][pick_options[1].find('for ')+4:]

        this_game = team_away + ' AT ' + team_home

        # item for ats_away
        picks_ats_away = response.xpath('/html/body/div[1]/table/tbody/tr')
        for pick in picks_ats_away[1:]:
            item = prepare_item(this_game, 'ats_away')
            yield item

        # item for ats_home
        picks_ats_home = response.xpath('/html/body/div[2]/table/tbody/tr')
        for pick in picks_ats_home[1:]:
            item = prepare_item(this_game, 'ats_home')
            yield item

        # item for ov_over
        # item for ov_under




