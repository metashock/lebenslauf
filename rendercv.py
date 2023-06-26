#!/usr/bin/env python3
import argparse
import datetime
import jinja2
import os
import yaml


class MissingTranslationError(Exception):
    ''' Raise when a translation is missing '''
    def __init__(self, missing_key):
        super().__init__(missing_key)
        self.missing_key = missing_key


def create_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', default='en')
    default_details = \
        True if os.environ.get('cv_details', 'n') == 'y' else False
    parser.add_argument(
        '--details',
        action='store_true',
        default=default_details,)
    return parser


def translations(lang):
    filename = 'translations/translations.' + lang + '.txt'
    lookup = {}
    with open(filename) as fd:
        for line in fd:
            key, value = line.strip().split('@@@')
            lookup[key] = value
    def translate(key):
        try:
            return lookup[key]
        except KeyError:
            raise MissingTranslationError(key)
    return translate

def date_formatter(lang):
    def format_date(year, month, day):
        if lang == 'en':
            return f'{year}/{month}/{day}'
        elif lang == 'de':
            return f'{day}.{month}.{year}'
    return format_date 


def create_template_env(translation_func, format_date):
    loader = jinja2.FileSystemLoader(
        searchpath='./templates',
    )
    env =jinja2.Environment(
        loader=loader,
        block_start_string='[%',
        block_end_string='%]',
        variable_start_string='[[',
        variable_end_string=']]',
    )
    env.globals['translate'] = translation_func
    env.globals['format_date'] = format_date
    return env


def load_datasource(datasource_name, data_directory_name='data'):
    with open(os.path.join(data_directory_name, datasource_name + '.yml')) as fd:
        return yaml.safe_load(fd)


def main():
    args = create_argparser().parse_args()
    env = create_template_env(
        translations(args.lang),
        date_formatter(args.lang),)
    
    try:
        tpl = env.get_template('cv.moderncv.tex.j2')
        output = tpl.render(
            data=load_datasource('cv.' + args.lang),
            print_details=args.details,)
        print(output)
    except jinja2.exceptions.TemplateSyntaxError as e:
        print(
            'TemplateSyntaxError',
            str(e.filename) + ':' + str(e.lineno),
            e.source.splitlines()[e.lineno],
        )
    except MissingTranslationError as e:
        print(
            f'Translation for "{e.missing_key}" is missing '
            f'for language {args.lang}'
        )


if __name__ == '__main__':
    main()
