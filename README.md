VB6国际化工具
=============
##动机

这个工具是用来完成遗留VB6项目的国际化的。

现有日文的VB6工程，需要将它进行国际化，支持中文，越南语等。

##方案
目标工程中，所有日文均是直接写在代码中，经研究，VB6可以使用资源文件中的StringTable来支持多国语言。

首先要找出所有的日文字符串，将其用StringTable的语法，以Unicode编码写入RC文件中，再用VB/VC6自带的RC.exe编译成RES文件。而相应的日文字符串，在代码用LoadResString来进行替换。

##工具
手工做这件事显然非常困难，所以就制作了这个工具，可以自动检测并替换日文字符串。

##使用方法

    python VB6_i18nizer.py {top_dir} [.vbs] [.frm] [.bas]

topdir是VB代码所在目录
后面的.vbs可以不写，默认对.vbs, .frm和.bas进行操作。

