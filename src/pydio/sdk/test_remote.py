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

        assert self.sdk.changes(555) == json.loads(response.content)
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
            assert self.sdk.stat('/path') == data['result']

        assert mock_get.call_args_list[0] == mock_get.call_args_list[1]
        assert mock_get.call_args_list[1] == mock_get.call_args_list[2]
        assert mock_get.call_args_list[2] == mock.call(
            url='url/api/basepath/statws_id/path',
            auth=('user_id', None)
        )

    @mock.patch.object(requests, 'get')
    def test_stat_exception_thrown(self, mock_get):
        errors_thrown = [ValueError, Exception]
        mock_get.side_effect = errors_thrown

        for error in errors_thrown:
            with self.assertRaises(error):
                assert not self.sdk.changes(555)

    @mock.patch.object(requests, 'post')
    def test_bulk_stat(self, mock_post):
        response = mock.Mock(spec=Response)
        response.content = '["foo", {"bar":["baz", null, 1.0, 2]}]'
        mock_post.return_value = response
        result_string = ''.join(['{"/path1": ', response.content, '}'])
        result = json.loads(result_string)

        assert self.sdk.bulk_stat(['/path1']) == result
        assert mock_post.call_args == mock.call(
            'url/api/basepath/statws_id/path1',
            data={'nodes[]': ['ws_id/path1']},
            auth=('user_id', None)
        )

    @mock.patch.object(json, 'loads')
    @mock.patch.object(requests, 'post')
    def test_bulk_stat_exception_thrown(self, mock_post, mock_loads):
        response = mock.Mock(spec=Response)
        response.content = '["foo", {"bar":["baz", null, 1.0, 2]}]'
        mock_post.return_value = response
        mock_loads.side_effect = ValueError

        with self.assertRaises(Exception):
            self.sdk.bulk_stat(['/path'])

    @mock.patch.object(requests, 'get')
    def test_mkdir(self, mock_get):
        response = mock.Mock(spec=Response)
        response.content = '["foo", {"bar":["baz", null, 1.0, 2]}]'
        mock_get.return_value = response

        assert self.sdk.mkdir('/path') == response.content
        assert mock_get.call_args == mock.call(
            url='url/api/basepath/mkdirws_id/path',
            auth=('user_id', None)
        )

    @mock.patch.object(requests, 'get')
    def test_mkfile(self, mock_get):
        response = mock.Mock(spec=Response)
        response.content = '["foo", {"bar":["baz", null, 1.0, 2]}]'
        mock_get.return_value = response

        assert self.sdk.mkfile('/path') == response.content
        assert mock_get.call_args == mock.call(
            url='url/api/basepath/mkfilews_id/path',
            auth=('user_id', None)
        )

    @mock.patch.object(requests, 'post')
    def test_rename(self, mock_post):
        response = mock.Mock(spec=Response)
        response.content = '["foo", {"bar":["baz", null, 1.0, 2]}]'
        mock_post.return_value = response

        called_with_arguments = [
            mock.call(
                url='url/api/basepath/rename',
                data={'dest': 'ws_id/target', 'file': 'ws_id/source'},
                auth=('user_id', None)),
            mock.call(
                url='url/api/basepath/rename',
                data={'dest': 'ws_id/test', 'file': 'ws_id/test'},
                auth=('user_id', None))
        ]

        assert self.sdk.rename('/source', '/target') == response.content
        assert self.sdk.rename('/test', '/test') == response.content
        assert mock_post.call_args_list == called_with_arguments

    @mock.patch.object(requests, 'get')
    def test_delete(self, mock_get):
        response = mock.Mock(spec=Response)
        response.content = '["foo", {"bar":["baz", null, 1.0, 2]}]'
        mock_get.return_value = response

        assert self.sdk.delete('/path') == response.content
        assert mock_get.call_args == mock.call(
            url='url/api/basepath/deletews_id/path',
            auth=('user_id', None)
        )

if __name__ == '__main__':
    unittest.main()
