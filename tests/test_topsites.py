#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Tests for topsites script."""

import datetime
import unittest
from xml.dom.minidom import parseString

from mock import patch

from tools import topsites


TEST_XML = '''<?xml version="1.0"?><aws:TopSitesResponse xmlns:aws="http://alexa.amazonaws.com/doc/2005-10-05/"><aws:Response><aws:OperationRequest><aws:RequestId>9ffc5e13-175e-4c7e-b33b-0efe3501d1f3</aws:RequestId></aws:OperationRequest><aws:TopSitesResult><aws:Alexa><aws:TopSites><aws:List><aws:CountryName>China</aws:CountryName><aws:CountryCode>CN</aws:CountryCode><aws:TotalSites>671496</aws:TotalSites><aws:Sites><aws:Site><aws:DataUrl>baidu.com</aws:DataUrl><aws:Country><aws:Rank>1</aws:Rank><aws:Reach><aws:PerMillion>358000</aws:PerMillion></aws:Reach><aws:PageViews><aws:PerMillion>77410</aws:PerMillion><aws:PerUser>11.5</aws:PerUser></aws:PageViews></aws:Country><aws:Global><aws:Rank>4</aws:Rank></aws:Global></aws:Site></aws:Sites></aws:List></aws:TopSites></aws:Alexa></aws:TopSitesResult><aws:ResponseStatus><aws:StatusCode>Success</aws:StatusCode></aws:ResponseStatus></aws:Response></aws:TopSitesResponse>'''  # nopep8
TEST_QUERY_STRING = 'Action=TopSites&AWSAccessKeyId=1234567890ABCDEFGHIJ&Count=100&CountryCode=CN&ResponseGroup=Country&SignatureMethod=HmacSHA256&SignatureVersion=2&Start=1&Timestamp=2006-01-01T00%3A00%3A00.000Z'  # nopep8
TEST_QUERY_URI = 'http://ats.amazonaws.com/?Action=TopSites&AWSAccessKeyId=1234567890ABCDEFGHIJ&Count=100&CountryCode=CN&ResponseGroup=Country&SignatureMethod=HmacSHA256&SignatureVersion=2&Start=1&Timestamp=2006-01-01T00%3A00%3A00.000Z&Signature=KNslS3thvc%2FROl5zLaDdpYsommrFfVAfz3D6Ebqavxg%3D'  # nopep8


class TestTopsites(unittest.TestCase):
    def setUp(self):
        self.dom = parseString(TEST_XML)
        topsites.ats_access_key = '1234567890ABCDEFGHIJ'
        topsites.ats_secret_key = 'JIHGFEDCBA0987654321'

    def test_build_uri(self):
        testdt = datetime.datetime(2006, 1, 1, 0, 0, 0, 0)
        with patch('datetime.datetime') as dt_mock:
            dt_mock.utcnow.return_value = testdt
            self.assertEqual(topsites.build_uri('CN', 1), TEST_QUERY_URI)

    def test_build_query_string(self):
        testdt = datetime.datetime(2006, 1, 1, 0, 0, 0, 0)
        with patch('datetime.datetime') as dt_mock:
            dt_mock.utcnow.return_value = testdt
            self.assertEqual(topsites.build_query_string('CN', 1),
                             TEST_QUERY_STRING)

    def test_node_text(self):
        site = self.dom.getElementsByTagName('aws:Site')[0]
        self.assertEqual(topsites.node_text(site, 'aws:DataUrl'), 'baidu.com')
        self.assertEqual(topsites.node_text(site, 'aws:Rank'), '1')


if __name__ == '__main__':
    unittest.main()
