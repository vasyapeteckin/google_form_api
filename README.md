# Google Form API

Asynchronous Module for filling Google Forms


# Installing

```bash
pip3 install google-form-api
```

# Basic usage

```python
import asyncio
from google_form_api import GoogleFormAPI


async def main():
    form_url = 'https://docs.google.com/forms/d/1oOREz1PyClCprACHfXcjs5OrMHJLz38B2HTuv13oFqs/viewform'

    # proxy supported formats: http, https, socks4, socks5
    proxy = 'socks5://login:password@host:port'

    # Answer the questions in order as in the form
    answers = ['@vasyapeteckin',
               'https://twitter.com/vasyapeteckin/status/1652222718539108353',
               '',  # Optional fields can be left blank
               'GL7Q77exFUi8SVtXeZmL5V7VjF9ahm9Bz1fxkLtxsf44']

    status_code = await GoogleFormAPI(proxies=proxy).submit_form(form_url=form_url,
                                                                 answers=answers)
    print(status_code)

asyncio.run(main())

```
