from app.music import Music
from app.scale import Scale
from app.key import Key
from app.modes import Modes
import pandas as pd
from IPython.display import display, HTML



if __name__ == "__main__":
    d_major = Scale('C', 'major')
    d_dom = Scale('F', 'melodic minor').reorder('C')
    try:
        display(pd.DataFrame([d_major.chords, d_dom.chords], index=[d_major.name, d_dom.name]))
    except Exception as e:
        print(e)
    print(d_dom.reorder("Bb").intervals)
    print(d_dom.intervals)