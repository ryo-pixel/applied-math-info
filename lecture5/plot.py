import matplotlib.pyplot as plt
fig,ax = plt.subplots(figsize=(6,4))

positions = {
     "M0": (0, 1),
    "M-": (-1, 0),
    "M+": (1, 0)
}

for label, (x ,y) in positions.items():
    ax.scatter(x ,y, s=700  , color='skyblue', edgecolor='black')
    ax.text(x, y, label, ha='center', va='center', fontsize=12)
    
ax.annotate(
        "",
        xy=(-1,0.1),
        xytext=(-0.1, 0.9),
        arrowprops=dict(arrowstyle='->', lw=2)
    )
    
ax.annotate(
    "",
    xy=(1,0.1),
    xytext=(0.1,0.9),
    arrowprops=dict(arrowstyle="->", lw=2)
)
    
ax.set_title("Morse Decomposition of $\\dot{x}=x-x^3$")

ax.set_xlim(-2, 2)
ax.set_ylim(-0.5, 1.5)
ax.axis('off')

plt.tight_layout
plt.show()