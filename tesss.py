

W1=200
W2=200
W3=200
W4=200
TS=10
TB=1

k=100
B1=W1*TS
B2=W2*TB
B3=W3*TS
B4=W4*TB

Wz=(-W1+W2-W3+W4)

if Wz>0:
    Bz=TS*Wz
else:
    Bz=TB*Wz


x=(B2+B4+Bz)/(B1+B2+1/k*B3+1/k*B4)
y=x/k

print(Bz)
print(x)
print(y)

B1=x*B1
B2=(1-x)*B2
B3=y*B3
B4=(1-y)*B4

print(str(B1)+" "+str(B2)+" "+str(B3)+" "+str(B4))
