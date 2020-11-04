import unittest
from six import u
from expects import *
import textwrap
import httpretty

from opentok import OpenTok, __version__, AuthError, ForceMuteError
from .validate_jwt import validate_jwt_header

class OpenTokForceMuteTest(unittest.TestCase):
    """" Class that contains test for force mute functionality """

    def setUp(self):
        self.api_key = u('123456')
        self.api_secret = u('1234567890abcdef1234567890abcdef1234567890')
        self.opentok = OpenTok(self.api_key, self.api_secret)
        self.session_id = u('SESSIONID')
        self.stream_id = u('STREAMID')
        self.excluded_stream_ids = [self.stream_id]

    @httpretty.activate
    def test_force_mute(self):
        """ Method to test force mute functionality using an OpenTok instance """

        httpretty.register_uri(
            httpretty.POST,
            u('https://api.opentok.com/v2/project/{0}/session/{1}/stream/{2}/mute').format(
                self.api_key,
                self.session_id,
                self.stream_id
            ),
            status=204,
            content_type=u('application/json')
        )

        self.opentok.force_mute(self.session_id, self.stream_id)

        validate_jwt_header(self, httpretty.last_request().headers[u('x-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to(contain(u('OpenTok-Python-SDK/')+__version__))
        expect(httpretty.last_request().headers[u('content-type')]).to(equal(u('application/json')))

    @httpretty.activate
    def test_throws_force_mute_exception(self):
        """ This method should throw a ForceMuteError """

        httpretty.register_uri(
            httpretty.POST,
            u('https://api.opentok.com/v2/project/{0}/session/{1}/stream/{2}/mute').format(
                self.api_key,
                self.session_id,
                self.stream_id
            ),
            status=400,
            content_type=u('application/json')
        )

        self.assertRaises(
            ForceMuteError,
            self.opentok.force_mute,
            self.session_id,
            self.stream_id
        )

    @httpretty.activate
    def test_throws_auth_exception(self):
        """ This method should throw an AuthError """

        httpretty.register_uri(
            httpretty.POST,
            u('https://api.opentok.com/v2/project/{0}/session/{1}/stream/{2}/mute').format(
                self.api_key,
                self.session_id,
                self.stream_id
            ),
            status=403,
            content_type=u('application/json')
        )

        self.assertRaises(
            AuthError,
            self.opentok.force_mute,
            self.session_id,
            self.stream_id
        )

    @httpretty.activate
    def test_force_mute_all(self):
        """ Method to test force mute functionality using an OpenTok instance """

        httpretty.register_uri(
            httpretty.POST,
            u('https://api.opentok.com/v2/project/{0}/session/{1}/mute').format(
                self.api_key,
                self.session_id
            ),
            body=textwrap.dedent(u("""\
                                               {
                                                  "exclude": ["STREAMID"]
                                                }""")),
            status=204,
            content_type=u('application/json')
        )

        self.opentok.force_mute_all(self.session_id, self.excluded_stream_ids)

        validate_jwt_header(self, httpretty.last_request().headers[u('x-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to(contain(u('OpenTok-Python-SDK/') + __version__))
        expect(httpretty.last_request().headers[u('content-type')]).to(equal(u('application/json')))

    @httpretty.activate
    def test_force_mute_all_throws_force_mute_exception(self):
        """ This method should throw a ForceMuteError """

        httpretty.register_uri(
            httpretty.POST,
            u('https://api.opentok.com/v2/project/{0}/session/{1}/mute').format(
                self.api_key,
                self.session_id
            ),
            body=textwrap.dedent(u("""\
                                                       {
                                                          "exclude": ["STREAMID"]
                                                        }""")),
            status=400,
            content_type=u('application/json')
        )

        self.assertRaises(
            ForceMuteError,
            self.opentok.force_mute_all,
            self.session_id,
            self.excluded_stream_ids
        )

    @httpretty.activate
    def test_force_mute_all_throws_auth_exception(self):
        """ This method should throw an AuthError """

        httpretty.register_uri(
            httpretty.POST,
            u('https://api.opentok.com/v2/project/{0}/session/{1}/mute').format(
                self.api_key,
                self.session_id
            ),
            body=textwrap.dedent(u("""\
                                                       {
                                                          "exclude": ["STREAMID"]
                                                        }""")),
            status=403,
            content_type=u('application/json')
        )

        self.assertRaises(
            AuthError,
            self.opentok.force_mute_all,
            self.session_id,
            self.excluded_stream_ids
        )