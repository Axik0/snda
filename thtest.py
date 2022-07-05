import time
import concurrent.futures


def timer(f):
    def inner(*args, **kwargs):
        tic = time.perf_counter()
        result = f(*args, **kwargs)
        toc = time.perf_counter()
        print(f"{toc-tic:.1f}s to run {f.__name__}")
        return result
    return inner


@timer
def test(s):
    # with open("test/1_bath-water-seller.jpg", 'rb') as img:
    #     print(img.read(50))
    time.sleep(s)
    return s

# tic = time.perf_counter()
# print(f"{time.perf_counter()-tic:.1f}s")


with concurrent.futures.ThreadPoolExecutor() as execc:
    largs = [_ for _ in range(5, 0, -1)]
    results = execc.map(test, largs)
    print([results])