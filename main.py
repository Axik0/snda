import os
import time

from multiprocessing import Pool
from multiprocessing import cpu_count


# def background(f):
#     import asyncio
#     def wrapped(*args):
#         return asyncio.get_event_loop().run_in_executor(None, f, *args)
#     return wrapped

def l_analysis(af_path):
    # moving import statements inside results in ~1s gain!
    import audioread.ffdec
    import librosa
    # ffmpeg binary backend must exist in the project folder if you want to read mp3 files with audioread
    """takes a file by path returns mp3 audio file BPM"""
    with audioread.audio_open(af_path) as m:
        # print(f.channels, f.samplerate, f.duration)
        lo = librosa.load(m)
        # each librosa object is a tuple, (y=array, sr=sampling rate)
        # beat_frames are subsections of y in the vicinity of each detected beat
        tempo, beat_frames = librosa.beat.beat_track(y=lo[0], sr=lo[1])
        return tempo, af_path


def l_analysis_o(afo):
    """takes pre-loaded object from RAM?. Anyway, not by path. Returns mp3 audio file BPM"""
    import librosa
    lo = librosa.load(afo)
    # each librosa object is a tuple, (y=array, sr=sampling rate)
    # beat_frames are subsections of y in the vicinity of each detected beat, we just ignore those here
    tempo = librosa.beat.beat_track(y=lo[0], sr=lo[1])
    return tempo


def ar_preloader(af_path):
    """creates a librosa object in memory"""
    import audioread.ffdec
    # ffmpeg binary backend must exist in the project folder if you want to read mp3 files with audioread
    with audioread.audio_open(af_path) as m:
        print(m.channels, m.samplerate, m.duration)
        return l_analysis_o(m)


if __name__ == "__main__":
    # NO PRINTING / ANY TIME-CONSUMING METHODS ABOVE THIS LINE!
    FOLDER = 'test'
    # build path from current folder
    path = os.path.join("./", FOLDER)
    # check that the directory exists
    # print(path, os.path.isdir(path), os.getcwd())
    # scan the directory and generate list of paths to the files we want
    fpl = []
    for e in os.listdir(path):
        tp = os.path.join(path, e)
        if os.path.isfile(tp) and e.lower().endswith('.mp3'):
            fpl.append(tp)

    # Standard loop takes ~9.5s
    # tict = time.perf_counter()
    # for p in fpl:
    #     tic = time.perf_counter()
    #     res = l_analysis(p)
    #     toc = time.perf_counter()
    #     print(f'Time spent: {toc - tic:.2f}', f'Tempo: {res:.2f}')
    # toct = time.perf_counter()
    # print(f'Time spent total: {toct-tict:.2f}')

    # # MP is a proper way to bypass GIL (1 io process lock w/ threading), now each process has its own GIL
    # # generate pool of processes, one per CPU core, almost no difference for core amount 4-16
    # pool = Pool(cpu_count())
    # tti = time.perf_counter()
    # with pool as po:
    #     # multiprocessor analogue of python's built-in map function
    #     results = po.map(l_analysis, fpl)
    # # I need context management here to ensure that all processes are killed after completion, otherwise:
    # # pool.close()  # 'TERM'
    # # pool.join()   # 'WAIT for processes to be killed'
    # tto = time.perf_counter()
    # print(f'Time spent total: {tto-tti:.2f}', results)
    # # MP version results in ~5.3s

    ar_preloader(fpl[0])
    # lol = []
    # tti = time.perf_counter()
    # for p in fpl:
    #     lol.append(ar_preloader(p))
    # tto = time.perf_counter()
    # print(f'Time spent stage 1: {tto - tti:.2f}', lol)

    # l_analysis_o(lol[0])
    # pool = Pool(cpu_count())
    # tti = time.perf_counter()
    # with pool as po:
    #     results = po.map(l_analysis_o, lol)
    # tto = time.perf_counter()
    # print(f'Time spent stage 2: {tto - tti:.2f}', results)
