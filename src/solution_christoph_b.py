#!/usr/bin/env python3

from src.common import load, load_output, save, score


def solution_christoph(data_input):

    durations = []
    for lib in data_input['libs']:
        duration = lib['t']
        duration_for_books = lib['n'] // lib['m']
        if lib['n'] // lib['m'] != 0:
            duration_for_books += 1
        durations.append(duration + duration_for_books)

    print(durations)

    libs = sorted(data_input['libs'], key=lambda k: k['t'])

    day_start = 0
    day_total = data_input['D']

    output = []
    for lib in libs:
        day_start += lib['t']
        left = day_total - day_start
        if left <= 0:
            break
        truncated = set(list(lib['ids'])[:left * lib['m']])
        lib['ids'] = truncated
        output.append(lib)

    return {"libs": output}


dset_a = "a_example"
dset_b = "b_read_on"
dset_c = "c_incunabula"
dset_d = "d_tough_choices"
dset_e = "e_so_many_books"
dset_f = "f_libraries_of_the_world"
dsets = [dset_a, dset_b, dset_c, dset_d, dset_e, dset_f]

if __name__ == "__main__":

    # dsets = dsets[1:2]

    total_score = 0

    for dset in dsets:
        data_input = load(dset)
        # print(data_input)
        solution_output = solution_christoph(data_input=data_input)
        score_value, filename = save(
            solution_output, method_name="method", ds_name=dset
        )
        print(dset)
        print(score(solution_output, data_input))

        total_score += score_value

        # solution_output = load_output(filename)
        # print(solution_output)

    print("total")
    print(total_score)
