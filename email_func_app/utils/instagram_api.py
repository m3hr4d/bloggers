"""Instagram API utilities for profile data retrieval using RapidAPI."""
import os
import logging
import requests
import time
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class InstagramAPI:
    """Instagram API wrapper using RapidAPI."""
    
    # RapidAPI configuration
    RAPIDAPI_KEY = "704c292ac7msh9e38b1a7a9fd2a7p1b2effjsna8756d78b10d"
    RAPIDAPI_HOST = "instagram-scraper-2022.p.rapidapi.com"
    BASE_URL = "https://instagram-scraper-2022.p.rapidapi.com"
    
    @classmethod
    def _make_request(cls, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """
        Make a request to the RapidAPI endpoint with rate limiting.
        
        Args:
            endpoint (str): API endpoint
            params (dict): Query parameters
            
        Returns:
            dict: Response data or None if failed
        """
        headers = {
            "X-RapidAPI-Key": cls.RAPIDAPI_KEY,
            "X-RapidAPI-Host": cls.RAPIDAPI_HOST
        }
        
        try:
            # Add delay to respect rate limits
            time.sleep(1)
            
            response = requests.get(
                f"{cls.BASE_URL}/{endpoint}",
                headers=headers,
                params=params,
                timeout=10
            )
            
            # Check if we hit rate limit
            if response.status_code == 429:
                logger.warning("Rate limit hit, waiting 60 seconds...")
                time.sleep(60)
                # Retry the request
                response = requests.get(
                    f"{cls.BASE_URL}/{endpoint}",
                    headers=headers,
                    params=params,
                    timeout=10
                )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request error: {str(e)}")
            return None
    
    @classmethod
    def get_profile_info_from_username(cls, username: str) -> Optional[Dict[str, Any]]:
        """
        Get Instagram profile information using RapidAPI.
        
        Args:
            username (str): Instagram username (with or without @)
            
        Returns:
            dict: Profile information or None if failed
        """
        username = username.strip('@').strip('/')
        logger.info(f"Fetching profile info for {username}")
        
        try:
            # Make API request
            data = cls._make_request(f"instagram/user/details", {"username": username})
            if not data:
                return None
            
            # Extract user data
            user_data = data.get('data', {})
            if not user_data:
                logger.error("No user data found in API response")
                return None
            
            # Format response
            return {
                'username': user_data.get('username'),
                'full_name': user_data.get('full_name'),
                'biography': user_data.get('biography'),
                'followers_count': user_data.get('followers'),
                'following_count': user_data.get('following'),
                'profile_picture_url': user_data.get('profile_pic_url'),
                'is_verified': user_data.get('is_verified', False),
                'external_url': user_data.get('external_url'),
                'business_category': user_data.get('category'),
                'is_business_account': user_data.get('is_business', False),
                'posts_count': user_data.get('posts'),
                'is_private': user_data.get('is_private', False)
            }
            
        except Exception as e:
            logger.error(f"Error fetching Instagram profile: {str(e)}")
            return None
    
    @classmethod
    def download_profile_picture(cls, username: str) -> Optional[bytes]:
        """
        Download profile picture for a given username.
        
        Args:
            username (str): Instagram username
            
        Returns:
            bytes: Profile picture data or None if failed
        """
        try:
            # First get profile info to get the picture URL
            profile_info = cls.get_profile_info_from_username(username)
            if not profile_info or not profile_info.get('profile_picture_url'):
                return None
            
            # Download the profile picture
            response = requests.get(
                profile_info['profile_picture_url'],
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
                },
                timeout=10
            )
            response.raise_for_status()
            return response.content
            
        except Exception as e:
            logger.error(f"Error downloading profile picture: {str(e)}")
            return None
    
    @classmethod
    def get_hashtag_info(cls, hashtag: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a hashtag using RapidAPI.
        
        Args:
            hashtag (str): Instagram hashtag (with or without #)
            
        Returns:
            dict: Hashtag information or None if failed
        """
        hashtag = hashtag.strip('#')
        logger.info(f"Fetching hashtag info for #{hashtag}")
        
        try:
            # Make API request
            data = cls._make_request("instagram/hashtag/details", {"hashtag": hashtag})
            if not data:
                return None
            
            # Extract hashtag data
            hashtag_data = data.get('data', {})
            if not hashtag_data:
                logger.error("No hashtag data found in API response")
                return None
            
            # Format response
            return {
                'name': hashtag_data.get('name'),
                'media_count': hashtag_data.get('media_count'),
                'search_result_subtitle': hashtag_data.get('search_result_subtitle'),
                'allow_following': hashtag_data.get('allow_following'),
                'is_following': hashtag_data.get('is_following'),
                'is_top_media_only': hashtag_data.get('is_top_media_only')
            }
            
        except Exception as e:
            logger.error(f"Error fetching hashtag info: {str(e)}")
            return None
