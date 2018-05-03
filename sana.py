#!/usr/bin/env python3

def nearest_x(df, value):
    """valueに最も近い値下がったところのindexを返す"""
    down = df.max() - value
    absolute_sub = pd.DataFrame(abs(df - down)).sort_values(by=df.columns[0])
    return absolute_sub
