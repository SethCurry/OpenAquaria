from openaquaria.octopus.observer import Range


def test_Range():
    r = Range(10, 20)

    mut = 0.0

    def callback(val: float):
        nonlocal mut
        mut = val

    r.add_callback(callback)
    r.ingest(15.1)

    assert mut == 0.0

    r.ingest(1.2)

    assert mut == 1.2
