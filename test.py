from tqdm import tqdm 

my_list = list(range(10000000))
with tqdm(total=len(my_list)) as pbar:
    for x in my_list:
        pbar.update(1)