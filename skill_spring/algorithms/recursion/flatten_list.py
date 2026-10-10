def flatten_list(lst, output=None):
    if output is None:
        output = []

    if len(lst) == 0:
        return output

    first, rest = lst[0], lst[1:]

    if isinstance(first, list):
        flatten_list(first, output)
    else:
        output.append(first)

    return flatten_list(rest, output)


def flatten_list_cleaner(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten_list_cleaner(item))
        else:
            result.append(item)
    return result


from typing import List, Any


def flatten_list_type_safe(lst: List[Any]) -> List[Any]:
    if not lst:
        return []

    head, *tail = lst

    if isinstance(head, list):
        return flatten_list_type_safe(head) + flatten_list_type_safe(tail)
    else:
        return [head] + flatten_list_type_safe(tail)
