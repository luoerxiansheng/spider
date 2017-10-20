#coding:utf-8

from settings import user_agent_list
import random

class RandomUser():

    def process_request(self,request,spider):

        ua = random.choice(user_agent_list)

        if ua:

            request.headers.setdefault('User-Agent',ua)