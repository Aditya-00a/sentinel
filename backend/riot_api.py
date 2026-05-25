import os
import logging
import httpx
from backend.db import cache_get, cache_set

logger = logging.getLogger("sentinel.riot_api")

RIOT_API_KEY = os.environ.get("RIOT_API_KEY", "")

PLATFORM_TO_CLUSTER = {
    "na1": "americas", "br1": "americas", "la1": "americas", "la2": "americas",
    "euw1": "europe", "eun1": "europe", "tr1": "europe", "ru": "europe",
    "kr": "asia", "jp1": "asia",
    "oc1": "americas", "ph2": "asia", "sg2": "asia", "th2": "asia", "tw2": "asia", "vn2": "asia",
}

CLUSTER_HOSTS = {
    "americas": "https://americas.api.riotgames.com",
    "europe": "https://europe.api.riotgames.com",
    "asia": "https://asia.api.riotgames.com",
}

PLATFORM_HOSTS = {
    "na1": "https://na1.api.riotgames.com",
    "euw1": "https://euw1.api.riotgames.com",
    "eun1": "https://eun1.api.riotgames.com",
    "kr": "https://kr.api.riotgames.com",
    "jp1": "https://jp1.api.riotgames.com",
    "br1": "https://br1.api.riotgames.com",
    "la1": "https://la1.api.riotgames.com",
    "la2": "https://la2.api.riotgames.com",
    "oc1": "https://oc1.api.riotgames.com",
    "tr1": "https://tr1.api.riotgames.com",
    "ru": "https://ru.api.riotgames.com",
}


class RiotAPIError(Exception):
    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message
        super().__init__(f"Riot API {status}: {message}")


async def _request(url: str, cache_endpoint: str, cache_key: str) -> dict | None:
    cached = cache_get(cache_endpoint, cache_key)
    if cached:
        logger.info(f"Cache hit: {cache_endpoint}/{cache_key} (age {cached['age_seconds']:.0f}s)")
        return cached["data"]

    if not RIOT_API_KEY:
        logger.warning("No RIOT_API_KEY set, skipping live request")
        return None

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, headers={"X-Riot-Token": RIOT_API_KEY})
            logger.info(f"Riot API {resp.status_code}: {cache_endpoint}/{cache_key}")

            if resp.status_code == 200:
                data = resp.json()
                cache_set(cache_endpoint, cache_key, data)
                return data
            elif resp.status_code in (401, 403):
                logger.error(f"Riot API auth error: {resp.status_code}")
                return None
            elif resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After", "unknown")
                logger.warning(f"Rate limited, Retry-After: {retry_after}")
                return None
            elif resp.status_code == 404:
                logger.info("Player/match not found")
                return None
            else:
                logger.error(f"Unexpected status {resp.status_code}: {resp.text[:200]}")
                return None
    except httpx.TimeoutException:
        logger.error(f"Timeout calling Riot API: {url}")
        return None
    except Exception as e:
        logger.error(f"Riot API error: {e}")
        return None


async def get_account_by_riot_id(game_name: str, tag_line: str, region: str = "americas") -> dict | None:
    host = CLUSTER_HOSTS.get(region, CLUSTER_HOSTS["americas"])
    url = f"{host}/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    return await _request(url, "account_by_riot_id", f"{game_name}#{tag_line}@{region}")


async def get_summoner_by_puuid(puuid: str, platform: str = "na1") -> dict | None:
    host = PLATFORM_HOSTS.get(platform, PLATFORM_HOSTS["na1"])
    url = f"{host}/lol/summoner/v4/summoners/by-puuid/{puuid}"
    return await _request(url, "summoner_by_puuid", f"{puuid}@{platform}")


async def get_league_entries(summoner_id: str, platform: str = "na1") -> list | None:
    host = PLATFORM_HOSTS.get(platform, PLATFORM_HOSTS["na1"])
    url = f"{host}/lol/league/v4/entries/by-summoner/{summoner_id}"
    return await _request(url, "league_entries", f"{summoner_id}@{platform}")


async def get_match_ids_lol(puuid: str, platform: str = "na1", count: int = 10) -> list | None:
    cluster = PLATFORM_TO_CLUSTER.get(platform, "americas")
    host = CLUSTER_HOSTS[cluster]
    url = f"{host}/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}"
    return await _request(url, "match_ids_lol", f"{puuid}@{cluster}:{count}")


async def get_match_detail_lol(match_id: str, platform: str = "na1") -> dict | None:
    cluster = PLATFORM_TO_CLUSTER.get(platform, "americas")
    host = CLUSTER_HOSTS[cluster]
    url = f"{host}/lol/match/v5/matches/{match_id}"
    return await _request(url, "match_detail_lol", match_id)


async def get_match_ids_val(puuid: str, region: str = "americas") -> list | None:
    host = CLUSTER_HOSTS.get(region, CLUSTER_HOSTS["americas"])
    url = f"{host}/val/match/v1/matchlists/by-puuid/{puuid}"
    result = await _request(url, "match_ids_val", f"{puuid}@{region}")
    if result and "history" in result:
        return [m["matchId"] for m in result["history"][:10]]
    return result


async def get_match_detail_val(match_id: str, region: str = "americas") -> dict | None:
    host = CLUSTER_HOSTS.get(region, CLUSTER_HOSTS["americas"])
    url = f"{host}/val/match/v1/matches/{match_id}"
    return await _request(url, "match_detail_val", match_id)


async def check_api_health() -> bool:
    if not RIOT_API_KEY:
        return False
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(
                "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/test/test",
                headers={"X-Riot-Token": RIOT_API_KEY},
            )
            return resp.status_code in (200, 404)
    except Exception:
        return False
