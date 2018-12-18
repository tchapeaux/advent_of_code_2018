"""
SECOND PART LOGIC

Looking at the simulation, it looks like my inputs loops

I can simulate it for a bit and plot the total resource value just to see what's what

(. . .)

When we are at tick=1000, the value loops every 28 ticks

"""

values = [
    235080,  # 972
    235440,  # 973
    236885,  # 974
    235425,  # 975
    236964,  # 976
    232617,  # 977
    229125,  # 978
    217200,  # 979
    209684,  # 980
    199144,  # 981
    196281,  # 982
    191649,  # 983
    189912,  # 984
    185658,  # 985
    184946,  # 986
    188020,  # 987
    191680,  # 988
    194205,  # 989
    198534,  # 990
    201105,  # 991
    206460,  # 992
    209710,  # 993
    215460,  # 994
    216876,  # 995
    222372,  # 996
    223170,  # 997
    229038,  # 998
    230454,  # 999
]

idx = (1000000000 - 972) % 28
print values[idx]
