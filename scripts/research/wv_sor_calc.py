import re, csv, sys, json
# SOR allocations from SAMHSA NOFOs
def parse(txt, start, end):
    seg = txt[txt.index(start):]
    seg = seg[:seg.index(end)] if end in seg else seg
    out = {}
    for m in re.finditer(r"^([A-Za-z .]+?)\s+\$([\d,]+)\s*$", seg, re.M):
        out[m.group(1).strip().title()] = int(m.group(2).replace(',', ''))
    return out
t22 = open('nofo22.txt').read(); t24 = open('nofo24.txt').read()
k = t22[t22.rindex('Appendix K – FY 2022 Annual Formula Based Allocation of'):]
sor22 = parse(k, 'STATE FY 2022', 'Appendix L')
l = k[k.index('Appendix L'):]
sor23 = parse(l, 'STATES  FY23', 'The program office')
a = t24[t24.rindex('Appendix A – FY 2024 Allocations'):]
sor24 = parse(a, 'State FY 2024', 'zzzz')
pop = {}
for r in csv.DictReader(open('census/nst2024.csv', encoding='latin-1')):
    if r['SUMLEV'] == '040':
        pop[r['NAME']] = {y: int(r[f'POPESTIMATE{y}']) for y in (2022, 2023, 2024)}
deaths = {}
for r in csv.DictReader(open('/Users/ericpachman/PycharmProjects/FentanylDeaths/data/clean/state.csv')):
    if r['year'] in ('2022', '2023', '2024'):
        deaths.setdefault(r['name'], {})[int(r['year'])] = int(r['deaths'])
fix = {'District Of Columbia': 'District of Columbia'}
rows = []
for name in pop:
    if name == 'Puerto Rico': continue
    kk = name.title() if name.title() in sor22 else [x for x in sor22 if fix.get(x, x) == name][0]
    s = {2022: sor22[kk], 2023: sor23[kk], 2024: sor24[kk]}
    d = deaths[name]
    rows.append(dict(state=name, **{f'sor{y}': s[y] for y in s}, **{f'pop{y}': pop[name][y] for y in s},
        **{f'd{y}': d[y] for y in d},
        pc22=s[2022]/pop[name][2022], pc23=s[2023]/pop[name][2023], pc24=s[2024]/pop[name][2024],
        pd22=s[2022]/d[2022], pd23=s[2023]/d[2023],
        chg=(d[2024]-d[2023])/d[2023]*100))
print('n states', len(rows), 'sums', sum(sor22.values()), sum(sor23.values()), sum(sor24.values()))
for key in ('pc23', 'pd23', 'pc22', 'pc24', 'chg'):
    rows.sort(key=lambda r: -r[key] if key != 'chg' else r[key])
    print('\n==', key)
    for i, r in enumerate(rows, 1):
        if i <= 8 or r['state'] == 'West Virginia':
            print(i, r['state'], round(r[key], 2), r['sor2023'], r['pop2023'], r['d2023'])
json.dump(rows, open('rows.json', 'w'))
# medians
import statistics as st
for key in ('pc22','pc23','pc24','pd22','pd23'):
    print(key, 'median', round(st.median(r[key] for r in rows), 2))
# US totals (50+DC)
S23 = sum(r['sor2023'] for r in rows); P23 = sum(r['pop2023'] for r in rows); D23 = sum(r['d2023'] for r in rows)
print('US 50+DC SOR23', S23, 'pop', P23, 'pc', S23/P23, 'deaths', D23, 'per death', S23/D23)
# spearman
def rank(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r = [0]*len(v)
    for j, i in enumerate(o): r[i] = j+1
    return r
x = [r['pc23'] for r in rows]; y = [r['chg'] for r in rows]
rx, ry = rank(x), rank(y); n = len(x)
print('spearman pc23 vs chg', 1 - 6*sum((a-b)**2 for a, b in zip(rx, ry))/(n*(n*n-1)))
x = [r['pd23'] for r in rows]; rx = rank(x)
print('spearman pd23 vs chg', 1 - 6*sum((a-b)**2 for a, b in zip(rx, ry))/(n*(n*n-1)))
