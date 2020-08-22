#
#   This file is part of jcm-pagination.
#
#   Copyright © 2020 Guillaume Jacquemin <williamjcm@users.noreply.github.com>
#
#   Permission is hereby granted, free of charge, to any person obtaining a
#   copy of this software and associated documentation files (the "Software"),
#   to deal in the Software without restriction, including without limitation
#   the rights to use, copy, modify, merge, publish, distribute, sublicense,
#   and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included
#   in all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#   THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.
#

from docutils.parsers import rst
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from docutils import nodes

class Pagination(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {'page_number': directives.unchanged_required,
                   'total_pages': directives.unchanged_required,
                   'previous_text': directives.unchanged,
                   'next_text': directives.unchanged,
                   'style': directives.unchanged}
    has_content = False

    def run(self):
        container = nodes.container()
        container['classes'].append('m-article-pagination')

        base_url = self.arguments[0]
        url_format_string = base_url + "/{}/"

        page_number = int(self.options['page_number'].strip())
        if page_number < 1:
            return None

        total_pages = int(self.options['total_pages'].strip())
        if total_pages < 1:
            return None

        if 'previous_text' in self.options:
            previous_text = self.options['previous_text']
        else:
            previous_text = 'previous'

        if 'next_text' in self.options:
            next_text = self.options['next_text']
        else:
            next_text = 'next'

        if 'style' in self.options:
            style = self.options['style'] if self.options['style'] in ['default', 'x_out_of_y', 'mcss'] else 'default'
        else:
            style = 'default'

        if page_number == 1:
            if style != 'mcss':
                container.append(nodes.inline(text="« {}".format(previous_text)))
        else:
            container.append(nodes.reference(text="« {}".format(previous_text),
                                             refuri=(base_url if page_number == 2 else url_format_string.format(page_number - 1))))

        if style != 'mcss' or page_number != 1:
            container.append(nodes.inline(text=' | '))

        if style == 'default':
            for i in range(1, total_pages + 1):
                if i == page_number:
                    container.append(nodes.inline(text="{}".format(i)))
                else:
                    container.append(nodes.reference(text="{}".format(i),
                                                     refuri=(base_url if i == 1 else url_format_string.format(i))))
                container.append(nodes.inline(text=' | '))
        else:
            container.append(nodes.inline(text="page {}{}".format(page_number, " out of {}".format(total_pages) if style == 'x_out_of_y' else '')))

            if style != 'mcss' or page_number != total_pages:
                container.append(nodes.inline(text=' | '))

        if page_number == total_pages:
            if style != 'mcss':
                container.append(nodes.inline(text="{} »".format(next_text)))
        else:
            container.append(nodes.reference(text="{} »".format(next_text),
                                             refuri=url_format_string.format(page_number + 1)))

        return [container]

def register():
    rst.directives.register_directive('jcm-pagination', Pagination)
