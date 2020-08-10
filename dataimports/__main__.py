from argparse import ArgumentParser
from dataimports.app import importdata

sources = ['wikidata']
parser = ArgumentParser(description='Scientific Events Importer')
parser.add_argument('-s', '--source',
                    choices=sources,
                    default='wikidata',
                    help="")
parser.add_argument('-l', '--list', action='store_true',
                    help="list available sources")
parser.add_argument('-f', '--format', help="Output format",
                    choices=['wiki', 'dict', 'json'],
                    default='dict')
parser.add_argument('-n', default=None, type=int,
                    help="Limit the number or results by n")
parser.add_argument('-o', '--output',
                    help="Filename for output OR **destination wiki**. "
                         "By default output is printed to console."
                         "Include -o fileme.txt to have file saved to file")
args = parser.parse_args()


if __name__ == '__main__':
    if args.list:
        print('**Source available:**')
        print('\n'.join(sources))
    else:
        importdata(source=args.source,
                   outformat=args.format,
                   outfile=args.output,
                   limit=args.n)
