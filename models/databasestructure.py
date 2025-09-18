DatabaseStructure = {
    'form': [
        {'n': 'int'},
        {'lit': 'text'},
        {'litnum': 'text'},
        {'firstname': 'text'},
        {'secondname': 'text'},
        {'lastname': 'text'},
        {'note': 'text'}
    ],
    'formdestroy': [
        {'n': 'int'},
        {'formnum': 'int'},
        {'destroydate': 'text'},
        {'destroynum': 'text'}
    ],
    'formsend': [
        {'n': 'int'},
        {'formnum': 'int'},
        {'ust': 'text'},
        {'senddirection': 'text'},
        {'regdate': 'text'},
        {'regnum': 'text'}
    ],
    'mails': [
        {'n': 'int'},
        {'formnum': 'int'},
        {'askdate': 'text'},
        {'asknum': 'text'},
        {'ansdate': 'text'},
        {'ansnum': 'text'},
        {'formacsess': 'int'},
        {'nakazdate': 'text'},
        {'nakaznum': 'text'},
        {'nakazstatus': 'text'},
        {'note': 'text'}
    ],
}
