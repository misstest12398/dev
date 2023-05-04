# -*- coding:utf-8 -*-
# @Time    :2023/5/4 10:49
# @Author  :DongFangchao
# @Email   :539699305@qq.com
# @File    :APItest1.py
# @Software:PyCharm

import logging.config
import pytest
import requests
import yaml
from requests.exceptions import RequestException

with open("logging.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
#logging.config.fileConfig("logging.yaml")
logger = logging.getLogger("api_test")

def load_test_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        test_data = yaml.safe_load(f)
    return test_data

def send_request(api_base_url, api_path, api_method, api_params=None, api_data=None, api_headers=None, api_timeout=10):
    url = api_base_url + api_path
    params = api_params or {}
    data = api_data or {}
    headers = api_headers or {}
    try:
        response = requests.request(api_method, url, params=params, data=data, headers=headers, timeout=api_timeout)
        response.raise_for_status()
    except RequestException as e:
        logger.exception(f"RequestException: {str(e)}")
        return None
    else:
        return response

def pytest_generate_tests(metafunc):
    if "test_data" in metafunc.fixturenames:
        test_data = load_test_data("data/test_data.yaml")
        metafunc.parametrize("test_data", test_data)

@pytest.mark.usefixtures("api_base_url", "api_headers")
class TestAPI:
    def test_api(self, api_base_url, api_headers, test_data):
        api_path = test_data["api_path"]
        api_method = test_data["api_method"]
        api_params = test_data.get("api_params", None)
        api_data = test_data.get("api_data", None)
        expected_status_code = test_data["expected_status_code"]
        expected_response = test_data.get("expected_response", None)
        response = send_request(api_base_url, api_path, api_method, api_params, api_data, api_headers)
        assert response.status_code == expected_status_code
        if expected_response:
            assert response.json() == expected_response

