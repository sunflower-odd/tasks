def func():
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        i = 0
        for line in lines:
            if i==0:
                w=int(line)
                i+=1
            elif i==1:
                n=int(line)
                i += 1
            else:
                weights = list(map(int, line.split()))
                weights.sort(reverse=True)
        weghts_base = weights.copy()
        all_variants=[]
        filled = 0
        for iteration in range(len(weghts_base)):
            while filled<=w and len(weights)>0:
                add_item=weights[0]
                filled += add_item
                if filled>w:
                    filled-= add_item
                    break
                weights.pop(0)
            if filled<w:
                remaining_capacity = w - filled
                for rest_gold in weights[:]:
                    if rest_gold <= remaining_capacity:
                        filled += rest_gold
                        remaining_capacity -= rest_gold
                        weights.remove(rest_gold)
            weghts_base.pop(0)
            all_variants.append(filled)
            filled = 0
            iteration+=1
    print(max(all_variants))
    return filled


if __name__ == '__main__':
    func()