import numpy as np
import pybullet as p
from robot_env import RobotEnv  # 假设你的环境类在robot_env.py中

def test_robot_env(total_steps=2000, render=True, slow_down_factor=2.0):
    """测试机器人环境的函数，专注于可视化机器人运动"""
    # 创建环境实例
    env = RobotEnv(render=render)
    
    # 重置环境
    max_pos_z = -np.inf  # 初始最大高度
    observation = env.reset()
    
    # 执行动作并观察结果
    for step in range(total_steps):
        # 生成随机动作（在-1到1之间）
        action = np.random.uniform(-1, 1, size=env.action_dim)
        
        # 执行动作
        observation, reward, done, info = env.step(action)
        position, _ = p.getBasePositionAndOrientation(env.robotId)
        pos_z = position[2]

        if pos_z > max_pos_z:
            max_pos_z = pos_z
            max_step = step
        
        # 打印简要信息（每100步一次）
        if step % 100 == 0:
            print(f"步骤: {step}, 奖励: {reward:.4f}")
            
            print(f"躯干高度: {position[2]:.3f}米，当前最高: {max_pos_z:.3f} 米")
        
        # 如果机器人摔倒，重置环境
        if done:
            print(f"机器人在步骤 {step} 摔倒，重置环境")
            observation = env.reset()
        
        # 控制模拟速度
        if render and slow_down_factor > 0:
            p.configureDebugVisualizer(p.COV_ENABLE_SINGLE_STEP_RENDERING)
            import time
            time.sleep(1.0/240.0 * slow_down_factor)
    
    
    # 关闭环境
    env.close()
    print("测试完成")
    print(f"最高躯干高度: {max_pos_z:.4f} 米（出现在步骤 {max_step}）")

if __name__ == "__main__":
    test_robot_env(render=True, slow_down_factor=2.0)  # 速度减半，便于观察