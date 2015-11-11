"""
Main entry point
"""

import argparse
from rdfconv.converter import RDFtoHTMLConverter, LanguageError
import pyinotify


class EventHandler(pyinotify.ProcessEvent):
    def __init__(self, output_folder, languages):
        super(EventHandler, self).__init__()
        self.output_folder = output_folder
        self.languages = languages

    def process_default(self, event):
        run(event.path, self.output_folder, self.languages)


def run(input_file, output_folder, languages='all'):
    """
    Run the RDF converter
    """
    try:
        rdf_conv = RDFtoHTMLConverter(languages)
        rdf_conv.load_file(input_file)
        rdf_conv.output_html(output_folder)
    except LanguageError as err:
        print 'Skipped file %s due to error:\n%s' % (input_file, err)


def watch(input_files, output_folder, languages='all'):
    handler = EventHandler(output_folder, languages)
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, handler)
    for input_file in input_files:
        wm.add_watch(input_file, pyinotify.IN_MODIFY)
    notifier.loop()


def main():
    # Handle arguments
    parser = argparse.ArgumentParser(description='RDF to HTML converter.')
    parser.add_argument('dcat_files', metavar='DCAT_FILE', type=str, nargs='+',
                        help='DCAT file')
    parser.add_argument('output', metavar='OUTPUT_DIR', type=str,
                        help='Output directory')
    parser.add_argument('--languages', type=str, default='all',
                        help='Languages to generate separated by comma (,). '
                             'If omitted all encountered languages are '
                             'generated.')
    parser.add_argument('--watch', action='store_true', help='Watch input '
                        'files for changes and run the conversion whan a '
                        'change occurs.')

    args = parser.parse_args()

    langs = args.languages.split(',')

    if args.watch:
        watch(args.dcat_files, args.output, langs)
    else:
        for dcat_file in args.dcat_files:
            run(dcat_file, args.output, langs)


if __name__ == '__main__':
    main()