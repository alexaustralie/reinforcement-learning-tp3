"""
Dans ce TP, nous allons implémenter un agent qui apprend à jouer au jeu Taxi-v3
de OpenAI Gym. Le but du jeu est de déposer un passager à une destination
spécifique en un minimum de temps. Le jeu est composé d'une grille de 5x5 cases
et le taxi peut se déplacer dans les 4 directions (haut, bas, gauche, droite).
Le taxi peut prendre un passager sur une case spécifique et le déposer à une
destination spécifique. Le jeu est terminé lorsque le passager est déposé à la
destination. Le jeu est aussi terminé si le taxi prend plus de 200 actions.

Vous devez implémenter un agent qui apprend à jouer à ce jeu en utilisant
les algorithmes Q-Learning et SARSA.

Pour chaque algorithme, vous devez réaliser une vidéo pour montrer que votre modèle fonctionne.
Vous devez aussi comparer l'efficacité des deux algorithmes en termes de temps
d'apprentissage et de performance.

A la fin, vous devez rendre un rapport qui explique vos choix d'implémentation
et vos résultats (max 1 page).
"""

import typing as t
import gymnasium as gym
import numpy as np
from qlearning import QLearningAgent
from qlearning_eps_scheduling import QLearningAgentEpsScheduling
from sarsa import SARSAAgent
import matplotlib.pyplot as plt

env = gym.make("Taxi-v3", render_mode="rgb_array")
n_actions = env.action_space.n  # type: ignore


def plot_rewards(rewards: list, title: str, filename: str) -> None:
    """
    Function to plot the evolution of rewards over episodes.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(rewards, label='Total Reward')
    plt.xlabel('Episodes')
    plt.ylabel('Total Reward')
    plt.title(title)
    plt.grid()
    plt.legend()
    plt.savefig(filename)
    plt.show()

#################################################
# 1. Play with QLearningAgent
#################################################
env = gym.wrappers.RecordVideo(env, "videos/QLearningAgent",episode_trigger=lambda ep: ep % 100 == 0)
# You can edit these hyperparameters!
agent = QLearningAgent(
    learning_rate=0.5, epsilon=0.1, gamma=0.99, legal_actions=list(range(n_actions))
)


def play_and_train(env: gym.Env, agent: QLearningAgent, t_max=int(1e4)) -> float:
    """
    This function should
    - run a full game, actions given by agent.getAction(s)
    - train agent using agent.update(...) whenever possible
    - return total rewardb
    """
    total_reward: t.SupportsFloat = 0.0
    s, _ = env.reset()

    for _ in range(t_max):
        # Get agent to pick action given state s
        a = agent.get_action(s)

        next_s, r, done, _, _ = env.step(a)

        # Train agent for state s
        # BEGIN SOLUTION
        total_reward += r
        agent.update(s, a, r, next_s)
        s = next_s
        if done:
            break
        # END SOLUTION

    return total_reward


rewards = []
for i in range(1000):
    rewards.append(play_and_train(env, agent))
    if i % 100 == 0:
        print("mean reward QLearningAgent epoch", i, ":", np.mean(rewards[-100:]))

assert np.mean(rewards[-100:]) > 0.0


# TODO: créer des vidéos de l'agent en action
env.close()

#Décomenter pour afficher le graphique
#plot_rewards(rewards, 'QLearning Agent - Evolution of Rewards', 'QLearningAgent_rewards.png')

#################################################
# 2. Play with QLearningAgentEpsScheduling
#################################################
env = gym.make("Taxi-v3", render_mode="rgb_array")
env = gym.wrappers.RecordVideo(env, "videos/QLearningAgentEpsScheduling",episode_trigger=lambda ep: ep % 100 == 0)



agent = QLearningAgentEpsScheduling(
    learning_rate=0.5, epsilon=0.25, gamma=0.99, legal_actions=list(range(n_actions))
)

rewards = []
for i in range(1000):
    rewards.append(play_and_train(env, agent))
    if i % 100 == 0:
        print("mean reward QLearningAgentEpsScheduling epoch", i, ":", np.mean(rewards[-100:]))

assert np.mean(rewards[-100:]) > 0.0


# TODO: créer des vidéos de l'agent en action
env.close()

#Décomenter pour afficher le graphique
#plot_rewards(rewards, 'QLearning Agent with Epsilon Scheduling - Evolution of Rewards', 'QLearningAgentEpsScheduling_rewards.png')

####################
# 3. Play with SARSA
####################
env = gym.make("Taxi-v3", render_mode="rgb_array")
env = gym.wrappers.RecordVideo(env, "videos/SARSA",episode_trigger=lambda ep: ep % 100 == 0)


agent = SARSAAgent(learning_rate=0.5, gamma=0.99, legal_actions=list(range(n_actions)))

rewards = []
for i in range(1000):
    rewards.append(play_and_train(env, agent))
    if i % 100 == 0:
        print("mean reward SARSA epoch", i, ":", np.mean(rewards[-100:]))
env.close()

#Décomenter pour afficher le graphique
#plot_rewards(rewards, 'SARSA Agent - Evolution of Rewards', 'SARSAAgent_rewards.png')
