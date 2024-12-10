import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb

def newton_method(f, df, z0, max_iter=100, tol=1e-6):
    z = z0
    for i in range(max_iter):
        z_next = z - f(z) / df(z)
        if abs(z_next - z) < tol:
            return z_next, i
        z = z_next
    return z, max_iter

# Define the function and its derivative for more roots
def f(z):
    return z**5 - 1  # Change to any polynomial you want

def df(z):
    return 5*z**4

# Define the grid in the complex plane
re = np.linspace(-2, 2, 1000)
im = np.linspace(-2, 2, 1000)
X, Y = np.meshgrid(re, im)
Z0 = X + 1j * Y

# Compute the roots of the polynomial
roots = [np.exp(2j * np.pi * k / 5) for k in range(5)]  # 5th roots of unity

# Generate colors using HSV color space
colors = hsv_to_rgb([(i / len(roots), 1.0, 1.0) for i in range(len(roots))])

# Apply Newton's method to each point in the grid
root_colors = np.zeros(Z0.shape + (3,))
iterations = np.zeros(Z0.shape)

for i in range(Z0.shape[0]):
    for j in range(Z0.shape[1]):
        root, iter_count = newton_method(f, df, Z0[i, j])
        closest_root = min(roots, key=lambda r: abs(r - root))
        root_index = roots.index(closest_root)
        root_colors[i, j] = colors[root_index]
        iterations[i, j] = iter_count

# Add the iteration count to color intensity
iteration_colors = root_colors * (1 - iterations[..., np.newaxis] / np.max(iterations))

# Plot the fractal
plt.figure(figsize=(10, 10))
plt.imshow(iteration_colors, extent=(-2, 2, -2, 2))
plt.xlabel('Re(z)')
plt.ylabel('Im(z)')
plt.title("Newton's Method in the Complex Plane for 5th Roots of Unity")
plt.show()
