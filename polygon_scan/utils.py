def is_seq(seq):
    return hasattr(seq, "__iter__") or (
        hasattr(seq, "__len__") and hasattr(seq, "__getitem__")
    )
