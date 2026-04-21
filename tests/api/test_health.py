import os

import pytest

from framework.api.assertions import assert_status


@pytest.mark.api
def test_health(api_client):
    if os.getenv("RUN_LIVE_TESTS") != "1":
        pytest.skip("Set RUN_LIVE_TESTS=1 to run against a real environment")

    resp = api_client.get("/health")
    assert_status(resp, 200)

