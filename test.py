class T:

    def __init__(self):
        self.flag = False
        self.a = {
            1: 2,
            2: 4
        }


def test(t, a):
    t.flag = True
    a[1] = 5


t = T()
test(t, t.a)

print(t.a)
