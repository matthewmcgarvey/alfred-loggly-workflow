# encoding: utf-8
import sys
from workflow import Workflow3, ICON_WEB, web

def get_searches(wf):
    searches = wf.stored_data("searches")
    if searches is None:
        searches = []
    return searches

def save_searches(wf, searches):
    wf.store_data("searches", searches)

def set_item(wf, search):
    wf.add_item(
        title=search,
        arg=search,
        icon=ICON_WEB,
        valid=True
    )

def set_items(wf, searches):
    for search in searches:
        set_item(wf, search)

def set_user_search(wf, search):
    wf.add_item(
        title=search,
        arg="-n " + search,
        icon=ICON_WEB,
        valid=True
    )

def main(wf):
    searches = get_searches(wf)
    if not wf.args:
        if not searches:
            wf.warn_empty("please enter a search")
        else:
            set_items(wf, searches)
        wf.send_feedback()
        return
    if wf.args[0] == '--goto':
        search = None
        if wf.args[1] == '-n':
            search = " ".join(wf.args[2:])
            searches.append(search)
            save_searches(wf, searches)
        if search is None:
            search = " ".join(wf.args[1:])
        print(search)
        return
    if wf.args[0] == '--delete':
        search_to_delete = " ".join(wf.args[1:])
        new_searches = []
        for search in searches:
            if search != search_to_delete:
                new_searches.append(search)
        save_searches(wf, new_searches)
        return
    search = " ".join(wf.args)
    matched = wf.filter(search, searches)
    set_user_search(wf, search)
    set_items(wf, matched)
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow3(libraries=['./lib'])
    sys.exit(wf.run(main))