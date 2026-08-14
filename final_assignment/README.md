# Information-Theoretic Analysis of TSP Search Dynamics

## Author
- **Course:** Applied Information Theory / 応用情報概要
- **Assignment:** Final Project / 最終課題
- **Student ID:** 6807001k
- **Name:** Ryohei Akehi

---

## Overview
This repository formulates "Information" in the context of combinatorial optimization, specifically applied to the **Traveling Salesman Problem (TSP)**. 

**Information** is defined as the **reduction of uncertainty (Shannon Entropy)** in the solution space during a stochastic optimization process. Using a Simulated Annealing (SA) metaheuristic with 2-opt neighborhood operators over a population of candidate tours, the transformation of raw search complexity into quantifiable information gain is systematically tracked.

---

## Mathematical Formulation

### 1. Solution Space Probability Distribution
Let $S = \{x_1, x_2, \dots, x_M\}$ be a population of $M = 100$ candidate TSP tours at iteration $t$, where each tour $x_i$ has a total length (cost) $C(x_i)$.

The selection probability $p_i(t)$ of tour $x_i$ is modeled using the **Boltzmann distribution** (softmax with temperature $T(t)$):

$$p_i(t) = \frac{\exp\left(-\frac{C(x_i)}{T(t)}\right)}{\sum_{j=1}^{M} \exp\left(-\frac{C(x_j)}{T(t)}\right)}$$

### 2. Shannon Entropy (Uncertainty)
The uncertainty $H(t)$ of the solution space at iteration $t$ is measured by the **Shannon Entropy** in bits:

$$H(t) = -\sum_{i=1}^{M} p_i(t) \log_2 p_i(t)$$

- **Initial State ($t=0$):** High temperature $T_0 = 50.0$ and randomized tours create a near-uniform probability distribution, resulting in an initial entropy close to the theoretical maximum ($\log_2(100) \approx 6.64$ bits).
- **Converged State:** As $T(t) \to 0$, the probability concentrates on lower-cost tours, causing $H(t)$ to decrease.

### 3. Information Gain
The **Information Gain $I(t)$** acquired by the algorithm up to iteration $t$ is mathematically defined as the reduction in entropy from the initial state:

$$I(t) = H(0) - H(t)$$

---

## Environment & Requirements

### Dependencies
- Python 3.8+
- `numpy`
- `matplotlib`

### Virtual Environment Setup & Installation
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install numpy matplotlib
```

### How to Run
1. Clone or download this repository.
2. Activate the virtual environment and install the dependencies (as shown above).
3. Execute the main Python script to run the TSP search and automatically generate the plot:

```bash
python main.py
```

Upon completion, the program will save the rendered plot as `result_information_gain.png`.

---

## Results

![Information Gain Plot](result_information_gain.png)

Starting from an initial entropy of $H(0) \approx 5.7$ bits (close to the theoretical maximum $\log_2(100) \approx 6.64$ bits for $M=100$ candidate tours), the entropy $H(t)$ decreases over 50 iterations to approximately $1.9 \sim 2.0$ bits, corresponding to an information gain of $I(t) \approx 3.8$ bits by the final iteration.

Two features of the curve are notable:
- **Overall Trend:** The overall trend confirms the hypothesis: as the simulated annealing search progresses and the temperature cools, uncertainty about which tour is best decreases substantially.
- **Non-Monotonic Behavior:** The curve is not monotonic — $H(t)$ fluctuates considerably (e.g., local increases around $t=10 \sim 11$ and $t=25 \sim 30$) rather than decreasing smoothly.

---

## Discussion & Analysis

### 1. Why the Entropy Curve is Noisy, Not Smooth
Unlike the idealized entropy-reduction picture in information theory (where each new piece of information monotonically reduces uncertainty), the $H(t)$ curve fluctuates. This occurs because each iteration applies only a single random 2-opt swap per individual, and the simulated-annealing acceptance rule occasionally accepts a worse tour (with probability $\exp(-\Delta / T)$).

This means individual iterations can locally increase the population's cost spread, temporarily raising entropy even while the long-run trend is downward. This is a genuine, expected feature of stochastic local search, not a bug — it reflects the fact that annealing intentionally tolerates temporary uphill moves to escape local optima.

### 2. A Limitation: Two Conflated Causes of Entropy Reduction
The entropy $H(t)$ is computed from a Boltzmann distribution $p_i(t) \propto \exp(-C(x_i)/T(t))$ that depends on both:
1. The actual costs $C(x_i)$ of the current population (which reflect real search progress), and
2. The cooling temperature $T(t)$, which decreases on a fixed schedule regardless of how well the search is performing.

Consequently, part of the entropy drop observed is mechanically caused by the shrinking temperature, which sharpens the Boltzmann distribution even if the underlying population of tours were not improving at all. A cleaner experiment would compare this curve against a control run with $T(t)$ held fixed, isolating the entropy reduction attributable to genuine convergence of the population versus the entropy reduction attributable to the annealing schedule itself.

This limitation is flagged here because it affects how the reported information gain $I(t)$ should be interpreted: it is a gain relative to a particular, temperature-coupled notion of "information," not a pure measure of search progress.

### 3. Why Entropy Does Not Reach Zero
After 50 iterations, $H(t)$ is still around $1.9 \sim 2.0$ bits rather than $0$, indicating that the population has not fully collapsed onto a single tour (or a small cluster of near-identical tours). This is expected given the modest iteration budget ($50$) relative to the population size ($100$) and the relatively slow cooling rate ($0.95$ per iteration). A longer run or faster cooling schedule would be expected to drive $H(t)$ further toward $0$, albeit at a higher risk of premature convergence to a suboptimal tour.

### 4. Connection to Lecture Concepts
This experiment operationalizes the central definition of information as uncertainty reduction ($H = -\sum p_i \log_2 p_i$) in a genuinely dynamic combinatorial-search setting, rather than through an externally-supplied oracle. The use of a Boltzmann/Gibbs-style distribution over tour costs also directly mirrors the mathematical equivalence between Shannon entropy and physical (Boltzmann) entropy ($S = -k_B \sum p_i \log p_i$), here applied to an optimization search rather than a physical ensemble of particles.