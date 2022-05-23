from datetime import datetime
from typing import List
import pytest


@pytest.fixture()
def posts_database_data() -> List:
    return [{'id': '0',
             'title': 'This is the first post',
             'author': 'danodic',
             'timestamp': datetime(2022, 2, 22, 12, 22, 22, 222222),
             'body': 'This is a sample post.'},
            {'id': '1',
             'title': 'This is the second post',
             'author': 'beutrano',
             'timestamp': datetime(2022, 2, 22, 11, 22, 22, 222222),
             'body': 'This is a sample post.'},
            {'id': '2',
             'title': 'This is the third post',
             'author': 'danodic',
             'timestamp': datetime(2022, 2, 22, 10, 22, 22, 222222),
             'body': 'This is a sample post.'},
            {'id': '3',
             'title': 'This is the fourth post',
             'author': 'danodic',
             'timestamp': datetime(2022, 2, 22, 9, 22, 22, 222222),
             'body': 'This is a sample post.'},
            {'id': '4',
             'title': 'This is the fifth post',
             'author': 'danodic',
             'timestamp': datetime(2022, 2, 22, 8, 22, 22, 222222),
             'body': 'This is a sample post.'},
            {'id': '5',
             'title': 'This is the sixth post',
             'author': 'danodic',
             'timestamp': datetime(2022, 2, 22, 7, 22, 22, 222222),
             'body': 'This is a sample post.'},
            {'id': '6',
             'title': 'This is the seventh post',
             'author': 'danodic',
             'timestamp': datetime(2022, 2, 22, 6, 22, 22, 222222),
             'body': 'This is a sample post.'},
            {'id': '7',
             'title': 'This is the eightieth post',
             'author': 'danodic',
             'timestamp': datetime(2022, 2, 22, 5, 22, 22, 222222),
             'body': 'This is a sample post.'},
            {'id': '8',
             'title': 'This is the ninetieth post',
             'author': 'danodic',
             'timestamp': datetime(2022, 2, 22, 4, 22, 22, 222222),
             'body': 'This is a sample post.'},
            {'id': '9',
             'title': 'This is the tenth post',
             'author': 'danodic',
             'timestamp': datetime(2022, 2, 22, 3, 22, 22, 222222),
             'body': 'This is a sample post.'}]