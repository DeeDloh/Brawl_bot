def trophies_statpoints_calc(t, brawlers):
    sp = 0
    for b in brawlers:
        bt = b['trophies']
        if bt < 500:
            continue
        elif 501 <= bt <= 524:
            sp += 20
            t -= bt - 500
        elif 525 <= bt <= 549:
            sp += 50
            t -= bt - 524
        elif 550 <= bt <= 574:
            sp += 70
            t -= bt - 549
        elif 575 <= bt <= 599:
            sp += 80
            t -= bt - 574
        elif 600 <= bt <= 624:
            sp += 90
            t -= bt - 599
        elif 625 <= bt <= 649:
            sp += 100
            t -= bt - 624
        elif 650 <= bt <= 674:
            sp += 110
            t -= bt - 649
        elif 675 <= bt <= 699:
            sp += 120
            t -= bt - 674
        elif 700 <= bt <= 724:
            sp += 130
            t -= bt - 699
        elif 725 <= bt <= 749:
            sp += 140
            t -= bt - 724
        elif 750 <= bt <= 774:
            sp += 150
            t -= bt - 749
        elif 775 <= bt <= 799:
            sp += 160
            t -= bt - 774
        elif 800 <= bt <= 824:
            sp += 170
            t -= bt - 799
        elif 825 <= bt <= 849:
            sp += 180
            t -= bt - 824
        elif 850 <= bt <= 874:
            sp += 190
            t -= bt - 849
        elif 875 <= bt <= 899:
            sp += 200
            t -= bt - 874
        elif 900 <= bt <= 924:
            sp += 210
            t -= bt - 885
        elif 925 <= bt <= 949:
            sp += 220
            t -= bt - 900
        elif 950 <= bt <= 974:
            sp += 230
            t -= bt - 920
        elif 975 <= bt <= 999:
            sp += 240
            t -= bt - 940
        elif 1000 <= bt <= 1049:
            sp += 250
            t -= bt - 960
        elif 1050 <= bt <= 1099:
            sp += 260
            t -= bt - 980
        elif 1100 <= bt <= 1149:
            sp += 270
            t -= bt - 1000
        elif 1150 <= bt <= 1199:
            sp += 280
            t -= bt - 1020
        elif 1200 <= bt <= 1249:
            sp += 290
            t -= bt - 1040
        elif 1250 <= bt <= 1299:
            sp += 300
            t -= bt - 1060
        elif 1300 <= bt <= 1349:
            sp += 310
            t -= bt - 1080
        elif 1350 <= bt <= 1399:
            sp += 320
            t -= bt - 1100
        elif 1400 <= bt <= 1449:
            sp += 330
            t -= bt - 1120
        elif 1450 <= bt <= 1499:
            sp += 340
            t -= bt - 1140
        elif bt >= 1500:
            sp += 350
            t -= bt - 1150
    return t, sp