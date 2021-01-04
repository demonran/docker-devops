#!/usr/bin/env python
# coding= utf-8

import os
import json
from urllib.request import urlopen
from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest
import configparser


class DnsHandler:
    conf = configparser.ConfigParser()
    conf.read('config.ini')
    # 从阿里云开发者后台获取Access_Key_Id和Access_Key_Secret
    access_key_id = conf.get('aliyun', 'access_key_id')
    access_key_secret = conf.get('aliyun', 'access_key_secret')
    region_id = conf.get('aliyun', 'region_id')

    # 填入自己的域名
    domain_name = conf.get('aliyun', 'domain_name')
    # 填入二级域名的RR值
    rr_keyword = conf.get('aliyun', 'rr_keyword')

    # 解析记录类型，一般为A记录
    record_type = "A"

    # 用于储存解析记录的文件名
    file_name = ".ip_addr"

    client = None
    record = None
    current_ip = ''

    # 初始化，获取client实例
    def __init__(self):
        self.client = AcsClient(
            self.access_key_id,
            self.access_key_secret,
            self.region_id
        )
        self.record = self.get_record()
        self.current_ip = self.get_current_ip()

    # 如果公网IP发生变化，则自动修改阿里云解析记录
    def reset(self):
        if self.current_ip != self.get_record_value():
            print(self.current_ip)
            print(self.get_record_value())
            self.update_record(self.current_ip)


    # 获取阿里云域名解析完整记录，并使用文件缓存
    def get_record(self):
        if os.path.isfile(self.file_name):
            file_handler = open(self.file_name, 'r')
            r = file_handler.read()
            file_handler.close()
        else:
            request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
            request.set_PageSize(10)
            request.set_action_name("DescribeDomainRecords")
            request.set_DomainName(self.domain_name)
            request.set_RRKeyWord(self.rr_keyword)
            request.set_TypeKeyWord(self.record_type)
            r = str(self.client.do_action_with_exception(request), encoding="utf-8")
            print(r)
            file_handler = open(self.file_name, 'w')
            file_handler.write(r)
            file_handler.close()
        return json.loads(r)

    # 获取阿里云域名解析记录ID
    def get_record_id(self):
        return self.record["DomainRecords"]["Record"][0]["RecordId"]

    # 获取当前域名解析记录
    def get_record_value(self):
        return self.record["DomainRecords"]["Record"][0]["Value"]

    # 修改阿里云解析记录
    def update_record(self, value):
        request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
        request.set_action_name("UpdateDomainRecord")
        request.set_RecordId(self.get_record_id())
        request.set_Type(self.record_type)
        request.set_RR(self.rr_keyword)
        request.set_Value(value)
        self.client.do_action_with_exception(request)
        os.remove(self.file_name)

    # 获取当前公网IP
    def get_current_ip(self):
        return json.load(urlopen('http://jsonip.com'))['ip']


# 实例化类并启动更新程序
dns = DnsHandler()
dns.reset()
