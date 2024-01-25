import asyncio
import json
import random

import aiohttp as aiohttp
import yarl
from faker import Faker

with open('bot_settings.json') as f:
    data = json.load(f)

number_of_users = data['number_of_users']
max_posts_per_user = data['max_posts_per_user']
max_likes_per_user = data['max_likes_per_user']

short_texts = [
    "Embrace the glorious mess that you are.",
    "Create your sunshine.",
    "Life is short. Smile while you still have teeth.",
    "Chase your dreams in high heels, of course!",
    "Happiness is not by chance but by choice.",
    "Stay positive, work hard, and make it happen.",
    "Be a voice, not an echo.",
    "Good vibes only.",
    "Dream big, work hard, stay focused.",
    "Believe in your #selfie.",
    "Live in the sunshine, swim in the sea, drink the wild air.",
    "Be a flamingo in a flock of pigeons.",
    "Do it with passion or not at all.",
    "Stay true to you.",
    "Coffee and kindness.",
]


def create_user():
    faker = Faker()
    user = {
        "username": faker.profile(fields=['username'])['username'],
        "password": faker.password()
    }
    return user


async def sign_up():
    user = create_user()

    async with aiohttp.ClientSession() as session:
        async with session.post('http://127.0.0.1:8000/sign_up', json=user) as resp:
            if resp.ok:
                return user
            else:
                await sign_up()


async def login(payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(
                yarl.URL(f"http://127.0.0.1:8000/login/?username={payload['username']}&password={payload['password']}",
                         encoded=True)) as resp:
            if resp.ok:
                resp_json = await resp.json()
                return resp_json['access_token']


async def create_post(user):
    headers = {"Authorization": f"Bearer {user['access_token']}"}
    payload = {"text": random.choice(short_texts)}
    async with aiohttp.ClientSession() as session:
        async with session.post('http://127.0.0.1:8000/post', headers=headers, json=payload) as resp:
            if resp.ok:
                resp_json = await resp.json()
                return resp_json['id']


async def like_post(user, post_id):
    headers = {"Authorization": f"Bearer {user['access_token']}"}
    async with aiohttp.ClientSession() as session:
        async with session.post(f'http://127.0.0.1:8000/like?post_id={post_id}', headers=headers) as resp:
            if resp.ok:
                return True
            else:
                return False


async def user_action(user):
    user['access_token'] = await login(user)
    post_ids = []
    for post_num in range(max_posts_per_user):
        post = await create_post(user)
        post_ids.append(post)
    liked_posts = []
    for like_number in range(max_likes_per_user):
        random_post = random.choice(post_ids)
        like_result = await like_post(user, random_post)
        if like_result:
            post_ids.remove(random_post)
            liked_posts.append(random_post)


async def main():
    users = []
    for k in range(number_of_users):
        signed_user = await sign_up()
        users.append(signed_user)
    coroutines = list(map(lambda user: user_action(user), users))
    await asyncio.gather(*coroutines)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
