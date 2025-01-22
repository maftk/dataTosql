import sys
import tracemalloc

# メモリ追跡を開始
tracemalloc.start()

# サンプル処理
# リストの場合
for x in range(3):
    list_data = [i ** 2 for i in range(10**6)]
    print(f"List size: {sys.getsizeof(list_data)} bytes")  # 数十MB以上になる

    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage: {current / (1024 * 1024):.2f} MB")
# print(f"Peak memory usage: {peak / (1024 * 1024):.2f} MB")
# # ジェネレーターの場合
# gen_data = (i ** 2 for i in range(10**6))
# print(f"Generator size: {sys.getsizeof(gen_data)} bytes")  # 数十バイト程度
#
# current, peak = tracemalloc.get_traced_memory()
# print(f"Current memory usage: {current / (1024 * 1024):.2f} MB")
# print(f"Peak memory usage: {peak / (1024 * 1024):.2f} MB")
#
# del list_data
# current, peak = tracemalloc.get_traced_memory()
# print(f"Current memory usage: {current / (1024 * 1024):.2f} MB")
# print(f"Peak memory usage: {peak / (1024 * 1024):.2f} MB")
# # メモリ使用状況を取得
#
# メモリ追跡を停止
tracemalloc.stop()
