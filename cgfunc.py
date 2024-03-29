
def cg_calc(data: dict):
    sum_weight = 0
    sum_sum = 0
    for key, item in data.items():
        sum_sum += item[0] * item[1]
        sum_weight = item[0]
    return sum_sum / sum_weight
