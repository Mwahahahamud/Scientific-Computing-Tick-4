import numpy as np
import matplotlib as plt
def one_percent(pop):
    return np.sum(np.flip(np.sort(pop))[0:pop.size // 100]) / np.sum(pop)


def pairs(N):
    x = np.arange(N)
    np.random.shuffle(x)
    return ((x[0:N // 2], x[N // 2:N]))


def converges(inequalities, convergence_num):
    stde = np.std(inequalities[0:convergence_num]) / np.sqrt(convergence_num)
    if np.mean(inequalities[convergence_num // 2:convergence_num]) - np.mean(inequalities[0:convergence_num // 2]) < 2 * stde:
        print("Converges")
        return True

def simulation(compound, T):
    equality = 0
    time_steps = 0
    pop_size = 10000
    population = np.ones(pop_size)


    def biased_exchange(a, b, R):
        if R > 0:
            return (a + ((R * min(a, b)) * (1 - T)), b - (R * min(a, b)))
        return (a + (R * min(a, b)), b - ((R * min(a, b)) * (1 - T)))

    def compoundInt(popBefore):
        popAfter = popBefore ** compound
        if popAfter > popBefore:  # Tax
            return popBefore + ((popAfter - popBefore) * (1 - T))
        return popAfter

    def tax(popBefore, popAfter):
        return max((np.sum(popBefore) - np.sum(popAfter)), 0)

    convergence_num = 200

    vexchange = np.vectorize(biased_exchange)
    vcompound = np.vectorize(compoundInt)

    inequalities = np.zeros(convergence_num)

    while equality < 0.32:


        time_steps += 1
        Taxes = 0

        if (time_steps % convergence_num == 0) and (time_steps > convergence_num):
            # Check if it didn't converge
            # Calculate the
            if converges(inequalities, convergence_num) == True:
                print(time_steps)
                time_steps = -1
                break

        # Exchanges
        n1, n2 = pairs(pop_size)
        all_pairs = np.concatenate([n1, n2])
        v, w = population[n1], population[n2]
        v_new, w_new = vexchange(v, w, (np.random.random_sample(pop_size // 2) - 0.5) * 2)
        exc_population = np.concatenate([v_new, w_new])[np.argsort(all_pairs)]

        # Exchange tax
        Taxes += tax(population, exc_population)
        if tax(population, exc_population) < 0:
            print(sum(population), sum(exc_population))
            print(tax(population, exc_population))
            print("exch tax throws error")
        # Return on capital
        ret_population = vcompound(exc_population)
        Taxes += tax(exc_population ** compound, ret_population)


        if tax(exc_population ** compound, ret_population) < 0:
            print(tax(exc_population ** compound, ret_population))
            print("compound tax throws error")


        # Distribute taxes
        population = ret_population + (Taxes / pop_size)

        # Normalise
        population *= (pop_size / np.sum(population))

        # Check if unequal
        equality = one_percent(population)

        if Taxes < 0:
            print("Total Taxes")
            print(Taxes)
            print(time_steps)

        inequalities[time_steps % convergence_num] = equality

    return (time_steps, np.average(inequalities))


