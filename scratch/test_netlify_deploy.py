import asyncio
import os
import sys
from unittest.mock import AsyncMock, patch, mock_open

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.dynamic_hosting import deploy_to_netlify

async def test_netlify_flow():
    token = "mock_token"
    zip_path = "mock_zip_path"
        
    # We will mock aiohttp.ClientSession post requests
    mock_response_create = AsyncMock()
    mock_response_create.status = 201
    mock_response_create.text = AsyncMock(return_value='{"id": "site_123", "subdomain": "adorable-hamster"}')

    mock_response_deploy = AsyncMock()
    mock_response_deploy.status = 201
    mock_response_deploy.text = AsyncMock(return_value='{"id": "deploy_abc"}')

    class MockSession:
        def __init__(self):
            self.posts = []
            
        async def __aenter__(self):
            return self
            
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

        def post(self, url, headers=None, json=None, data=None, timeout=None):
            self.posts.append((url, headers, json, data))
            mock = AsyncMock()
            if "deploys" in url:
                mock.__aenter__.return_value = mock_response_deploy
            else:
                mock.__aenter__.return_value = mock_response_create
            return mock

    mock_session = MockSession()

    with patch("aiohttp.ClientSession", return_value=mock_session):
        with patch("builtins.open", mock_open(read_data=b"dummy_zip_content")):
            url = await deploy_to_netlify(zip_path, token)
            
            # Check returned URL
            assert url == "https://adorable-hamster.netlify.app", f"Expected URL mismatch: {url}"
            
            # Check calls
            assert len(mock_session.posts) == 2, f"Expected 2 POST requests, got {len(mock_session.posts)}"
            
            # First post (Create Site)
            url1, headers1, json1, data1 = mock_session.posts[0]
            assert url1 == "https://api.netlify.com/api/v1/sites"
            assert headers1["Content-Type"] == "application/json"
            assert json1 == {}
            
            # Second post (Deploy)
            url2, headers2, json2, data2 = mock_session.posts[1]
            assert url2 == "https://api.netlify.com/api/v1/sites/site_123/deploys"
            assert headers2["Content-Type"] == "application/zip"
            assert data2 == b"dummy_zip_content"
            
            print("[OK] Netlify two-step deploy mock test passed successfully!")

if __name__ == "__main__":
    asyncio.run(test_netlify_flow())
