import matplotlib.pyplot as plt

# Example values for illustrating IIT concepts
systems = ["Independent\nSystem", "Integrated\nSystem"]
phi_values = [0.2, 1.0]

plt.figure(figsize=(6, 4))
bars = plt.bar(systems, phi_values)

plt.title("Illustration of Integrated Information in a Smart Home")
plt.xlabel("System Type")
plt.ylabel("Illustrative Integrated Information (Φ)")
plt.ylim(0, 1.2)

# Display values on top of each bar
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.03,
        f"{height:.1f}",
        ha="center"
    )

plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.show()