# 软件工程 实验报告

| 姓名   | 班级   | 学号   |
| ---- | ---- | ---- |
|      |      |      |
|      |      |      |
|      |      |      |
|      |      |      |

## 如何运行（Python 2.7）

```bash
git clone https://github.com/MartinNey/se-draw-balls.git
cd se-draw-balls
pyvenv .venv
. .venv/bin/activate
pip install -r requirements.txt
python main.py
```

##  算法

+ 将所有的面，点，球抽象为‘限制’，而很容易得知，在满足题设条件的球，必定与四个限制‘相切’（面相切、点在球面上、两个球相切）。
+ 所以这个问题就转换成了，求出，所有四个限制的组合，求出每一个组合中满足条件的球，找到其中半径最大的那个球。


+ 那么开始具体过程
  1. 传进初始的限制`list`（即四条的限制，或者需要添加的障碍点）、你初始添加的圆`list`（默认为空）、需求的圆的个数`number`

  2. 如果圆的列表长度达到了需要的个数，将结果返回，反之继续。

  3. 求目前最大的圆将圆添加进限制列表以及圆列表，将这两个量连同需要圆个数记录下来返回步骤2。

     > 关于如何求最大的圆：
     >
     > 1. 得到所有的四个限制的组合。
     > 2. 求出每个组合中满足条件的圆。
     > 3. 比较得出最大的圆。

  4. 得出结果，进行数据展示以及可视化。

+ 关于优化空间：

  + 求四个限制组合以及最大圆的过程，可以使用动态规划，可以大幅度降低计算量。
  + 目前解方程这个过程是通过库计算的，理论上可以通过手算获取最后的结果表达式，可以大幅降低计算量。
  + 可以将限制的组合，优化为区域，区域间不重复，可以大幅降低计算量，但需要额外判断。


## 测试用例

```python
    # 带了障碍点的情况
    restrictions_3d = [
        Point_3D({ 'x': 40, 'y': 100, 'z': 40 }),
        Coordinate('x', border=0, is_max=False),
        Coordinate('x', border=200, is_max=True),
        Coordinate('y', border=0, is_max=False),
        Coordinate('y', border=200, is_max=True),
        Coordinate('z', border=0, is_max=False),
        Coordinate('z', border=200, is_max=True),
    ]
    # n 为10，24
    balls, restrictions = calculate_3d(n, balls, restrictions_3d, real_time_callback=lambda ball: print(ball.dictify()))
    # 没带障碍点的情况
        restrictions_2d = [
        Point_2D({ 'x': 40, 'y': 100 }),
        Coordinate('x', border=0, is_max=False),
        Coordinate('x', border=200, is_max=True),
        Coordinate('y', border=0, is_max=False),
        Coordinate('y', border=200, is_max=True),
    ]
    # n 为10，24，50
    circles, restrictions = calculate_2d(n, circles, restrictions_2d, real_time_callback=lambda circle: print(circle.dictify()))

```

