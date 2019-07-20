"""Checker tests module."""
from unittest import mock
from unittest.mock import mock_open

import pytest
from koles.checker import KolesChecker


@mock.patch('koles.checker.os.walk')
@mock.patch('koles.checker.os.access')
def test_get_files_to_check(access_mock, walk_mock):
    """Test that the function walks and gather filenames properly."""
    walk_mock.return_value = (
        ('root', ['dir'], ['file1', 'file2']),
        ('root/dir', ['sub_dir'], ['file3']),
        ('root/sub_dir', [], ['file4', 'file5']),
    )
    access_mock.side_effect = 4 * [True] + [False]
    koles_checker = KolesChecker(path="test_path")
    result = [*koles_checker._get_files_to_check()]
    expected_result = [
        'root/file1', 'root/file2', 'root/dir/file3', 'root/sub_dir/file4'
    ]

    assert result == expected_result


@mock.patch('koles.checker.pkg_resources.resource_string')
def test_get_bad_words(resource_string_mock):
    """Test that the function returns set of bad words."""
    resource_string_mock.return_value = b'Mike D\nMCA\nAd-Rock'
    koles_checker = KolesChecker(path="test_path")
    result = koles_checker._get_bad_words()

    assert result == {'MCA', 'Ad-Rock', 'Mike D'}


@pytest.mark.parametrize('pattern, string, expected_result', (

        # Case 1: Multiple overlapping patterns
        (
                '(?=(abcd|ab|abc|cd))',
                'abcdab',
                [0, 2, 4]
        ),

        # Case 2: Single non-overlapping pattern
        (
                '(?=(ab))',
                'abcdab',
                [0, 4]
        ),

        # Case 3: Empty string
        (
                '(?=(ab))',
                '',
                []
        ),

        # Case 3: Empty pattern
        (
                '',
                'abcdab',
                [*range(7)]
        ),

        # Case 4: Empty string and pattern
        (
                '',
                '',
                [0]
        ),
))
def test_check_string(pattern, string, expected_result):
    """Test that check_string returns appropriate value for given pattern and string."""
    koles_checker = KolesChecker(path="test_path")
    koles_checker._pattern = pattern
    result = koles_checker._check_string(string)

    assert [*result] == expected_result


@mock.patch('koles.checker.KolesChecker._check_string')
def test_check_file_content(_check_string_mock):
    """Test that the function returns valid error messages for clean and dirty rows."""
    koles_checker = KolesChecker(path="test_path")
    _check_string_mock.side_effect = [[1, 3], [], [3]]
    read_data = 'Mike D\nMCA\nAd-Rock'

    with mock.patch("builtins.open", mock_open(read_data=read_data)):
        result = koles_checker._check_file_content('test_path')

    expected_result = [
        'test_path:1: Inappropriate vocabulary found at position: [1, 3]',
        'test_path:3: Inappropriate vocabulary found at position: [3]'
    ]

    assert result == expected_result


@pytest.mark.parametrize('_check_string_value, _check_file_content_value, expected_result', (

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
                [1, 3],
                [[]],
                [f'test_path: Filename contains bad language at position: [1, 3]'],

        ),

        # Case 5: Dirty filename, dirty content
        (
                [1, 3],
                [[
                    'test_path:1: Inappropriate vocabulary found at position: [1, 3]',
                    'test_path:3: Inappropriate vocabulary found at position: [3]'
                ]],
                [f'test_path: Filename contains bad language at position: [1, 3]',

                 'test_path:1: Inappropriate vocabulary found at position: [1, 3]',
                 'test_path:3: Inappropriate vocabulary found at position: [3]'

                 ],

        ),

        # Case 6: Dirty filename, UnicodeDecodeError
        (
                [1, 3],
                UnicodeDecodeError('test_codec', b'\x00\x00', 1, 2, 'unicode_decode_error'),
                [
                    f'test_path: Filename contains bad language at position: [1, 3]',
                    'test_path: File couldn\'t have been opened: \'test_codec\' codec '
                    'can\'t decode byte 0x00 in position 1: unicode_decode_error',
                ]

        ),

))
@mock.patch('koles.checker.KolesChecker._check_file_content')
@mock.patch('koles.checker.KolesChecker._check_string')
def test_check_file(
        _check_string_mock,
        _check_file_content_mock,
        _check_string_value,
        _check_file_content_value,
        expected_result
):
    """Test that the function returns appropriate error messages."""
    koles_checker = KolesChecker(path="test_path")
    _check_string_mock.return_value = _check_string_value
    _check_file_content_mock.side_effect = _check_file_content_value

    result = koles_checker._check_file('test_path')

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
        expected_result
):
    """Test that the function return appropriate error messages."""
    koles_checker = KolesChecker(path="test_path")
    _check_file_mock.side_effect = _check_file_mock_value
    _get_files_to_check_mock.return_value = _get_files_to_check_value

    koles_checker._pattern = pattern
    result = koles_checker.check()

    assert result == expected_result
