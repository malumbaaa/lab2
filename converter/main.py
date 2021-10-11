import argparse
from converter.converter import convert, ParsersEnum
from parsers.serializer_creator.json_serializer_creator import JsonSerializerCreator

formats = ['json', 'yaml', 'toml', 'pickle']


def create_parser():
    parser = argparse.ArgumentParser(
        prog='wtf_converter',
        usage='%(prog)s [A | [file_to_convert & original_format & target_format | file_to_save]]'
    )

    parser.add_argument('-cfg', '--config', type=argparse.FileType('r', encoding='UTF-8'),
                        help='JSON text configuration file')
    parser.add_argument('-of', '--original_format', choices=formats)
    parser.add_argument('-tf', '--target_format', choices=formats)
    parser.add_argument('-ftc', '--file_to_convert', type=str)
    parser.add_argument('-fts', '--file_to_save', type=str)

    return parser


def parse_config(fp):
    parser = JsonSerializerCreator().create_serializer()
    cfg = parser.load(fp)
    try:
        original_format = getattr(ParsersEnum, cfg['original_format'].upper())
        target_format = getattr(ParsersEnum, cfg['target_format'].upper())
        file_to_convert = cfg['file_to_convert']
        if 'file_to_save' in cfg:
            file_to_save = cfg['file_to_save']
        else:
            file_to_save = None
    except Exception:
        raise Exception('incorrect config')
    return original_format, target_format, file_to_convert, file_to_save


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.config is not None:
        cfg = parse_config(args.config)
        convert(*cfg)
    elif args.original_format and args.target_format and args.file_to_convert is not None:
        deserializer = getattr(ParsersEnum, args.original_format.upper())
        serializer = getattr(ParsersEnum, args.target_format.upper())
        convert(deserializer, serializer, args.file_to_convert, args.file_to_save)
    else:
        parser.error('parameters --format and --file_to_convert are required together')


if __name__ == '__main__':
    main()
