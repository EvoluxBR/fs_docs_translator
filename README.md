# FreeSwitch docs translator
A translator script to help the migration from the old FreeSwitch's Media Wiki to new FreeSwitch's Confluence Wiki.


Installation
-----------
1. [Download](/EvoluxBR/fs_docs_translator/archive/master.zip) or fork this project and go to the enclosing folder.
2. `$ pip install -r requirements.txt` *If you do not have the `pip` you can use `easy_install`.

Usage
-----

Run the `translator.py` program with an wiki page title.
```sh
$ python translator.py API_sofia_count_reg
 Article->'API_sofia_count_reg'
     Section tagname='@section' level=3
         Node
             u'API sofia_count_reg '
         Paragraph tagname='p'->'p'
             u'This api is used to return the count of registration of a user of a domain, or just of a domain. '
         Paragraph tagname='p'->'p'
             Strong''
                 u'Usage:'
         PreFormatted
             u'#>sofia_count_reg [user]@domain\n'
         Paragraph tagname='p'->'p'
         Paragraph tagname='p'->'p'
             Strong''
                 u'See also:'
         ItemList tagname='ul'->'ul'
             Item tagname='li'->'li'
                 ArticleLink target=u'mod_sofia' ns=0
         Paragraph tagname='p'->'p'
         Paragraph tagname='p'->'p'
             Strong''
                 u'Implemented By:'
         Table tagname='table' vlist={u'cellpadding': 5, u'cellspacing': 0, u'border': 1}
             Row tagname='tr'
                 Cell tagname='td'
                     Strong tagname=u'b'
                         u'Module Name'
                 Cell tagname='td'
                     Strong tagname=u'b'
                         u'Source File'
                 Cell tagname='td'
                     Strong tagname=u'b'
                         u'Last Updated'
             Row tagname='tr'
                 Cell tagname='td'
                     u'mod_sofia'
                 Cell tagname='td'
                 Cell tagname='td'
         Paragraph tagname='p'->'p'
             CategoryLink target=u'Category:API' ns=14
in write Article Article->'API_sofia_count_reg'
<html xml:lang="en" xmlns="http://www.w3.org/1999/xhtml"><head><title>API_sofia_count_reg</title></head><body><div class="mwx.article"><h1>API_sofia_count_reg</h1><div class="mwx.section"><h2>API sofia_count_reg </h2><div class="mwx.paragraph">This api is used to return the count of registration of a user of a domain, or just of a domain. </div><div class="mwx.paragraph"><strong>Usage:</strong></div><ac:structured-macro ac:name="code"><ac:parameter ac:name="theme">Emacs</ac:parameter><ac:plain-text-body>
<![CDATA[#>sofia_count_reg ]]>
</ac:plain-text-body></ac:structured-macro><div class="mwx.paragraph" /><div class="mwx.paragraph"><strong>See also:</strong></div><ul><li><a class="mwx.link.article" href="#">mod_sofia</a></li></ul><div class="mwx.paragraph" /><div class="mwx.paragraph"><strong>Implemented By:</strong></div><table border="1" cellpadding="5" cellspacing="0"><tr><td><strong>Module Name</strong></td><td><strong>Source File</strong></td><td><strong>Last Updated</strong></td></tr><tr><td>mod_sofia</td><td /><td /></tr></table><div class="mwx.paragraph" /></div><ol class="mwx.categorylinks"><li><a class="mwx.link.category" href="Category:API">Category:API</a></li></ol></div></body></html>
```

The content that you want is that with starts with `<html xml:lang="en"` you can just copy and paste on Confluence.
