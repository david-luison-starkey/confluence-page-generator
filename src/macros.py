from typing import List, Dict

# https://confluence.atlassian.com/display/CONF55/Working+with+Macros
CODE_EXTENSION: List[Dict[str, str]] = [
    {"code": "actionscript3", "extension": "as"},
    {"code": "bash", "extension": "sh"},
    {"code": "csharp", "extension": "cs"},
    {"code": "coldfusion", "extension": "cfm"},
    {"code": "cpp", "extension": "cpp"},
    {"code": "css", "extension": "css"},
    {"code": "delphi", "extension": "pas"},
    {"code": "diff", "extension": "diff"},
    {"code": "erlang", "extension": "erl"},
    {"code": "groovy", "extension": "groovy"},
    {"code": "html", "extension": "html"},
    {"code": "java", "extension": "java"},
    {"code": "javafx", "extension": "javafx"},
    {"code": "javascript", "extension": "js"},
    {"code": "json", "extension": "json"},
    {"code": "none", "extension": "txt"},
    {"code": "perl", "extension": "pl"},
    {"code": "php", "extension": "php"},
    {"code": "powershell", "extension": "ps1"},
    {"code": "python", "extension": "py"},
    {"code": "ruby", "extension": "rb"},
    {"code": "scala", "extension": "scala"},
    {"code": "sql", "extension": "sql"},
    {"code": "typescript", "extension": "ts"},
    {"code": "vb", "extension": "vb"},
]


def get_code_block_macro_string(code_block: str, language: str) -> str:
    return (
        '<ac:structured-macro ac:name="code">'
        f'<ac:parameter ac:name="language">{language}</ac:parameter>'
        """
<ac:parameter ac:name="linenumbers">true</ac:parameter>
<ac:plain-text-body>
<![CDATA["""
        f"{code_block}"
        """    
]]>
</ac:plain-text-body>
</ac:structured-macro>
"""
    )


def get_table_contents_macro_string() -> str:
    return """
<ac:structured-macro ac:name="toc">
</ac:structured-macro>
"""


def get_page_tree_macro_string() -> str:
    return """
<ac:structured-macro ac:name="pagetree">
<ac:parameter ac:name="root">
<ac:link>@self</ac:link>
</ac:parameter>
</ac:structured-macro>
"""
