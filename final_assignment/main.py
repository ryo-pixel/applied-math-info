import numpy as np
import matplotlib.pyplot as plt

def generate_tsp_instance(num_cities, seed=42):
    """ランダムな都市座標と距離行列を生成"""
    np.random.seed(seed)
    coords = np.random.rand(num_cities, 2) * 100  # 100x100の平面上に配置
    
    # 都市間のユーグリッド距離行列
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

def run_real_tsp_search(num_cities=10, num_samples=100, iterations=50):
    """
    実際にTSPの解候補を探索し、その解のコスト分布からエントロピーを算出する
    """
    _, dist_matrix = generate_tsp_instance(num_cities)
    
    # 初期状態：完全ランダムな巡回路を100個生成
    population = [np.random.permutation(num_cities) for _ in range(num_samples)]
    
    history_entropy = []
    history_info_gain = []
    
    # 初期評価値の計算
    costs = np.array([calculate_tour_length(tour, dist_matrix) for tour in population])
    
    # ソフトマックス（ボルツマン分布）で選択確率をモデル化するパラメータ（温度）
    temperature = 50.0
    cooling_rate = 0.95
    
    # 初期エントロピー H(0)
    p_initial = np.exp(-costs / temperature)
    p_initial /= np.sum(p_initial)
    H_0 = calculate_entropy(p_initial)
    
    for t in range(iterations):
        # 探索ステップ：各個体に2-opt風の変異（2都市の入れ替え）を適用して解を更新
        new_population = []
        new_costs = []
        
        for i in range(num_samples):
            current_tour = population[i].copy()
            
            # ランダムに2つの位置を選んで入れ替える（局所探索）
            idx1, idx2 = np.random.choice(num_cities, size=2, replace=False)
            current_tour[idx1], current_tour[idx2] = current_tour[idx2], current_tour[idx1]
            
            new_cost = calculate_tour_length(current_tour, dist_matrix)
            old_cost = costs[i]
            
            # 良い解は必ず採用、悪い解も確率的に許容（模擬焼鈍法のアルゴリズム）
            delta = new_cost - old_cost
            if delta < 0 or np.random.rand() < np.exp(-delta / temperature):
                new_population.append(current_tour)
                new_costs.append(new_cost)
            else:
                new_population.append(population[i])
                new_costs.append(costs[i])
                
        population = new_population
        costs = np.array(new_costs)
        
        # 温度の更新（冷却）
        temperature *= cooling_rate
        
        # 現在の解アンサンブルにおける選択確率分布とエントロピーの計算
        p_t = np.exp(-costs / (temperature + 1e-5))
        p_t /= np.sum(p_t)
        
        H_t = calculate_entropy(p_t)
        I_t = H_0 - H_t
        
        history_entropy.append(H_t)
        history_info_gain.append(I_t)
        
    return history_entropy, history_info_gain

def main():
    entropy, info_gain = run_real_tsp_search(num_cities=10, num_samples=100, iterations=50)
    
    # プロットと画像保存
    fig, ax1 = plt.subplots(figsize=(8, 5))

    color = 'tab:red'
    ax1.set_xlabel('Iteration (t)')
    ax1.set_ylabel('Entropy H(t) [bits]', color=color)
    ax1.plot(entropy, color=color, linewidth=2, label='Entropy H(t)')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  
    color = 'tab:blue'
    ax2.set_ylabel('Information Gain I(t) [bits]', color=color)
    ax2.plot(info_gain, color=color, linewidth=2, linestyle='--', label='Information Gain I(t)')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Real TSP Search: Uncertainty Reduction and Information Gain')
    fig.tight_layout()
    plt.grid(True, alpha=0.3)
    
    plt.savefig('result_information_gain.png', dpi=300)
    print("Real TSP simulation complete. Graph saved as 'result_information_gain.png'")

if __name__ == "__main__":
    main()