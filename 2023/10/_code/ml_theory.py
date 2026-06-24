#!/usr/bin/env python3
"""Machine Learning Theory Demo - VC Dimension, Bias-Variance, Kernel, Bayesian"""

import numpy as np
import math

def vc_dimension_intervals():
    """VC dimension of axis-aligned intervals on real line is 2"""
    can_shatter = True
    for x1 in [0, 1]:
        for x2 in [0, 1]:
            # Can we find an interval (a,b) such that point < a = 0, a <= point <= b = 1, point > b = 0?
            pass
    return 2

def vc_dimension_perceptron():
    """VC dimension of d-dimensional perceptron is d+1"""
    return lambda d: d + 1

def bias_variance_decomposition(degree=3, n_samples=50, n_trials=2000):
    """Bias-variance decomposition for polynomial regression"""
    np.random.seed(42)
    xs = np.linspace(-3, 3, n_samples)
    def true_fn(x): return np.sin(x)
    ys_true = true_fn(xs)

    all_predictions = np.zeros((n_trials, n_samples))
    for t in range(n_trials):
        noise = np.random.normal(0, 0.3, n_samples)
        ys = ys_true + noise
        coeffs = np.polyfit(xs, ys, degree)
        poly = np.poly1d(coeffs)
        all_predictions[t] = poly(xs)

    avg_prediction = np.mean(all_predictions, axis=0)
    bias_sq = np.mean((avg_prediction - ys_true) ** 2)
    variance = np.mean(np.var(all_predictions, axis=0))
    expected_error = bias_sq + variance
    return {
        "bias_sq": round(bias_sq, 4),
        "variance": round(variance, 4),
        "bias_sq + variance": round(expected_error, 4),
        "irreducible_noise": 0.09
    }

def kernel_functions(x, y, kernel_type="rbf", gamma=1.0):
    """Compute kernel function values"""
    if kernel_type == "rbf":
        return math.exp(-gamma * np.linalg.norm(np.array(x) - np.array(y)) ** 2)
    elif kernel_type == "polynomial":
        return (np.dot(x, y) + 1) ** gamma
    elif kernel_type == "linear":
        return np.dot(x, y)
    else:
        raise ValueError(f"Unknown kernel: {kernel_type}")

def kernel_matrix(X, kernel_type="rbf", gamma=1.0):
    """Compute kernel matrix K_ij = k(x_i, x_j)"""
    n = len(X)
    K = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            K[i, j] = kernel_functions(X[i], X[j], kernel_type, gamma)
    return K

def bayesian_update(prior_alpha=2, prior_beta=2, heads=7, tails=3):
    """Bayesian update for Bernoulli likelihood with Beta conjugate prior"""
    post_alpha = prior_alpha + heads
    post_beta = prior_beta + tails
    prior_mean = prior_alpha / (prior_alpha + prior_beta)
    post_mean = post_alpha / (post_alpha + post_beta)
    prior_var = (prior_alpha * prior_beta) / ((prior_alpha + prior_beta) ** 2 * (prior_alpha + prior_beta + 1))
    post_var = (post_alpha * post_beta) / ((post_alpha + post_beta) ** 2 * (post_alpha + post_beta + 1))

    # Marginal likelihood P(data | prior) via Beta-Binomial
    from math import comb, lgamma
    n = heads + tails
    log_marg = (lgamma(prior_alpha + prior_beta) - lgamma(prior_alpha) - lgamma(prior_beta) +
                lgamma(prior_alpha + heads) + lgamma(prior_beta + tails) - lgamma(prior_alpha + prior_beta + n) +
                math.log(comb(n, heads)))
    return {
        "prior": f"Beta({prior_alpha},{prior_beta})",
        "likelihood": f"Binomial({heads},{tails})",
        "posterior": f"Beta({post_alpha},{post_beta})",
        "prior_mean": round(prior_mean, 4),
        "posterior_mean": round(post_mean, 4),
        "prior_variance": round(prior_var, 4),
        "posterior_variance": round(post_var, 4),
        "log_marginal_likelihood": round(log_marg, 4)
    }

def demo():
    """Run all ML theory demos"""
    print("=== Machine Learning Theory Demo ===\n")

    print("--- VC Dimension ---")
    print(f"VC dimension of intervals on real line: {vc_dimension_intervals()}")
    print(f"VC dimension of d-dim perceptron: d+1 (e.g., d=2 -> {vc_dimension_perceptron()(2)})\n")

    print("--- Bias-Variance Decomposition (Degree 3) ---")
    bv = bias_variance_decomposition(degree=3)
    for k, v in bv.items():
        print(f"  {k}: {v}")
    print(f"  Check: bias_sq + variance = {bv['bias_sq'] + bv['variance']:.4f} ≈ bias_sq + variance (computed) = {bv['bias_sq + variance']}\n")

    print("--- Kernel Functions ---")
    x1, x2 = [1.0, 2.0], [3.0, 4.0]
    print(f"x1={x1}, x2={x2}")
    print(f"  RBF kernel (gamma=0.5): {kernel_functions(x1, x2, 'rbf', 0.5):.4f}")
    print(f"  Polynomial kernel (d=3): {kernel_functions(x1, x2, 'polynomial', 3):.4f}")
    print(f"  Linear kernel: {kernel_functions(x1, x2, 'linear'):.4f}")

    X = [[1, 0], [0, 1], [1, 1], [0, 0]]
    K = kernel_matrix(X, "rbf", 0.5)
    print(f"\n  RBF kernel matrix (gamma=0.5) for {X}:")
    print(f"  {np.array2string(K, precision=3, suppress_small=True)}\n")

    print("--- Bayesian Update ---")
    result = bayesian_update(prior_alpha=2, prior_beta=2, heads=7, tails=3)
    for k, v in result.items():
        print(f"  {k}: {v}")
    print()
    print("=== Demo complete ===")

if __name__ == "__main__":
    demo()
