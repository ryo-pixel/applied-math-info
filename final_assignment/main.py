import numpy as np
import matplotlib.pyplot as plt


def generate_tsp_instance(num_cities, seed=42):
    """ランダムな都市座標と距離行列を生成"""
    np.random.seed(seed)
    coords = np.random.rand(num_cities, 2) * 100  # 100x100の平面上に配置

    dist_matrix = np.zeros((num_cities, num_cities))
    for i in range(num_cities):
        for j in range(num_cities):
            dist_matrix[i, j] = np.linalg.norm(coords[i] - coords[j])

    return coords, dist_matrix


def calculate_tour_length(tour, dist_matrix):
    """巡回路の総距離（コスト）を計算"""
    length = 0
    num_cities = len(tour)

    for i in range(num_cities):
        length += dist_matrix[tour[i], tour[(i + 1) % num_cities]]

    return length


def calculate_entropy(probabilities):
    """確率分布からShannonエントロピーを計算 (bits)"""
    eps = 1e-12
    p = np.array(probabilities) + eps
    p = p / np.sum(p)

    return -np.sum(p * np.log2(p))


def run_tsp_search(
    num_cities=10,
    num_samples=100,
    iterations=50,
    cool_temperature=True,
    seed=42
):
    """
    TSPの解候補群を探索し、エントロピーと情報量の推移を計算する。

    cool_temperature=True:
        通常のSA（温度が徐々に低下）

    cool_temperature=False:
        対照実験（温度が一定 T=50.0）
    """

    np.random.seed(seed)

    _, dist_matrix = generate_tsp_instance(
        num_cities,
        seed=seed
    )

    # 初期状態：ランダムな巡回路を生成
    population = [
        np.random.permutation(num_cities)
        for _ in range(num_samples)
    ]

    costs = np.array([
        calculate_tour_length(tour, dist_matrix)
        for tour in population
    ])

    history_entropy = []
    history_info_gain = []

    # 初期温度
    temperature = 50.0

    # 通常SAでは温度を0.95倍ずつ下げる
    # Controlでは温度を50.0に固定
    cooling_rate = 0.95 if cool_temperature else 1.0

    # 初期状態のEntropy H(0)
    p_initial = np.exp(-costs / temperature)
    p_initial /= np.sum(p_initial)

    H_0 = calculate_entropy(p_initial)

    # Iteration
    for t in range(iterations):

        new_population = []
        new_costs = []

        for i in range(num_samples):

            current_tour = population[i].copy()

            # ==========================================
            # 2-opt neighborhood operation
            # ==========================================
            # ランダムに2つの位置を選択
            idx1, idx2 = sorted(
                np.random.choice(
                    num_cities,
                    size=2,
                    replace=False
                )
            )

            # idx1～idx2の経路を反転
            current_tour[idx1:idx2 + 1] = (
                current_tour[idx1:idx2 + 1][::-1]
            )

            # 新しいツアーのコストを計算
            new_cost = calculate_tour_length(
                current_tour,
                dist_matrix
            )

            old_cost = costs[i]

            # コスト差
            delta = new_cost - old_cost

            # ==========================================
            # Simulated Annealing acceptance rule
            # ==========================================
            if (
                delta < 0
                or np.random.rand() < np.exp(-delta / temperature)
            ):
                new_population.append(current_tour)
                new_costs.append(new_cost)

            else:
                new_population.append(population[i])
                new_costs.append(costs[i])

        # Populationを更新
        population = new_population
        costs = np.array(new_costs)

        # ==========================================
        # 温度更新
        # ==========================================
        temperature *= cooling_rate

        # ==========================================
        # Entropy calculation
        # ==========================================
        p_t = np.exp(-costs / temperature)
        p_t /= np.sum(p_t)

        H_t = calculate_entropy(p_t)

        # Information Gain
        I_t = H_0 - H_t

        history_entropy.append(H_t)
        history_info_gain.append(I_t)

    return history_entropy, history_info_gain


def main():

    iterations = 50

    # ==========================================
    # 1. 通常の Simulated Annealing
    #    温度低下あり
    # ==========================================
    entropy_sa, info_sa = run_tsp_search(
        cool_temperature=True,
        iterations=iterations
    )

    # ==========================================
    # 2. Control Run
    #    温度一定 T=50.0
    # ==========================================
    entropy_ctrl, info_ctrl = run_tsp_search(
        cool_temperature=False,
        iterations=iterations
    )

    # ==========================================
    # グラフ描画
    # ==========================================
    fig, (ax1, ax2) = plt.subplots(
        1,
        2,
        figsize=(14, 5)
    )

    # ==========================================
    # 左図：Entropy Comparison
    # ==========================================
    ax1.plot(
        entropy_sa,
        color='tab:red',
        linewidth=2,
        label='Annealing (T cooled)'
    )

    ax1.plot(
        entropy_ctrl,
        color='tab:gray',
        linewidth=2,
        linestyle='--',
        label='Control (T fixed at 50.0)'
    )

    ax1.set_xlabel('Iteration (t)')
    ax1.set_ylabel('Entropy H(t) [bits]')
    ax1.set_title(
        'Uncertainty / Entropy Reduction: SA vs. Control'
    )

    ax1.grid(True, alpha=0.3)
    ax1.legend()

    # ==========================================
    # 右図：Information Gain Comparison
    # ==========================================
    ax2.plot(
        info_sa,
        color='tab:blue',
        linewidth=2,
        label='Annealing (T cooled)'
    )

    ax2.plot(
        info_ctrl,
        color='tab:cyan',
        linewidth=2,
        linestyle='--',
        label='Control (T fixed at 50.0)'
    )

    ax2.set_xlabel('Iteration (t)')
    ax2.set_ylabel(
        'Information Gain I(t) [bits]'
    )

    ax2.set_title(
        'Information Gain: SA vs. Control'
    )

    ax2.grid(True, alpha=0.3)
    ax2.legend()

    fig.tight_layout()

    # グラフ保存
    plt.savefig(
        'result_information_gain.png',
        dpi=300
    )

    print(
        "Comparison simulation complete. "
        "Graph saved as 'result_information_gain.png'"
    )


if __name__ == "__main__":
    main()