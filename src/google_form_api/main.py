import asyncio
import re
import json

from aiohttp.client import ClientSession
from aiohttp_proxy import ProxyConnector
import ua_generator


class GoogleFormAPI:
    def __init__(self, proxies: str = None):
        if proxies:
            connector = ProxyConnector.from_url(proxies)

        else:
            connector = None

        user_agent = ua_generator.generate(device='desktop', browser='firefox').text
        self.session = ClientSession(headers={'user-agent': user_agent},
                                     connector=connector)

    async def _get_google_form_fields(self, form_url: str) -> list[dict]:
        result = []
        async with self.session.get(form_url) as response:
            response_text = await response.text()
            json_data = re.search(r'FB_PUBLIC_LOAD_DATA_ = (\[.+\]);', response_text).group(1)

        data = json.loads(json_data)
        fields = data[1][1]
        for field in fields:
            try:
                field_title = field[1]
                field_id = field[4][0][0]

                result.append({"id": field_id,
                               "title": field_title})
            except TypeError:
                pass

        return result

    @staticmethod
    def _generate_payload(fields: list[dict], answers: list[str]) -> dict:
        payload = {}
        for field, answer in zip(fields, answers):
            payload[f"entry.{field['id']}"] = answer
            # print(f"{field['title']}: {answer}")
        return payload

    async def _post_data(self, form_url: str, payload: dict) -> int:
        async with self.session.post(f'{form_url.rsplit("/", 1)[0]}/formResponse', data=payload) as response:
            return response.status

    async def _close_session(self):
        await self.session.close()

    async def submit_form(self, form_url: str, answers: list[str]):
        form_fields = await self._get_google_form_fields(form_url=form_url)
        payload = self._generate_payload(form_fields, answers)
        status = await self._post_data(form_url=form_url,
                                       payload=payload)

        await self._close_session()
        return status
