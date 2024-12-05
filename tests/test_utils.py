from unittest.mock import patch

import pytest

from src.utils import read_greeting


@pytest.mark.parametrize('hour, expected', [(6, 'Доброе утро'),
                                            (15, 'Добрый день'),
                                            (21, 'Добрый вечер'),
                                            (24, 'Доброй ночи'),
                                            ])
def test_read_greeting(hour, expected):
    with patch('src.utils.datetime') as mock_datetime:
        mock_datetime.now.return_value.hour = hour
        assert read_greeting() == expected
