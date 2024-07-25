def max_val(to_consider, avail):
    if to_consider == [] or avail == 0:
        result = 0, ()
    elif to_consider[0].get_units() > avail:
        result = max_val(to_consider[1:], avail)
    else:
        next_item = to_consider[0]
        with_val, with2take = max_val(
            to_consider[1:], avail - next_item.get_units()
        )
        withVal += next_item.get_value()
        without_val, without2take = max_val(to_consider[1:], avail)
    if with_val > without_val:
        result = with_val, with2take + (next_item,)
    else:
        result = without_val, without2take
    return result