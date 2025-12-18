li = []
st = "help **me** please"
ts = st.split("**")
for item in range(0, len(ts)):
    ti = [ts[item]]
    li.append(ti)
print(li)
