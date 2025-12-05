import os

round = 3 

for i in range(0, round):
    print("\n" + "=" * 50)
    print(f"ĐANG CHẠY LẦN TEST THỨ {i+1}")
    print("=" * 50 + "\n")

    os.system(f"RUN_INDEX={i+1} pytest -s")

print(f"\n✅ ĐÃ CHẠY XONG {round} LẦN TEST!")
