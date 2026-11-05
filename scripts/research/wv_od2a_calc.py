import json
# CDC Injury Center state funding pages, FY2025 (Oct 1 2024 - Sep 30 2025), state award + local awards
S = {'Alabama':(3619072,[1557500]),'Alaska':(2692878,[]),'Arizona':(4703386,[2892500,2544375]),'Arkansas':(2155910,[]),
'California':(5094718,[2549000,3217500,2892500,2225000,2225000]),'Colorado':(4307759,[1807494]),'Connecticut':(4452788,[1779479,1090000]),
'Delaware':(3327587,[]),'Florida':(5823539,[3742500,3075000,2550000]),'Georgia':(4245286,[]),'Hawaii':(2748281,[]),'Idaho':(2041935,[]),
'Illinois':(4586082,[3417500]),'Indiana':(5129814,[2750000]),'Iowa':(2507303,[]),'Kansas':(2685279,[1140000]),'Kentucky':(5407419,[]),
'Louisiana':(4688805,[]),'Maine':(2920497,[823799]),'Maryland':(4528982,[2550000]),'Massachusetts':(4210480,[1355037]),
'Michigan':(4261805,[838273]),'Minnesota':(4199924,[]),'Mississippi':(2540192,[]),'Missouri':(4394497,[2682189]),'Montana':(2169512,[]),
'Nebraska':(2481553,[890000]),'Nevada':(2509678,[2550000]),'New Hampshire':(2697194,[]),'New Jersey':(4653462,[]),'New Mexico':(4322929,[]),
'New York':(5017294,[3401911,890000]),'North Carolina':(4950273,[837708]),'North Dakota':(0,[]),'Ohio':(5256430,[3742500,3075000,2851407]),
'Oklahoma':(2453381,[]),'Oregon':(3854849,[]),'Pennsylvania':(5310740,[3742500,2997558,889941]),'Rhode Island':(3453142,[]),
'South Carolina':(4587985,[]),'South Dakota':(1865943,[]),'Tennessee':(5343696,[1320505]),'Texas':(3847634,[2225000,2231063]),
'Utah':(2710977,[890000]),'Vermont':(3272032,[]),'Virginia':(4066658,[]),'Washington':(4193955,[3075000,889476]),
'District of Columbia':(3945761,[]),'West Virginia':(5339590,[]),'Wisconsin':(4483777,[]),'Wyoming':(1952533,[])}
rows = {r['state']: r for r in json.load(open('rows.json'))}
out = []
for s,(st,loc) in S.items():
    p = rows[s]['pop2024']; tot = st+sum(loc)
    out.append((tot/p, s, st, tot, p, tot/rows[s]['d2024']))
out.sort(reverse=True)
for i,(pc,s,st,tot,p,pd) in enumerate(out,1):
    if i<=10 or s=='West Virginia': print(i,s,st,tot,p,round(pc,2),round(pd))
st_rank = sorted(out,key=lambda x:-x[2]); print('WV state-award rank by $', [i for i,x in enumerate(st_rank,1) if x[1]=='West Virginia'])
import statistics; print('median pc', round(statistics.median(x[0] for x in out),2), 'n', len(out))
print('sum all', sum(x[3] for x in out), 'pop', sum(x[4] for x in out))
