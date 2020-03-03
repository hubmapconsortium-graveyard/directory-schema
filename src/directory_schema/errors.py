from yaml import dump as dump_yaml


def _to_dir_listing(dir_as_list, indent=''):
    next_indent = indent + '    '
    return ''.join([
        '\n' + indent + item['name']
        + _to_dir_listing(
            item['contents'] if 'contents' in item else [],
            next_indent
        )
        for item in dir_as_list
    ])


def _validation_error_to_string(error, indent):
    schema_string = ''.join([
        f'\n{indent}{line}' for line in
        dump_yaml(error.schema[error.validator]).split('\n')
    ])

    fail_message = f'''

fails this "{error.validator}" check:
{schema_string}
    '''

    error_type = type(error.instance)

    if error_type == str:
        return f'''This string:
{indent}{error.instance}{fail_message}
        '''

    if error_type == dict:
        return f'''This item:
{_to_dir_listing([error.instance], indent)}{fail_message}
        '''

    if error_type == list:
        return f'''This directory:
{_to_dir_listing(error.instance, indent)}{fail_message}
        '''

    raise Exception(f'Unrecognized type "{error_type}"')


class DirectoryValidationErrors(Exception):
    def __init__(self, errors):
        self.json_validation_errors = errors

    def __str__(self):
        return '\n'.join([
            _validation_error_to_string(e, '    ')
            for e in self.json_validation_errors
        ])

    def _repr__(self):
        return self.json_validation_error.__repr__()
