import asyncio

import aiohttp
import bs4


global loop


async def get_html(site_url: str) -> str:

    url = f'https://{site_url}/'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()

            return await resp.text()


def get_title(html: str, site_url: str) -> str:
    print(f'Getting TITLE for {site_url}', flush=True)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    header = soup.title
    if not header:
        return 'MISSING'

    return header.text.strip()


def main():
    asyncio.run(get_title_range())


async def get_title_range():
    file = open('news_sites.txt', 'r')
    tasks = []

    while True:
        n = file.readline()
        if not n:
            break
        tasks.append((n.strip(), asyncio.get_event_loop().create_task(get_html(n.strip()))))

    for n, t in tasks:
        html = await t
        title = get_title(html, n)
        print(f'{n} - {title}', flush=True)
        print('-' * 20)


    file.close()

if __name__ == '__main__':
    main()


