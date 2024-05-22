# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import json
from urllib import parse

import re
import requests
from typing import Optional

import wlc
from wlc import config as cfg

# Supported Weblate version
WEBLATE_SUPPORTED_VERSION = "5.4"


class IniConfig(object):
    """Object that stores weblate.ini configuration.

    Read url and key from weblate.ini and make its values available.
    Attributes:
    url: The URL of the Weblate server.
    key: The API key to use for authentication.
    _inifile: The path to the ini file to load values from (not public).

    """

    def __init__(self, inifile):
        self._inifile = inifile
        self._find_config()

    def _find_config(self):
        config = cfg.WeblateConfig()
        config.load(self._inifile)
        self.url, self.key = config.get_url_key()


class WeblateRestService(object):
    """Object that communicates with the Weblate REST API.

    Attributes:
    url: The URL of the Weblate server.
    key: The API key to use for authentication.
    headers: The HTTP headers to use for requests. Must contain the key.
    verify: Whether to verify SSL certificates.

    """

    def __init__(
        self,
        wconfig,
        accept="application/json, text/javascript",
        content_type="application/json",
        verify=True,
    ):
        self.url, self.key = wconfig.url, wconfig.key
        self.weblate_obj = wlc.Weblate()
        self.headers = {
            "Accept": accept,
            "Content-Type": content_type,
            "Authorization": "Token " + self.key,
        }
        self.verify = verify

        current_version = self.get_weblate_cloud_version()
        if not current_version.startswith(WEBLATE_SUPPORTED_VERSION):
            raise ValueError(
                "Unsupported server version: %(version)s.",
                {"version": current_version}
            )

    def _construct_url(self, url_fragment):
        return parse.urljoin(self.url, url_fragment)

    def query(self, url_fragment, raise_errors=True):
        request_url = self._construct_url(url_fragment)
        self.headers["Accept"] = "application/json, text/javascript"

        try:
            r = requests.get(
                request_url,
                headers=self.headers,
                verify=self.verify,
                )
        except requests.exceptions.ConnectionError as e:
            # raise ValueError("Connection Error: %s" % e)
            print(e)
        if raise_errors and r.status_code != 200:
            raise ValueError(
                "Got status code %s for %s" % (r.status_code, request_url)
                )
        if raise_errors and not r.content:
            raise ValueError(
                "Did not receive any data from %s" % request_url
                )
        return r

    def push(self, url_fragment, data):
        request_url = self._construct_url(url_fragment)
        try:
            return requests.put(
                request_url,
                verify=self.verify,
                headers=self.headers,
                data=json.dumps(data),
            )
        except requests.exceptions.ConnectionError:
            raise ValueError("Connection error")

    def _base_url(self) -> str:
        parsed_url = parse.urlparse(self.url)
        baseurl = f"{parsed_url.scheme}://{parsed_url.netloc}"

        return baseurl

    def get_weblate_cloud_version(self) -> Optional[str]:
        """Function that retrieves Weblate version

        Note that the information is not available via REST API as of now
        so crawling the version via web page

        """

        request_url = self._base_url()
        response = requests.get(request_url)
        version_pattern = r"weblate-(\d+\.\d+)"

        version_match = re.search(version_pattern, response.text)

        if version_match:
            version = version_match.group(1)
            return version

        return None
