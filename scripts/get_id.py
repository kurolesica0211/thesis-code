from pathlib import Path


bench_dir = Path("custom_family_bench")
texts_dir = bench_dir.joinpath("royalty/denoised_texts")
ids = set([
    str(path).split("/")[-1].removesuffix(".txt")
    for path in texts_dir.iterdir()
    if not str(path).split("/")[-1].startswith(".")
])
final_ids = sorted(ids)

print(final_ids.index("Constantine_II_of_Greece"))