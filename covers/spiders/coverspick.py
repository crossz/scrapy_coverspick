# -*- coding: utf-8 -*-
import scrapy
import re
import time
import datetime

from covers.items import CoversItem
from covers.items import ScoreItem
from covers.items import ExpertpickItem

class CoverspickSpider(scrapy.Spider):
    name = 'coverspick'
    allowed_domains = ['covers.com']


    ## mode for one-day-guide/review.
    start_urls = ['https://www.covers.com/Sports/NBA/Matchups']


    ## mode for batch download w/ start_date/end_date.
    # start_urls = ['https://www.covers.com/Sports/NBA/Matchups?selectedDate=2019-10-22']
    # end_date = '2019-12-31'

    # %% season 2017-18; No expert pick data already on season 2019-20.
    # start_urls = ['https://www.covers.com/Sports/NBA/Matchups?selectedDate=2017-10-17']
    # end_date = '2017-12-31'
    # start_urls = ['https://www.covers.com/Sports/NBA/Matchups?selectedDate=2018-01-01']
    # end_date = '2018-06-09'

    # %% season 2018-19
    # start_urls = ['https://www.covers.com/Sports/NBA/Matchups?selectedDate=2018-10-16']
    # end_date = '2018-12-31'
    # start_urls = ['https://www.covers.com/Sports/NBA/Matchups?selectedDate=2019-01-01']
    # end_date = '2019-06-13'

    if 'end_date' not in locals():
        # end_date = str(datetime.date.today() + datetime.timedelta(+1))
        end_date = str(datetime.date.today())

    def parse(self, response):
        # %% predict analysis purpose: tomorrow game list
        next_page = response.xpath('//*[@class="cmg_matchup_three_day_navigation"]/a[3]/@href').extract_first()
        ## '/Sports/NBA/Matchups?selectedDate=2018-03-09'
        page_tomorrow = response.urljoin(next_page)

        # %% today: alive games (game finished or not determined by the time)
        current_page = response.xpath('//*[@class="cmg_matchup_three_day_navigation"]/a[2]/@href').extract_first()
        page_today = response.urljoin(current_page)
        
        
        ## ---------------- mode for daily one-page-guide/review or batch download w/ start_date/end_date ----------------
        ## the date to be passed
        if response.url.find('=') == -1:
            matchup_date_string = str(datetime.date.today() + datetime.timedelta(-1))
        else:
            matchup_date_string = response.url[response.url.find('=')+1:] ## the date to be passed
        ## */ ---------------- mode END ----------------


        # condition to stop crawling
        if time.strptime(matchup_date_string, "%Y-%m-%d") <= time.strptime(self.end_date, "%Y-%m-%d"):



            # # pick page to crawl
            # for href in response.xpath('//*[@id="content"]//div//a[.="Consensus"]/@href'):
            #     yield response.follow(href, self.parse_consensus_page, meta={'date_string':matchup_date_string})

        
            # score, teams, date to crawl
            for matchup in response.css('div.cmg_matchup_game'):
                item = ScoreItem()

                div_teams = matchup.xpath('.//div[@class="cmg_team_name"]/text()').extract()
                team_away = div_teams[0].strip()
                team_home = div_teams[3].strip()
                score_away = matchup.xpath('.//div[@class="cmg_matchup_list_score"]').css('div.cmg_matchup_list_score_away::text').extract_first()
                score_home = matchup.xpath('.//div[@class="cmg_matchup_list_score"]').css('div.cmg_matchup_list_score_home::text').extract_first()
                ats = matchup.xpath('.//div[@class="cmg_matchup_game_box cmg_game_data"]/@data-game-odd').extract_first()
                hilo = matchup.xpath('.//div[@class="cmg_matchup_game_box cmg_game_data"]/@data-game-total').extract_first()

                # ats = 
                # hilo = 
                # matchup_date_string = response.url[response.url.find('=')+1:]
                game_string = team_away + '@' + team_home + '_ON_' + matchup_date_string

                item['game_string'] = game_string
                item['date_string'] = matchup_date_string
                
                item['team_away'] = team_away
                item['team_home'] = team_home
                item['score_away'] = score_away
                item['score_home'] = score_home
                item['ats'] = ats
                item['hilo'] = hilo
                
                yield item

            # consensus link to crawl
            # for matchup in response.css('div.cmg_matchup_game'):
                consensus_href = matchup.xpath('.//div//a[.="Consensus"]/@href').extract_first()
                yield response.follow(consensus_href, self.parse_consensus_page, meta={'date_string':matchup_date_string, 'game_string': game_string})

            # next page to crawl        
            yield scrapy.Request(page_tomorrow, callback=self.parse)


    def parse_consensus_page(self, response):
        '''
        To find the real link to the expert lines api, then send requests.
        '''
        page_url = response.request.url
        # # 'https://contests.covers.com/Consensus/MatchupConsensusDetails/a80513f5-5ca8-47cc-ae21-a87e00f145d9?showExperts=False'
        searchObj = re.search(r'https://contests.covers.com/Consensus/MatchupConsensusDetails/(.*)\?showExperts.*', page_url)
        gameHash = searchObj.group(1)
        expertApi_prefix = 'https://contests.covers.com/Consensus/MatchupConsensusExpertDetails/'
        expert_api_url = expertApi_prefix + gameHash
        print(' ------------------========================------------------------- ' + expert_api_url)


        # current date
        # date_string = response.xpath('//*[@id="mainContainer"]/p/text()').extract()[2].split(',')[1].strip()
        ## ' - Thursday, March 1, 2018 7:30 PM\r\n'
        date_string = response.meta['date_string']
        game_string = response.meta['game_string']

        yield scrapy.Request(expert_api_url, callback=self.parse_consensus_expertlines, meta={'date_string':date_string, 'game_string': game_string})
        

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


        '''
        To extract the summarized experts picks.
        This can be used to generate one-page-overview for daily betting; Also, this can be used to do simple review for expert group's performance.
        # 这个其实可以和 ScoreItem 放在一起, 但是由于这些数据不在同一个页面, 不方便同时存入一行数据里, 所以拆成 2 种 item 数据用以存储和分析.
        '''
        left_wagers_list = response.xpath('//div[@id="experts_analysis_content"]//div[@class="covers-CoversConsensusDetailsTable-awayWagers"]/text()').extract()
        right_wagers_list = response.xpath('//div[@id="experts_analysis_content"]//div[@class="covers-CoversConsensusDetailsTable-homeWagers"]/text()').extract()

        item = ExpertpickItem()
        item['game_string'] = game_string
        item['date_string'] = date_string
        item['product1_left'] = left_wagers_list[0]
        item['product1_right'] = right_wagers_list[0]
        item['product2_left'] = left_wagers_list[1]
        item['product2_right'] = right_wagers_list[1]

        print(' ------------------========================------------------------- ' + game_string + ': ' + left_wagers_list[0] + ' vs ' + right_wagers_list[0] + ' AND ' + left_wagers_list[1] + ' vs ' + right_wagers_list[1])

        yield item

    def parse_consensus_expertlines(self, response):
        '''
        find the real link to the expert lines api, then send requests.
        '''

        def prepare_item(this_game_string, pick_product):
            item = CoversItem()
            
            item['game_string'] = response.meta['game_string']
            item['pick_line'] = pick.xpath('td[2]/div/span//text()').extract_first()
            item['pick_team'] = pick.xpath('td[2]/div/a//text()').extract_first()
            item['pick_desc'] = pick.xpath('td[3]//text()').extract_first()
            item['pick_product'] = pick_product
            item['date_string'] = response.meta['date_string']    
            item['leader'] = pick.xpath('td[1]//text()').extract_first()
            # return item

            desc = item['pick_desc']
            if desc.find("#1 ") != -1 or desc.find("#2 ") != -1:
                return item
            else:
                pass


        # pick_options = response.css('div.covers-CoversConsensus-leagueHeader::text').extract()
        # team_away = pick_options[0][pick_options[0].find('for ')+4:]
        # team_home = pick_options[1][pick_options[1].find('for ')+4:]
        # this_game = team_away + ' AT ' + team_home
        this_game = response.css('p.covers-CoversConsensus-detailsGameDate span::text').extract_first()

        # item for ats_away
        picks_ats_away = response.xpath('/html/body/div[1]/table/tbody/tr')
        if len(picks_ats_away.extract()) > 1:
            # temp1 = list([picks_ats_away[1]])
            # for pick in temp1:
            for pick in picks_ats_away[1:]:
                item = prepare_item(this_game, 'ats_away')
                yield item



        # item for ats_home
        picks_ats_home = response.xpath('/html/body/div[2]/table/tbody/tr')
        if len(picks_ats_home.extract()) > 1:
            for pick in picks_ats_home[1:]:
                item = prepare_item(this_game, 'ats_home')
                yield item




        # item for ov_over
        # item for ov_under




