import Card
import TwoPocketLookup as twp

def evalPocket(card1, card2):
    v1 = card1.value - 2
    v2 = card2.value - 2

    # Are hole cards suited?
    suited = card2.suit != card1.suit
    index1 = min(v1,v2)
    index2 = max(v1,v2) - index1

    return lookuphand[index1][index2][suited]

lookuphand =   [
                    [#2
                        [-1, 306],#2
                        [238, 197],#3
                        [246, 206],#4
                        [254, 214],#5
                        [248, 207],#6
                        [245, 204],#7
                        [258, 217],#8
                        [270, 230],#9
                        [286, 247],#10
                        [303, 264],#11
                        [323, 286],#12
                        [348, 311],#13
                        [388, 352],#14
                    ],
                    [#3
                        [-1, 336],#3
                        [264, 225],#4
                        [272, 234],#5
                        [266, 227],#6
                        [264, 224],#7
                        [263, 223],#8
                        [278, 239],#9
                        [294, 255],#10
                        [312, 273],#11
                        [331, 294],#12
                        [357, 320],#13
                        [396, 362],#14
                    ],
                    [#4
                        [-1, 367],#4
                        [290, 253],#5
                        [285, 247],#6
                        [282, 244],#7
                        [282, 243],#8
                        [283, 245],#9
                        [302, 264],#10
                        [318, 282],#11
                        [340, 303],#12
                        [365, 329],#13
                        [405, 372],#14
                    ],
                    [#5
                        [-1, 400],#5
                        [302, 266],#6
                        [301, 265],#7
                        [300, 264],#8
                        [302, 265],#9
                        [308, 270],#10
                        [327, 291],#11
                        [348, 312],#12
                        [374, 339],#13
                        [415, 381],#14
                    ],
                    [#6
                        [-1, 431],#6
                        [318, 284],#7
                        [319, 284],#8
                        [320, 286],#9
                        [326, 291],#10
                        [333, 298],#11
                        [357, 322],#12
                        [382, 349],#13
                        [411, 379],#14
                    ],
                    [#7
                        [-1, 464],#7
                        [337, 304],#8
                        [341, 306],#9
                        [346, 312],#10
                        [353, 318],#11
                        [365, 330],#12
                        [392, 359],#13
                        [423, 392],#14
                    ],
                    [#8
                        [-1, 499],#8
                        [359, 327],#9
                        [366, 334],#10
                        [374, 341],#11
                        [385, 352],#12
                        [402, 369],#13
                        [435, 404],#14
                    ],
                    [#9
                        [-1, 536],#9
                        [387, 356],#10
                        [394, 363],#11
                        [406, 375],#12
                        [423, 392],#13
                        [445, 415],#14
                    ],
                    [#10
                        [-1, 575],#10
                        [419, 390],#11
                        [431, 401],#12
                        [448, 419],#13
                        [471, 442],#14
                    ],
                    [#11
                        [-1, 611],#11
                        [442, 413],#12
                        [458, 430],#13
                        [482, 455],#14
                    ],
                    [#12
                        [-1, 649],#12
                        [470, 443],#13
                        [494, 468],#14
                    ],
                    [#13
                        [-1, 688],#13
                        [506, 482],#14
                    ],
                    [#14
                        [-1, 734],#14
                    ],
                ]

if __name__ == "__main__":
    lookupvalue = [[] for j in range(1000)]
    cards = []
    values = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
    suits = ['s','c','h','d']
    for i,v1 in enumerate(values):
        for j,s1 in enumerate(suits):
            card1 = Card.Card(v1+s1)
            for v2 in values[i+1:]:
                for s2 in suits:
                    card2 = Card.Card(v2+s2)
                    cards += [(card1,card2)]
            for s2 in suits[j+1:]:
                card2 = Card.Card(v1+s2)
                cards += [(card1,card2)]
    print len(cards)
    for c in cards:
        lookupvalue[evalPocket(*c)] += [(c[0].stringValue,c[1].stringValue)]
    print lookupvalue[482]
    print lookupvalue[734]
    #with open("reverse3lookup.txt",'w') as f:
    #    f.write(str(lookupvalue))
    lookupvalue = [[] for j in range(1000)]
    for c in cards:
        lookupvalue[twp.evalPocket(*c)] += [(c[0].stringValue,c[1].stringValue)]
    #with open("reverse2lookup.txt",'w') as f:
    #    f.write(str(lookupvalue))

lookupvalue = [[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[('2s', '3c'), ('2s', '3h'), ('2s', '3d'), ('2c', '3s'), ('2c', '3h'), ('2c', '3d'), ('2h', '3s'), ('2h', '3c'), ('2h', '3d'), ('2d', '3s'), ('2d', '3c'), ('2d', '3h')],
[],
[],
[],
[],
[],
[],
[('2s', '7c'), ('2s', '7h'), ('2s', '7d'), ('2c', '7s'), ('2c', '7h'), ('2c', '7d'), ('2h', '7s'), ('2h', '7c'), ('2h', '7d'), ('2d', '7s'), ('2d', '7c'), ('2d', '7h')],
[],
[('2s', '4c'), ('2s', '4h'), ('2s', '4d'), ('2c', '4s'), ('2c', '4h'), ('2c', '4d'), ('2h', '4s'), ('2h', '4c'), ('2h', '4d'), ('2d', '4s'), ('2d', '4c'), ('2d', '4h')],
[('2s', '6c'), ('2s', '6h'), ('2s', '6d'), ('2c', '6s'), ('2c', '6h'), ('2c', '6d'), ('2h', '6s'), ('2h', '6c'), ('2h', '6d'), ('2d', '6s'), ('2d', '6c'), ('2d', '6h')],
[],
[],
[],
[],
[],
[],
[('2s', '5c'), ('2s', '5h'), ('2s', '5d'), ('2c', '5s'), ('2c', '5h'), ('2c', '5d'), ('2h', '5s'), ('2h', '5c'), ('2h', '5d'), ('2d', '5s'), ('2d', '5c'), ('2d', '5h')],
[],
[],
[('2s', '8c'), ('2s', '8h'), ('2s', '8d'), ('2c', '8s'), ('2c', '8h'), ('2c', '8d'), ('2h', '8s'), ('2h', '8c'), ('2h', '8d'), ('2d', '8s'), ('2d', '8c'), ('2d', '8h')],
[],
[],
[],
[],
[],
[('3s', '8c'), ('3s', '8h'), ('3s', '8d'), ('3c', '8s'), ('3c', '8h'), ('3c', '8d'), ('3h', '8s'), ('3h', '8c'), ('3h', '8d'), ('3d', '8s'), ('3d', '8c'), ('3d', '8h')],
[('3s', '7c'), ('3s', '7h'), ('3s', '7d'), ('3c', '7s'), ('3c', '7h'), ('3c', '7d'), ('3h', '7s'), ('3h', '7c'), ('3h', '7d'), ('3d', '7s'), ('3d', '7c'), ('3d', '7h')],
[('3s', '4c'), ('3s', '4h'), ('3s', '4d'), ('3c', '4s'), ('3c', '4h'), ('3c', '4d'), ('3h', '4s'), ('3h', '4c'), ('3h', '4d'), ('3d', '4s'), ('3d', '4c'), ('3d', '4h')],
[],
[('3s', '6c'), ('3s', '6h'), ('3s', '6d'), ('3c', '6s'), ('3c', '6h'), ('3c', '6d'), ('3h', '6s'), ('3h', '6c'), ('3h', '6d'), ('3d', '6s'), ('3d', '6c'), ('3d', '6h')],
[],
[],
[('2s', '9c'), ('2s', '9h'), ('2s', '9d'), ('2c', '9s'), ('2c', '9h'), ('2c', '9d'), ('2h', '9s'), ('2h', '9c'), ('2h', '9d'), ('2d', '9s'), ('2d', '9c'), ('2d', '9h')],
[],
[],
[],
[('3s', '5c'), ('3s', '5h'), ('3s', '5d'), ('3c', '5s'), ('3c', '5h'), ('3c', '5d'), ('3h', '5s'), ('3h', '5c'), ('3h', '5d'), ('3d', '5s'), ('3d', '5c'), ('3d', '5h')],
[],
[],
[],
[('2s', '3s'), ('2c', '3c'), ('2h', '3h'), ('2d', '3d')],
[('3s', '9c'), ('3s', '9h'), ('3s', '9d'), ('3c', '9s'), ('3c', '9h'), ('3c', '9d'), ('3h', '9s'), ('3h', '9c'), ('3h', '9d'), ('3d', '9s'), ('3d', '9c'), ('3d', '9h')],
[],
[],
[],
[('4s', '8c'), ('4s', '8h'), ('4s', '8d'), ('4c', '8s'), ('4c', '8h'), ('4c', '8d'), ('4h', '8s'), ('4h', '8c'), ('4h', '8d'), ('4d', '8s'), ('4d', '8c'), ('4d', '8h')],
[('4s', '7c'), ('4s', '7h'), ('4s', '7d'), ('4c', '7s'), ('4c', '7h'), ('4c', '7d'), ('4h', '7s'), ('4h', '7c'), ('4h', '7d'), ('4d', '7s'), ('4d', '7c'), ('4d', '7h')],
[('2s', '7s'), ('2c', '7c'), ('2h', '7h'), ('2d', '7d'), ('4s', '9c'), ('4s', '9h'), ('4s', '9d'), ('4c', '9s'), ('4c', '9h'), ('4c', '9d'), ('4h', '9s'), ('4h', '9c'), ('4h', '9d'), ('4d', '9s'), ('4d', '9c'), ('4d', '9h')],
[('2s', '4s'), ('2c', '4c'), ('2h', '4h'), ('2d', '4d')],
[('2s', 'Tc'), ('2s', 'Th'), ('2s', 'Td'), ('2c', 'Ts'), ('2c', 'Th'), ('2c', 'Td'), ('2h', 'Ts'), ('2h', 'Tc'), ('2h', 'Td'), ('2d', 'Ts'), ('2d', 'Tc'), ('2d', 'Th'), ('4s', '6c'), ('4s', '6h'), ('4s', '6d'), ('4c', '6s'), ('4c', '6h'), ('4c', '6d'), ('4h', '6s'), ('4h', '6c'), ('4h', '6d'), ('4d', '6s'), ('4d', '6c'), ('4d', '6h')],
[('2s', '6s'), ('2c', '6c'), ('2h', '6h'), ('2d', '6d')],
[],
[],
[],
[],
[('4s', '5c'), ('4s', '5h'), ('4s', '5d'), ('4c', '5s'), ('4c', '5h'), ('4c', '5d'), ('4h', '5s'), ('4h', '5c'), ('4h', '5d'), ('4d', '5s'), ('4d', '5c'), ('4d', '5h')],
[('2s', '5s'), ('2c', '5c'), ('2h', '5h'), ('2d', '5d')],
[('3s', 'Tc'), ('3s', 'Th'), ('3s', 'Td'), ('3c', 'Ts'), ('3c', 'Th'), ('3c', 'Td'), ('3h', 'Ts'), ('3h', 'Tc'), ('3h', 'Td'), ('3d', 'Ts'), ('3d', 'Tc'), ('3d', 'Th')],
[],
[],
[('2s', '8s'), ('2c', '8c'), ('2h', '8h'), ('2d', '8d')],
[],
[],
[],
[],
[('3s', '8s'), ('3c', '8c'), ('3h', '8h'), ('3d', '8d')],
[('2s', 'Jc'), ('2s', 'Jh'), ('2s', 'Jd'), ('2c', 'Js'), ('2c', 'Jh'), ('2c', 'Jd'), ('2h', 'Js'), ('2h', 'Jc'), ('2h', 'Jd'), ('2d', 'Js'), ('2d', 'Jc'), ('2d', 'Jh'), ('3s', '4s'), ('3s', '7s'), ('3c', '4c'), ('3c', '7c'), ('3h', '4h'), ('3h', '7h'), ('3d', '4d'), ('3d', '7d'), ('4s', 'Tc'), ('4s', 'Th'), ('4s', 'Td'), ('4c', 'Ts'), ('4c', 'Th'), ('4c', 'Td'), ('4h', 'Ts'), ('4h', 'Tc'), ('4h', 'Td'), ('4d', 'Ts'), ('4d', 'Tc'), ('4d', 'Th'), ('5s', '8c'), ('5s', '8h'), ('5s', '8d'), ('5c', '8s'), ('5c', '8h'), ('5c', '8d'), ('5h', '8s'), ('5h', '8c'), ('5h', '8d'), ('5d', '8s'), ('5d', '8c'), ('5d', '8h')],
[('5s', '7c'), ('5s', '7h'), ('5s', '7d'), ('5s', '9c'), ('5s', '9h'), ('5s', '9d'), ('5c', '7s'), ('5c', '7h'), ('5c', '7d'), ('5c', '9s'), ('5c', '9h'), ('5c', '9d'), ('5h', '7s'), ('5h', '7c'), ('5h', '7d'), ('5h', '9s'), ('5h', '9c'), ('5h', '9d'), ('5d', '7s'), ('5d', '7c'), ('5d', '7h'), ('5d', '9s'), ('5d', '9c'), ('5d', '9h')],
[('3s', '6s'), ('3c', '6c'), ('3h', '6h'), ('3d', '6d'), ('5s', '6c'), ('5s', '6h'), ('5s', '6d'), ('5c', '6s'), ('5c', '6h'), ('5c', '6d'), ('5h', '6s'), ('5h', '6c'), ('5h', '6d'), ('5d', '6s'), ('5d', '6c'), ('5d', '6h')],
[],
[],
[],
[('2s', '9s'), ('2c', '9c'), ('2h', '9h'), ('2d', '9d'), ('5s', 'Tc'), ('5s', 'Th'), ('5s', 'Td'), ('5c', 'Ts'), ('5c', 'Th'), ('5c', 'Td'), ('5h', 'Ts'), ('5h', 'Tc'), ('5h', 'Td'), ('5d', 'Ts'), ('5d', 'Tc'), ('5d', 'Th')],
[],
[('3s', '5s'), ('3c', '5c'), ('3h', '5h'), ('3d', '5d')],
[('3s', 'Jc'), ('3s', 'Jh'), ('3s', 'Jd'), ('3c', 'Js'), ('3c', 'Jh'), ('3c', 'Jd'), ('3h', 'Js'), ('3h', 'Jc'), ('3h', 'Jd'), ('3d', 'Js'), ('3d', 'Jc'), ('3d', 'Jh')],
[],
[],
[],
[],
[('3s', '9s'), ('3c', '9c'), ('3h', '9h'), ('3d', '9d')],
[],
[],
[],
[('4s', '7s'), ('4s', '8s'), ('4s', 'Jc'), ('4s', 'Jh'), ('4s', 'Jd'), ('4c', '7c'), ('4c', '8c'), ('4c', 'Js'), ('4c', 'Jh'), ('4c', 'Jd'), ('4h', '7h'), ('4h', '8h'), ('4h', 'Js'), ('4h', 'Jc'), ('4h', 'Jd'), ('4d', '7d'), ('4d', '8d'), ('4d', 'Js'), ('4d', 'Jc'), ('4d', 'Jh')],
[('4s', '9s'), ('4c', '9c'), ('4h', '9h'), ('4d', '9d')],
[('6s', '7c'), ('6s', '7h'), ('6s', '7d'), ('6s', '8c'), ('6s', '8h'), ('6s', '8d'), ('6c', '7s'), ('6c', '7h'), ('6c', '7d'), ('6c', '8s'), ('6c', '8h'), ('6c', '8d'), ('6h', '7s'), ('6h', '7c'), ('6h', '7d'), ('6h', '8s'), ('6h', '8c'), ('6h', '8d'), ('6d', '7s'), ('6d', '7c'), ('6d', '7h'), ('6d', '8s'), ('6d', '8c'), ('6d', '8h')],
[('4s', '6s'), ('4c', '6c'), ('4h', '6h'), ('4d', '6d')],
[('2s', 'Ts'), ('2s', 'Qc'), ('2s', 'Qh'), ('2s', 'Qd'), ('2c', 'Tc'), ('2c', 'Qs'), ('2c', 'Qh'), ('2c', 'Qd'), ('2h', 'Th'), ('2h', 'Qs'), ('2h', 'Qc'), ('2h', 'Qd'), ('2d', 'Td'), ('2d', 'Qs'), ('2d', 'Qc'), ('2d', 'Qh'), ('6s', '9c'), ('6s', '9h'), ('6s', '9d'), ('6c', '9s'), ('6c', '9h'), ('6c', '9d'), ('6h', '9s'), ('6h', '9c'), ('6h', '9d'), ('6d', '9s'), ('6d', '9c'), ('6d', '9h')],
[],
[],
[],
[('4s', '5s'), ('4c', '5c'), ('4h', '5h'), ('4d', '5d')],
[('5s', 'Jc'), ('5s', 'Jh'), ('5s', 'Jd'), ('5c', 'Js'), ('5c', 'Jh'), ('5c', 'Jd'), ('5h', 'Js'), ('5h', 'Jc'), ('5h', 'Jd'), ('5d', 'Js'), ('5d', 'Jc'), ('5d', 'Jh'), ('6s', 'Tc'), ('6s', 'Th'), ('6s', 'Td'), ('6c', 'Ts'), ('6c', 'Th'), ('6c', 'Td'), ('6h', 'Ts'), ('6h', 'Tc'), ('6h', 'Td'), ('6d', 'Ts'), ('6d', 'Tc'), ('6d', 'Th')],
[],
[],
[('3s', 'Ts'), ('3s', 'Qc'), ('3s', 'Qh'), ('3s', 'Qd'), ('3c', 'Tc'), ('3c', 'Qs'), ('3c', 'Qh'), ('3c', 'Qd'), ('3h', 'Th'), ('3h', 'Qs'), ('3h', 'Qc'), ('3h', 'Qd'), ('3d', 'Td'), ('3d', 'Qs'), ('3d', 'Qc'), ('3d', 'Qh')],
[],
[],
[],
[('6s', 'Jc'), ('6s', 'Jh'), ('6s', 'Jd'), ('6c', 'Js'), ('6c', 'Jh'), ('6c', 'Jd'), ('6h', 'Js'), ('6h', 'Jc'), ('6h', 'Jd'), ('6d', 'Js'), ('6d', 'Jc'), ('6d', 'Jh')],
[],
[('5s', '8s'), ('5c', '8c'), ('5h', '8h'), ('5d', '8d')],
[('5s', '7s'), ('5c', '7c'), ('5h', '7h'), ('5d', '7d')],
[('4s', 'Ts'), ('4c', 'Tc'), ('4h', 'Th'), ('4d', 'Td'), ('5s', '6s'), ('5s', '9s'), ('5c', '6c'), ('5c', '9c'), ('5h', '6h'), ('5h', '9h'), ('5d', '6d'), ('5d', '9d')],
[('2s', 'Js'), ('2c', 'Jc'), ('2h', 'Jh'), ('2d', 'Jd'), ('4s', 'Qc'), ('4s', 'Qh'), ('4s', 'Qd'), ('4c', 'Qs'), ('4c', 'Qh'), ('4c', 'Qd'), ('4h', 'Qs'), ('4h', 'Qc'), ('4h', 'Qd'), ('4d', 'Qs'), ('4d', 'Qc'), ('4d', 'Qh')],
[('7s', '8c'), ('7s', '8h'), ('7s', '8d'), ('7c', '8s'), ('7c', '8h'), ('7c', '8d'), ('7h', '8s'), ('7h', '8c'), ('7h', '8d'), ('7d', '8s'), ('7d', '8c'), ('7d', '8h')],
[],
[('2s', '2c'), ('2s', '2h'), ('2s', '2d'), ('2c', '2h'), ('2c', '2d'), ('2h', '2d'), ('7s', '9c'), ('7s', '9h'), ('7s', '9d'), ('7c', '9s'), ('7c', '9h'), ('7c', '9d'), ('7h', '9s'), ('7h', '9c'), ('7h', '9d'), ('7d', '9s'), ('7d', '9c'), ('7d', '9h')],
[],
[('5s', 'Ts'), ('5c', 'Tc'), ('5h', 'Th'), ('5d', 'Td')],
[],
[],
[('2s', 'Kc'), ('2s', 'Kh'), ('2s', 'Kd'), ('2c', 'Ks'), ('2c', 'Kh'), ('2c', 'Kd'), ('2h', 'Ks'), ('2h', 'Kc'), ('2h', 'Kd'), ('2d', 'Ks'), ('2d', 'Kc'), ('2d', 'Kh')],
[('3s', 'Js'), ('3c', 'Jc'), ('3h', 'Jh'), ('3d', 'Jd'), ('5s', 'Qc'), ('5s', 'Qh'), ('5s', 'Qd'), ('5c', 'Qs'), ('5c', 'Qh'), ('5c', 'Qd'), ('5h', 'Qs'), ('5h', 'Qc'), ('5h', 'Qd'), ('5d', 'Qs'), ('5d', 'Qc'), ('5d', 'Qh'), ('7s', 'Tc'), ('7s', 'Th'), ('7s', 'Td'), ('7c', 'Ts'), ('7c', 'Th'), ('7c', 'Td'), ('7h', 'Ts'), ('7h', 'Tc'), ('7h', 'Td'), ('7d', 'Ts'), ('7d', 'Tc'), ('7d', 'Th')],
[],
[],
[],
[],
[],
[('4s', 'Js'), ('4c', 'Jc'), ('4h', 'Jh'), ('4d', 'Jd'), ('6s', '7s'), ('6c', '7c'), ('6h', '7h'), ('6d', '7d'), ('7s', 'Jc'), ('7s', 'Jh'), ('7s', 'Jd'), ('7c', 'Js'), ('7c', 'Jh'), ('7c', 'Jd'), ('7h', 'Js'), ('7h', 'Jc'), ('7h', 'Jd'), ('7d', 'Js'), ('7d', 'Jc'), ('7d', 'Jh')],
[('6s', '8s'), ('6c', '8c'), ('6h', '8h'), ('6d', '8d')],
[('3s', 'Kc'), ('3s', 'Kh'), ('3s', 'Kd'), ('3c', 'Ks'), ('3c', 'Kh'), ('3c', 'Kd'), ('3h', 'Ks'), ('3h', 'Kc'), ('3h', 'Kd'), ('3d', 'Ks'), ('3d', 'Kc'), ('3d', 'Kh'), ('6s', '9s'), ('6c', '9c'), ('6h', '9h'), ('6d', '9d')],
[],
[('6s', 'Qc'), ('6s', 'Qh'), ('6s', 'Qd'), ('6c', 'Qs'), ('6c', 'Qh'), ('6c', 'Qd'), ('6h', 'Qs'), ('6h', 'Qc'), ('6h', 'Qd'), ('6d', 'Qs'), ('6d', 'Qc'), ('6d', 'Qh')],
[('2s', 'Qs'), ('2c', 'Qc'), ('2h', 'Qh'), ('2d', 'Qd')],
[],
[],
[('6s', 'Ts'), ('6c', 'Tc'), ('6h', 'Th'), ('6d', 'Td')],
[('5s', 'Js'), ('5c', 'Jc'), ('5h', 'Jh'), ('5d', 'Jd'), ('8s', '9c'), ('8s', '9h'), ('8s', '9d'), ('8c', '9s'), ('8c', '9h'), ('8c', '9d'), ('8h', '9s'), ('8h', '9c'), ('8h', '9d'), ('8d', '9s'), ('8d', '9c'), ('8d', '9h')],
[],
[('4s', 'Kc'), ('4s', 'Kh'), ('4s', 'Kd'), ('4c', 'Ks'), ('4c', 'Kh'), ('4c', 'Kd'), ('4h', 'Ks'), ('4h', 'Kc'), ('4h', 'Kd'), ('4d', 'Ks'), ('4d', 'Kc'), ('4d', 'Kh')],
[('7s', 'Qc'), ('7s', 'Qh'), ('7s', 'Qd'), ('7c', 'Qs'), ('7c', 'Qh'), ('7c', 'Qd'), ('7h', 'Qs'), ('7h', 'Qc'), ('7h', 'Qd'), ('7d', 'Qs'), ('7d', 'Qc'), ('7d', 'Qh')],
[('3s', 'Qs'), ('3c', 'Qc'), ('3h', 'Qh'), ('3d', 'Qd')],
[],
[('6s', 'Js'), ('6c', 'Jc'), ('6h', 'Jh'), ('6d', 'Jd')],
[('8s', 'Tc'), ('8s', 'Th'), ('8s', 'Td'), ('8c', 'Ts'), ('8c', 'Th'), ('8c', 'Td'), ('8h', 'Ts'), ('8h', 'Tc'), ('8h', 'Td'), ('8d', 'Ts'), ('8d', 'Tc'), ('8d', 'Th')],
[],
[('3s', '3c'), ('3s', '3h'), ('3s', '3d'), ('3c', '3h'), ('3c', '3d'), ('3h', '3d')],
[('7s', '8s'), ('7c', '8c'), ('7h', '8h'), ('7d', '8d')],
[],
[('5s', 'Kc'), ('5s', 'Kh'), ('5s', 'Kd'), ('5c', 'Ks'), ('5c', 'Kh'), ('5c', 'Kd'), ('5h', 'Ks'), ('5h', 'Kc'), ('5h', 'Kd'), ('5d', 'Ks'), ('5d', 'Kc'), ('5d', 'Kh')],
[('4s', 'Qs'), ('4c', 'Qc'), ('4h', 'Qh'), ('4d', 'Qd')],
[('7s', '9s'), ('7c', '9c'), ('7h', '9h'), ('7d', '9d'), ('8s', 'Jc'), ('8s', 'Jh'), ('8s', 'Jd'), ('8c', 'Js'), ('8c', 'Jh'), ('8c', 'Jd'), ('8h', 'Js'), ('8h', 'Jc'), ('8h', 'Jd'), ('8d', 'Js'), ('8d', 'Jc'), ('8d', 'Jh')],
[],
[],
[],
[],
[('7s', 'Ts'), ('7c', 'Tc'), ('7h', 'Th'), ('7d', 'Td')],
[],
[('2s', 'Ks'), ('2c', 'Kc'), ('2h', 'Kh'), ('2d', 'Kd'), ('5s', 'Qs'), ('5c', 'Qc'), ('5h', 'Qh'), ('5d', 'Qd')],
[('6s', 'Kc'), ('6s', 'Kh'), ('6s', 'Kd'), ('6c', 'Ks'), ('6c', 'Kh'), ('6c', 'Kd'), ('6h', 'Ks'), ('6h', 'Kc'), ('6h', 'Kd'), ('6d', 'Ks'), ('6d', 'Kc'), ('6d', 'Kh')],
[],
[],
[('2s', 'Ac'), ('2s', 'Ah'), ('2s', 'Ad'), ('2c', 'As'), ('2c', 'Ah'), ('2c', 'Ad'), ('2h', 'As'), ('2h', 'Ac'), ('2h', 'Ad'), ('2d', 'As'), ('2d', 'Ac'), ('2d', 'Ah'), ('8s', 'Qc'), ('8s', 'Qh'), ('8s', 'Qd'), ('8c', 'Qs'), ('8c', 'Qh'), ('8c', 'Qd'), ('8h', 'Qs'), ('8h', 'Qc'), ('8h', 'Qd'), ('8d', 'Qs'), ('8d', 'Qc'), ('8d', 'Qh')],
[('7s', 'Js'), ('7c', 'Jc'), ('7h', 'Jh'), ('7d', 'Jd')],
[],
[],
[('9s', 'Tc'), ('9s', 'Th'), ('9s', 'Td'), ('9c', 'Ts'), ('9c', 'Th'), ('9c', 'Td'), ('9h', 'Ts'), ('9h', 'Tc'), ('9h', 'Td'), ('9d', 'Ts'), ('9d', 'Tc'), ('9d', 'Th')],
[('3s', 'Ks'), ('3c', 'Kc'), ('3h', 'Kh'), ('3d', 'Kd'), ('6s', 'Qs'), ('6c', 'Qc'), ('6h', 'Qh'), ('6d', 'Qd')],
[],
[('7s', 'Kc'), ('7s', 'Kh'), ('7s', 'Kd'), ('7c', 'Ks'), ('7c', 'Kh'), ('7c', 'Kd'), ('7h', 'Ks'), ('7h', 'Kc'), ('7h', 'Kd'), ('7d', 'Ks'), ('7d', 'Kc'), ('7d', 'Kh'), ('8s', '9s'), ('8c', '9c'), ('8h', '9h'), ('8d', '9d')],
[],
[],
[('3s', 'Ac'), ('3s', 'Ah'), ('3s', 'Ad'), ('3c', 'As'), ('3c', 'Ah'), ('3c', 'Ad'), ('3h', 'As'), ('3h', 'Ac'), ('3h', 'Ad'), ('3d', 'As'), ('3d', 'Ac'), ('3d', 'Ah')],
[('9s', 'Jc'), ('9s', 'Jh'), ('9s', 'Jd'), ('9c', 'Js'), ('9c', 'Jh'), ('9c', 'Jd'), ('9h', 'Js'), ('9h', 'Jc'), ('9h', 'Jd'), ('9d', 'Js'), ('9d', 'Jc'), ('9d', 'Jh')],
[],
[('4s', 'Ks'), ('4c', 'Kc'), ('4h', 'Kh'), ('4d', 'Kd'), ('7s', 'Qs'), ('7c', 'Qc'), ('7h', 'Qh'), ('7d', 'Qd')],
[('8s', 'Ts'), ('8c', 'Tc'), ('8h', 'Th'), ('8d', 'Td')],
[('4s', '4c'), ('4s', '4h'), ('4s', '4d'), ('4c', '4h'), ('4c', '4d'), ('4h', '4d')],
[],
[('8s', 'Kc'), ('8s', 'Kh'), ('8s', 'Kd'), ('8c', 'Ks'), ('8c', 'Kh'), ('8c', 'Kd'), ('8h', 'Ks'), ('8h', 'Kc'), ('8h', 'Kd'), ('8d', 'Ks'), ('8d', 'Kc'), ('8d', 'Kh')],
[],
[],
[('4s', 'Ac'), ('4s', 'Ah'), ('4s', 'Ad'), ('4c', 'As'), ('4c', 'Ah'), ('4c', 'Ad'), ('4h', 'As'), ('4h', 'Ac'), ('4h', 'Ad'), ('4d', 'As'), ('4d', 'Ac'), ('4d', 'Ah')],
[],
[('5s', 'Ks'), ('5c', 'Kc'), ('5h', 'Kh'), ('5d', 'Kd'), ('8s', 'Js'), ('8c', 'Jc'), ('8h', 'Jh'), ('8d', 'Jd')],
[('9s', 'Qc'), ('9s', 'Qh'), ('9s', 'Qd'), ('9c', 'Qs'), ('9c', 'Qh'), ('9c', 'Qd'), ('9h', 'Qs'), ('9h', 'Qc'), ('9h', 'Qd'), ('9d', 'Qs'), ('9d', 'Qc'), ('9d', 'Qh')],
[],
[],
[],
[('6s', 'Ac'), ('6s', 'Ah'), ('6s', 'Ad'), ('6c', 'As'), ('6c', 'Ah'), ('6c', 'Ad'), ('6h', 'As'), ('6h', 'Ac'), ('6h', 'Ad'), ('6d', 'As'), ('6d', 'Ac'), ('6d', 'Ah')],
[],
[('5s', 'Ac'), ('5s', 'Ah'), ('5s', 'Ad'), ('5c', 'As'), ('5c', 'Ah'), ('5c', 'Ad'), ('5h', 'As'), ('5h', 'Ac'), ('5h', 'Ad'), ('5d', 'As'), ('5d', 'Ac'), ('5d', 'Ah')],
[('6s', 'Ks'), ('6c', 'Kc'), ('6h', 'Kh'), ('6d', 'Kd')],
[],
[],
[('8s', 'Qs'), ('8c', 'Qc'), ('8h', 'Qh'), ('8d', 'Qd')],
[],
[('9s', 'Ts'), ('9c', 'Tc'), ('9h', 'Th'), ('9d', 'Td')],
[('2s', 'As'), ('2c', 'Ac'), ('2h', 'Ah'), ('2d', 'Ad')],
[],
[('Ts', 'Jc'), ('Ts', 'Jh'), ('Ts', 'Jd'), ('Tc', 'Js'), ('Tc', 'Jh'), ('Tc', 'Jd'), ('Th', 'Js'), ('Th', 'Jc'), ('Th', 'Jd'), ('Td', 'Js'), ('Td', 'Jc'), ('Td', 'Jh')],
[],
[('7s', 'Ks'), ('7s', 'Ac'), ('7s', 'Ah'), ('7s', 'Ad'), ('7c', 'Kc'), ('7c', 'As'), ('7c', 'Ah'), ('7c', 'Ad'), ('7h', 'Kh'), ('7h', 'As'), ('7h', 'Ac'), ('7h', 'Ad'), ('7d', 'Kd'), ('7d', 'As'), ('7d', 'Ac'), ('7d', 'Ah'), ('9s', 'Kc'), ('9s', 'Kh'), ('9s', 'Kd'), ('9c', 'Ks'), ('9c', 'Kh'), ('9c', 'Kd'), ('9h', 'Ks'), ('9h', 'Kc'), ('9h', 'Kd'), ('9d', 'Ks'), ('9d', 'Kc'), ('9d', 'Kh')],
[],
[('9s', 'Js'), ('9c', 'Jc'), ('9h', 'Jh'), ('9d', 'Jd')],
[],
[('3s', 'As'), ('3c', 'Ac'), ('3h', 'Ah'), ('3d', 'Ad')],
[],
[],
[],
[('5s', '5c'), ('5s', '5h'), ('5s', '5d'), ('5c', '5h'), ('5c', '5d'), ('5h', '5d')],
[('Ts', 'Qc'), ('Ts', 'Qh'), ('Ts', 'Qd'), ('Tc', 'Qs'), ('Tc', 'Qh'), ('Tc', 'Qd'), ('Th', 'Qs'), ('Th', 'Qc'), ('Th', 'Qd'), ('Td', 'Qs'), ('Td', 'Qc'), ('Td', 'Qh')],
[('8s', 'Ks'), ('8c', 'Kc'), ('8h', 'Kh'), ('8d', 'Kd')],
[],
[('8s', 'Ac'), ('8s', 'Ah'), ('8s', 'Ad'), ('8c', 'As'), ('8c', 'Ah'), ('8c', 'Ad'), ('8h', 'As'), ('8h', 'Ac'), ('8h', 'Ad'), ('8d', 'As'), ('8d', 'Ac'), ('8d', 'Ah')],
[('4s', 'As'), ('4c', 'Ac'), ('4h', 'Ah'), ('4d', 'Ad')],
[('9s', 'Qs'), ('9c', 'Qc'), ('9h', 'Qh'), ('9d', 'Qd')],
[],
[],
[],
[],
[('6s', 'As'), ('6c', 'Ac'), ('6h', 'Ah'), ('6d', 'Ad')],
[],
[('Js', 'Qc'), ('Js', 'Qh'), ('Js', 'Qd'), ('Jc', 'Qs'), ('Jc', 'Qh'), ('Jc', 'Qd'), ('Jh', 'Qs'), ('Jh', 'Qc'), ('Jh', 'Qd'), ('Jd', 'Qs'), ('Jd', 'Qc'), ('Jd', 'Qh')],
[],
[('5s', 'As'), ('5c', 'Ac'), ('5h', 'Ah'), ('5d', 'Ad'), ('9s', 'Ac'), ('9s', 'Ah'), ('9s', 'Ad'), ('9c', 'As'), ('9c', 'Ah'), ('9c', 'Ad'), ('9h', 'As'), ('9h', 'Ac'), ('9h', 'Ad'), ('9d', 'As'), ('9d', 'Ac'), ('9d', 'Ah')],
[],
[],
[],
[('Ts', 'Js'), ('Ts', 'Kc'), ('Ts', 'Kh'), ('Ts', 'Kd'), ('Tc', 'Jc'), ('Tc', 'Ks'), ('Tc', 'Kh'), ('Tc', 'Kd'), ('Th', 'Jh'), ('Th', 'Ks'), ('Th', 'Kc'), ('Th', 'Kd'), ('Td', 'Jd'), ('Td', 'Ks'), ('Td', 'Kc'), ('Td', 'Kh')],
[],
[],
[],
[('7s', 'As'), ('7c', 'Ac'), ('7h', 'Ah'), ('7d', 'Ad'), ('9s', 'Ks'), ('9c', 'Kc'), ('9h', 'Kh'), ('9d', 'Kd')],
[],
[],
[],
[],
[],
[],
[('Js', 'Kc'), ('Js', 'Kh'), ('Js', 'Kd'), ('Jc', 'Ks'), ('Jc', 'Kh'), ('Jc', 'Kd'), ('Jh', 'Ks'), ('Jh', 'Kc'), ('Jh', 'Kd'), ('Jd', 'Ks'), ('Jd', 'Kc'), ('Jd', 'Kh')],
[('6s', '6c'), ('6s', '6h'), ('6s', '6d'), ('6c', '6h'), ('6c', '6d'), ('6h', '6d'), ('Ts', 'Qs'), ('Tc', 'Qc'), ('Th', 'Qh'), ('Td', 'Qd')],
[],
[],
[],
[('8s', 'As'), ('8c', 'Ac'), ('8h', 'Ah'), ('8d', 'Ad')],
[],
[],
[],
[],
[],
[],
[('Ts', 'Ac'), ('Ts', 'Ah'), ('Ts', 'Ad'), ('Tc', 'As'), ('Tc', 'Ah'), ('Tc', 'Ad'), ('Th', 'As'), ('Th', 'Ac'), ('Th', 'Ad'), ('Td', 'As'), ('Td', 'Ac'), ('Td', 'Ah'), ('Js', 'Qs'), ('Jc', 'Qc'), ('Jh', 'Qh'), ('Jd', 'Qd')],
[('Qs', 'Kc'), ('Qs', 'Kh'), ('Qs', 'Kd'), ('Qc', 'Ks'), ('Qc', 'Kh'), ('Qc', 'Kd'), ('Qh', 'Ks'), ('Qh', 'Kc'), ('Qh', 'Kd'), ('Qd', 'Ks'), ('Qd', 'Kc'), ('Qd', 'Kh')],
[],
[('9s', 'As'), ('9c', 'Ac'), ('9h', 'Ah'), ('9d', 'Ad')],
[],
[],
[('Ts', 'Ks'), ('Tc', 'Kc'), ('Th', 'Kh'), ('Td', 'Kd')],
[],
[],
[],
[],
[],
[],
[('Js', 'Ac'), ('Js', 'Ah'), ('Js', 'Ad'), ('Jc', 'As'), ('Jc', 'Ah'), ('Jc', 'Ad'), ('Jh', 'As'), ('Jh', 'Ac'), ('Jh', 'Ad'), ('Jd', 'As'), ('Jd', 'Ac'), ('Jd', 'Ah')],
[],
[],
[('Js', 'Ks'), ('Jc', 'Kc'), ('Jh', 'Kh'), ('Jd', 'Kd')],
[],
[],
[],
[],
[],
[('7s', '7c'), ('7s', '7h'), ('7s', '7d'), ('7c', '7h'), ('7c', '7d'), ('7h', '7d')],
[],
[],
[],
[('Qs', 'Ac'), ('Qs', 'Ah'), ('Qs', 'Ad'), ('Qc', 'As'), ('Qc', 'Ah'), ('Qc', 'Ad'), ('Qh', 'As'), ('Qh', 'Ac'), ('Qh', 'Ad'), ('Qd', 'As'), ('Qd', 'Ac'), ('Qd', 'Ah')],
[],
[('Qs', 'Ks'), ('Qc', 'Kc'), ('Qh', 'Kh'), ('Qd', 'Kd')],
[('Ts', 'As'), ('Tc', 'Ac'), ('Th', 'Ah'), ('Td', 'Ad')],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[('Js', 'As'), ('Jc', 'Ac'), ('Jh', 'Ah'), ('Jd', 'Ad'), ('Ks', 'Ac'), ('Ks', 'Ah'), ('Ks', 'Ad'), ('Kc', 'As'), ('Kc', 'Ah'), ('Kc', 'Ad'), ('Kh', 'As'), ('Kh', 'Ac'), ('Kh', 'Ad'), ('Kd', 'As'), ('Kd', 'Ac'), ('Kd', 'Ah')],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[('Qs', 'As'), ('Qc', 'Ac'), ('Qh', 'Ah'), ('Qd', 'Ad')],
[],
[],
[],
[],
[('8s', '8c'), ('8s', '8h'), ('8s', '8d'), ('8c', '8h'), ('8c', '8d'), ('8h', '8d')],
[],
[],
[],
[],
[],
[],
[('Ks', 'As'), ('Kc', 'Ac'), ('Kh', 'Ah'), ('Kd', 'Ad')],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[('9s', '9c'), ('9s', '9h'), ('9s', '9d'), ('9c', '9h'), ('9c', '9d'), ('9h', '9d')],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[('Ts', 'Tc'), ('Ts', 'Th'), ('Ts', 'Td'), ('Tc', 'Th'), ('Tc', 'Td'), ('Th', 'Td')],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[('Js', 'Jc'), ('Js', 'Jh'), ('Js', 'Jd'), ('Jc', 'Jh'), ('Jc', 'Jd'), ('Jh', 'Jd')],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[('Qs', 'Qc'), ('Qs', 'Qh'), ('Qs', 'Qd'), ('Qc', 'Qh'), ('Qc', 'Qd'), ('Qh', 'Qd')],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[('Ks', 'Kc'), ('Ks', 'Kh'), ('Ks', 'Kd'), ('Kc', 'Kh'), ('Kc', 'Kd'), ('Kh', 'Kd')],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[('As', 'Ac'), ('As', 'Ah'), ('As', 'Ad'), ('Ac', 'Ah'), ('Ac', 'Ad'), ('Ah', 'Ad')],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[]]
