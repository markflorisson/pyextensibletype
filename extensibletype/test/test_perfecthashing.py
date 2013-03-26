from nose.tools import eq_, ok_
import numpy as np
from .. import extensibletype, methodtable


def test_binsort():
    nbins = 64
    p = np.zeros(nbins, dtype=np.uint16)
    binsizes = np.random.randint(0, 7, size=nbins).astype(np.uint8)
    num_by_size = np.zeros(8, dtype=np.uint8)
    x = np.bincount(binsizes).astype(np.uint8)
    num_by_size[:x.shape[0]] = x
    extensibletype.bucket_argsort(p, binsizes, num_by_size)
    assert np.all(sorted(binsizes) == binsizes[p][::-1])

def test_basic():
    n=64
    prehashes = extensibletype.draw_hashes(np.random, n)
    assert len(prehashes) == len(set(prehashes))
    p, r, m_f, m_g, d = extensibletype.perfect_hash(prehashes, repeat=10**5)
    hashes = ((prehashes >> r) & m_f) ^ d[prehashes & m_g]
    print(p)
    print(d)
    hashes.sort()
    print(hashes)
    assert len(hashes) == len(np.unique(hashes))

def test_methodtable():
    ids = ["ff->f", "dd->d", "ii->i", "ll->l", "OO->O"]
    flags = range(1, len(ids) + 1)
    funcs = range(len(ids))

    table = methodtable.PerfectHashMethodTable(methodtable.Hasher())
    table.generate_table(len(ids), ids, flags, funcs)

    for (signature, flag, func) in zip(ids, flags, funcs):
        result = table.find_method(signature)
        assert result is not None
        got_func, got_flag = result
        assert func == got_func, (func, got_func)
        # assert flag == got_flag, (flag, got_flag)

