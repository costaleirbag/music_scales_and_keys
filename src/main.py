from key import Key
from scale import Scale

if __name__ == '__main__':
    scale = Scale("C", "melodic minor")
    print(scale.notes)
    key = Key(scale)
    from pdb import set_trace; set_trace()