# -*- coding: utf-8 -*-

"""
Script to transalte from MediaWiki to Atlassian Confluence format.

Usage:
  $ python translator.py WikiPageTitle
"""

import sys
import urllib

from mwlib.dummydb import DummyDB
from mwlib.uparser import parseString
from mwlib.parser import show
from mwlib.xhtmlwriter import MWXHTMLWriter, preprocess

try:
    import xml.etree.ElementTree as ET
except:
    from elementtree import ElementTree as ET


BASE_URL = 'https://wiki.freeswitch.org/index.php?title=%s&action=raw'


# Oh the joys of monkeypatching...
# We need a CDATA element in set_security_msg, but ElementTree doesn't
# support it.
def CDATA(text=None):
    element = ET.Element('![CDATA[')
    element.text = text
    return element


# Python 2.7 and 3
if hasattr(ET, '_serialize_xml'):
    ET._original_serialize_xml = ET._serialize_xml
    def _serialize_xml(write, elem, *args):
        if elem.tag == '![CDATA[':
            write("\n<![CDATA[%s]]>\n" % (elem.text))
            return
        return ET._original_serialize_xml(write, elem, *args)
    ET._serialize_xml = ET._serialize['xml'] = _serialize_xml
# Python 2.5-2.6, and non-stdlib ElementTree
elif hasattr(ET.ElementTree, '_write'):
    ET.ElementTree._orig_write = ET.ElementTree._write
    def _write(self, file, node, encoding, namespaces):
        if node.tag == '![CDATA[':
            file.write("\n<![CDATA[%s]]>\n" % node.text.encode(encoding))
        else:
            self._orig_write(file, node, encoding, namespaces)
    ET.ElementTree._write = _write
else:
    raise RuntimeError(
        "Don't know how to monkeypatch CDATA support. "
        "Please report a bug at https://github.com/seveas/python-hpilo")


class Environment(object):
    def __init__(self, title):
        self.metabook = {'title': title}


class ConfluenceWriter(MWXHTMLWriter):
    """Confluence Wiki Writer.

    Details of HTML that needs to be wrote to Confluence:

        <h1>About</h1>
        <p>This module stores CDRs (Call Detail Record) directly to a MongoDB database.</p>
        <ac:structured-macro ac:name="panel">
           <ac:parameter ac:name="bgColor">#f7f7f7</ac:parameter>
           <ac:parameter ac:name="borderStyle">dotted</ac:parameter>
           <ac:parameter ac:name="borderColor">lightgray</ac:parameter>
           <ac:parameter ac:name="borderWidth">1</ac:parameter>
           <ac:rich-text-body>
             <p>
               <ac:structured-macro ac:name="toc">
                 <ac:parameter ac:name="printable">false</ac:parameter>
                 <ac:parameter ac:name="style">none</ac:parameter>
                 <ac:parameter ac:name="maxLevel">3</ac:parameter>
                 <ac:parameter ac:name="indent">1em</ac:parameter>
                 <ac:parameter ac:name="exclude">About</ac:parameter>
               </ac:structured-macro>
             </p>
           </ac:rich-text-body>
        </ac:structured-macro>
    """
    header = ''
    css = None

    def asstring(self):
        def _r(obj, p=None):
            for c in obj:
                assert c is not None
                for k,v in c.items():
                    if v is None:
                        print k,v
                        assert v is not None
                _r(c,obj)
        _r(self.root)
        #res = self.header + ET.tostring(self.getTree())
        res = self.header + u''.join([x.decode('utf-8') for x in ET.tostringlist(self.root, "utf-8")])
        return res

    def xwritePreFormatted(self, obj):
        """Pre formatted code writer.

        The code block that Confluence supports:

            <ac:structured-macro ac:name="code">
              <ac:parameter ac:name="theme">Emacs</ac:parameter>
              <ac:plain-text-body><![CDATA[
                Content
              ]]></ac:plain-text-body>
            </ac:structured-macro>
        """
        ac_sm = ET.Element('ac:structured-macro', attrib={'ac:name': 'code'})
        ac_param = ET.SubElement(ac_sm, 'ac:parameter',
                                 attrib={'ac:name': 'theme'})
        ac_param.text = 'Emacs'
        ac_plain = ET.SubElement(ac_sm, 'ac:plain-text-body')

        # Using the mocked CDATA to allow ElementTree write CDATA tags.
        cdata = CDATA(obj.children[0].text)
        ac_plain.append(cdata)

        obj.children = obj.children[1:]
        return ac_sm


def write_confluence_XHTML(wikitext, title):
    """Boilerplate of MWLib and write Confluence XHTML."""
    env = Environment(title)
    db = DummyDB()
    r = parseString(title=title, raw=wikitext, wikidb=db)
    preprocess(r)
    show(sys.stdout, r)

    dbw = ConfluenceWriter(env=env)
    dbw.writeBook(r)
    return dbw.asstring()


def fix_cdata_output(xhtml):
    """Fixes the CDATA output. In the Confluence Writer there is a hack to
    allow ElementTree write CDATA tags, but it closes the like an common HTML
    tag, here we fix it.
    """
    xhtml = xhtml.replace('<![CDATA[>', '<![CDATA[')
    xhtml = xhtml.replace('</![CDATA[>', ']]>')
    return xhtml


class PageNotFound(Exception):
    pass


class PageAlreadyMigrated(Exception):
    pass


def translate(page_title):
    """Translates an Wiki Page from Media Wiki to Confluence Wiki."""
    url = BASE_URL % page_title

    page = urllib.urlopen(url)
    if page.getcode() != 200:
        raise PageNotFound('The page "%s" was not found.' % page_title)

    if 'wiki.freeswitch.org/' not in page.geturl():
        raise PageAlreadyMigrated('The page "%s" was already migrated.'
                                  % page_title)

    raw = page.read()
    xhtml = write_confluence_XHTML(raw.decode('utf-8'), page_title)
    xhtml = fix_cdata_output(xhtml)
    return xhtml


if __name__ == '__main__':
    title = sys.argv[1]
    print translate(title)
