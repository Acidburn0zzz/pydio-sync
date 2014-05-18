import json
import mock
import requests
import unittest

from httplib2 import Response
from .remote import PydioSdk


class RemoteSdkLocalTests(unittest.TestCase):

    def setUp(self):
        self.sdk = PydioSdk(
            'url', 'basepath', 'ws_id', 'user_id', 'auth')

    @mock.patch.object(requests, 'get')
    def test_changes_valid_json(self, mock_get):
        response = mock.Mock(spec=Response)
        response.content = '["foo", {"bar":["baz", null, 1.0, 2]}]'
        mock_get.return_value = response

        self.sdk.changes(555)
        assert mock_get.call_args == mock.call(
            url='url/api/basepath/changes/555?filter=ws_id',
            auth=('user_id', None)
        )

    @mock.patch.object(requests, 'get')
    def test_changes_invalid_json_exception_thrown(self, mock_get):
        response = mock.Mock(spec=Response)
        response.content = '["foo", {"bar"["baz", null, 1.0, 2]}]'
        mock_get.return_value = response
        exception_message = 'Invalid JSON value received while getting remote changes'

        with self.assertRaises(Exception) as context:
            self.sdk.changes(555)
            assert context.exception.message == exception_message

    @mock.patch.object(requests, 'get')
    def test_stat(self, mock_get):
        response = mock.Mock(spec=Response)
        test_data = [
            {
                'content': '["size", {"bar":["baz", null, 1.0, 2]}]',
                'result': json.loads('["size", {"bar":["baz", null, 1.0, 2]}]'),
            },
            {
                'content': '["foo", {"bar":["baz", null, 1.0, 2]}]',
                'result': False,
            },
            {
                'content': '',
                'result': False,
            },
        ]

        for data in test_data:
            response.content = data['content']
            mock_get.return_value = response
            assert self.sdk.stat('/test') == data['result']

    @mock.patch.object(requests, 'get')
    def test_stat_exception_thrown(self, mock_get):
        errors_thrown = [ValueError, Exception]
        mock_get.side_effect = errors_thrown

        for error in errors_thrown:
            with self.assertRaises(error):
                assert not self.sdk.changes(555)

# def stat(self, path, with_hash=False):
#         path = self.remote_folder + path;
#         action = '/stat_hash' if with_hash else '/stat'
#         try:
#             url = self.url + action + urllib.pathname2url(path.encode('utf-8'))
#             resp = requests.get(url=url, auth=self.auth)
#             data = json.loads(resp.content)
#             if not data:
#                 return False
#             if len(data) > 0 and 'size' in data:
#                 return data
#             else:
#                 return False
#         except ValueError:
#             return False
#         except:
#             return False