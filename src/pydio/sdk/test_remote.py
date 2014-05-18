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
    def test_changes(self, mock_get):
        response = mock.Mock(spec=Response)
        response.content = json.dumps('\\')
        mock_get.return_value = response
        print self.sdk.changes(555)

        assert mock_get.call_args == mock.call(
            url='url/api/basepath/changes/555?filter=ws_id',
            auth=('user_id', None)
        )
