print sorted([36, 12, 5, 9, 21], lambda x, y: y - x)
print sorted([5, 36, 12, 9, 21], lambda y, x: y - x)
print sorted(['ADD', 'dsa', '23', 'dfeeeee'], lambda x, y:cmp(y, x))
print sorted(['ADD', 'dsa', '23', 'dfeeeee'], lambda x, y:-cmp(y, x))
