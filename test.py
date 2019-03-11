# -*- coding: utf-8 -*-

def exist_sensitive_words(payload):
    sensitive_words = ["select", "show", "top", "distinct", "from", "dual", "where", "group by", "order by",
                       "having", "limit", "offset", "union", "union all", "rownum as", "(case"]
    for each_word in sensitive_words:
        if -1 != payload.find(each_word):
            return True
    return False
