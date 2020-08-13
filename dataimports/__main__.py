from argparse import ArgumentParser, RawTextHelpFormatter
from dataimports.app import importdata
from dataimports.file_utils import wikidetails_present
from dataimports.globals import Colors

sources = ['wikidata']
parser = ArgumentParser(description=f"""{Colors.OKBLUE}
                   ///
                  (. .)
--------------o00--( )--00o--
{Colors.FAIL} confIDent Data Importer {Colors.OKBLUE}
-----------------------------{Colors.ENDC}""",
                        formatter_class=RawTextHelpFormatter)
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
parser.add_argument('-w', '--write', action='store_true',
                    help="writes the output to wiki or file. "
                         "Default: False (dry-run).")
parser.add_argument('-o', '--output',
                    help="Filename for output or destination wiki."
                         "Include -o fileme.txt to have file saved to file")
args = parser.parse_args()


if __name__ == '__main__':
    if args.list:
        print(args)
        print('**Source available:**')
        print('\n'.join(sources))
    else:
        if args.write and args.format == 'wiki':
            wikidetails_present()
        importdata(source=args.source,
                   outformat=args.format,
                   outfile=args.output,
                   limit=args.n,
                   write=args.write)
