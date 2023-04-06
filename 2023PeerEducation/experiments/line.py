import matplotlib.pyplot as plt

if __name__ == "__main__":
    dy = [[0, 0, 9], [0.2, 549, 554], [0.4, 1000, 1000], [0.6, 1000, 1000], [0.8, 1000, 1000], [1, 1000, 1000]]


    y1 = [0, 0.549, 1, 1, 1, 1]
    x1 = [0, 0.2, 0.4, 0.6, 0.8, 1]
    y2 = [0, 0.554, 1, 1, 1, 1]
    plt.plot(x1, y1, label='behaviors', linewidth=3, color='r', marker='o',
             markerfacecolor='blue', markersize=12)
    plt.plot(x1, y2, label='emotions')
    plt.xlabel('pressure degrees')
    plt.ylabel('Proportion of joint behaviors and emotions')
    plt.legend()
    plt.show()
    plt.savefig("figures/fc.png")
