"""Checker tests module."""
from unittest import mock
from unittest.mock import mock_open

import pytest
from koles.checker import KolesChecker


@mock.patch('koles.checker.os.walk')
@mock.patch('koles.checker.os.access')
def test_get_files_to_check(access_mock, walk_mock, koles_checker_fixture):
    """Test that the function walks and gather filenames properly."""
    walk_mock.return_value = (
        ('root', ['dir'], ['file1', 'file2']),
        ('root/dir', ['sub_dir'], ['file3']),
        ('root/sub_dir', [], ['file4', 'file5']),
    )
    access_mock.side_effect = 4 * [True] + [False]
    result = [*koles_checker_fixture._get_files_to_check()]
    expected_result = [
        'root/file1', 'root/file2', 'root/dir/file3', 'root/sub_dir/file4'
    ]

    assert result == expected_result


@mock.patch('koles.checker.pkg_resources.resource_string')
def test_get_bad_words(resource_string_mock, koles_checker_fixture):
    """Test that the function returns set of bad words."""
    resource_string_mock.return_value = b'Mike D\nMCA\nAd-Rock'
    result = koles_checker_fixture._get_bad_words()

    assert result == {'MCA', 'Ad-Rock', 'Mike D'}


@pytest.mark.parametrize('pattern, string, expected_result', (

        # Case 1: Multiple overlapping patterns
        (
                'abcd|ab|abc|cd',
                'abcdab',
                [(0, 'abcd'), (2, 'cd'), (4, 'ab')]
        ),

        # Case 2: Single non-overlapping pattern
        (
                'ab',
                'abcdab',
                [(0, 'ab'), (4, 'ab')]
        ),

        # Case 3: Empty string
        (
                '(?=(ab))',
                '',
                []
        ),

        # Case 4: Empty pattern
        (
                '',
                'abcdab',
                []
        ),

        # Case 6: Empty string and pattern
        (
                '',
                '',
                []
        ),

        # Case 7: Uppercase string
        (
                'abcd|ab|abc|cd',
                'ABCDAB',
                [(0, 'ABCD'), (2, 'CD'), (4, 'AB')]
        ),
))
def test_check_row(pattern, string, expected_result, koles_checker_fixture):
    """Test that check_string returns appropriate value for given pattern and string."""
    koles_checker_fixture._pattern = pattern
    result = koles_checker_fixture._check_row(string)

    assert [*result] == expected_result


@mock.patch('koles.checker.KolesChecker._check_row')
def test_check_file_content(_check_row_mock, koles_checker_fixture):
    """Test that the function returns valid error messages for clean and dirty rows."""
    _check_row_mock.side_effect = [[(1, 'Mike D'), (3, 'MCA')], [], [(3, 'MCA')]]
    read_data = 'Mike D\nMCA\nAd-Rock'

    with mock.patch("builtins.open", mock_open(read_data=read_data)):
        result = koles_checker_fixture._check_file_content('test_path')

    expected_result = [
        'test_path:1: Inappropriate vocabulary found: 1: M*****, 3: M**',
        'test_path:3: Inappropriate vocabulary found: 3: M**'
    ]

    assert result == expected_result


@pytest.mark.parametrize('_check_row_value, _check_file_content_value, expected_result', (

        # Case 1: Clean filename, clean content
        (
                [],
                [[]],
                []
        ),

        # Case 2: Clean filename, dirty content
        (
                [],
                [[
                    'test_path:1: Inappropriate vocabulary found at position: [1, 3]',
                    'test_path:3: Inappropriate vocabulary found at position: [3]'
                ]],
                [
                    'test_path:1: Inappropriate vocabulary found at position: [1, 3]',
                    'test_path:3: Inappropriate vocabulary found at position: [3]'
                ]
        ),

        # Case 3: Clean filename, UnicodeDecodeError
        (
                [],
                UnicodeDecodeError('test_codec', b'\x00\x00', 1, 2, 'unicode_decode_error'),
                [
                    'test_path: File couldn\'t have been opened: \'test_codec\' codec '
                    'can\'t decode byte 0x00 in position 1: unicode_decode_error'
                ]
        ),

        # Case 4: Dirty filename, clean content
        (
                [(1, 'Mike D'), (3, 'Ad-Rock')],
                [[]],
                [f'test_path: Filename contains bad language: 1: M*****, 3: A******'],
        ),

        # Case 5: Dirty filename, dirty content
        (
                [(1, 'Ad-Rock'), (3, 'MCA')],
                [[
                    'test_path:1: Inappropriate vocabulary found: 6: B***********',
                    'test_path:3: Inappropriate vocabulary found: 6: M**'
                ]],
                [
                    'test_path: Filename contains bad language: 1: A******, 3: M**',
                    'test_path:1: Inappropriate vocabulary found: 6: B***********',
                    'test_path:3: Inappropriate vocabulary found: 6: M**'
                ],

        ),

        # Case 6: Dirty filename, UnicodeDecodeError
        (
                [(1, 'Mike D'), (3, 'MCA')],
                UnicodeDecodeError('test_codec', b'\x00\x00', 1, 2, 'unicode_decode_error'),
                [
                    f'test_path: Filename contains bad language: 1: M*****, 3: M**',
                    'test_path: File couldn\'t have been opened: \'test_codec\' codec '
                    'can\'t decode byte 0x00 in position 1: unicode_decode_error',
                ]

        ),

))
@mock.patch('koles.checker.KolesChecker._check_file_content')
@mock.patch('koles.checker.KolesChecker._check_row')
def test_check_file(
        _check_row_mock,
        _check_file_content_mock,
        _check_row_value,
        _check_file_content_value,
        expected_result,
        koles_checker_fixture
):
    """Test that the function returns appropriate error messages."""
    _check_row_mock.return_value = _check_row_value
    _check_file_content_mock.side_effect = _check_file_content_value

    result = koles_checker_fixture._check_file('test_path')

    assert result == expected_result


@pytest.mark.parametrize('pattern, _check_file_mock_value, _get_files_to_check_value, expected_result', (

        # Case 1: Pattern is not present
        (
                None,
                [],
                [],
                ''
        ),

        # Case 2: Pattern is present, no files to check
        (
                r'+w',
                [],
                [],
                ''
        ),

        # Case 3: Pattern is present, available files to check
        (
                r'+w',
                [
                    [
                        'test_path/file1:1: Inappropriate vocabulary found at position: [1, 3]',
                    ],
                    [],
                    ['test_path/file3:1: Inappropriate vocabulary found at position: [1, 3]'],

                ],
                ['file1', 'file2', 'file3'],
                (
                        'test_path/file1:1: Inappropriate vocabulary found at position: [1, 3]\n'
                        'test_path/file3:1: Inappropriate vocabulary found at position: [1, 3]'
                )

        ),

))
@mock.patch('koles.checker.KolesChecker._get_files_to_check')
@mock.patch('koles.checker.KolesChecker._check_file')
def test_check(
        _check_file_mock,
        _get_files_to_check_mock,
        pattern,
        _check_file_mock_value,
        _get_files_to_check_value,
        expected_result,
        koles_checker_fixture
):
    """Test that the function return appropriate error messages."""
    _check_file_mock.side_effect = _check_file_mock_value
    _get_files_to_check_mock.return_value = _get_files_to_check_value

    koles_checker_fixture._pattern = pattern
    result = koles_checker_fixture.check()

    assert result == expected_result
