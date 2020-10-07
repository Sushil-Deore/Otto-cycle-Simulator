# otto cycle simulator

import matplotlib.pyplot as plt
import math


def engine_kinemetics( bore, stroke, con_rod, cr, starting_crank, ending_crank):

    # geometric parameters

    a=stroke/2
    R=con_rod/a
    num_values = 20

    s_crank=math.radians(starting_crank)
    e_crank=math.radians(ending_crank)

    v_s = (math.pi/4) * pow(bore,2) * stroke
    v_c = v_s/(cr-1)

    V=[]

    dtheta= (e_crank-s_crank)/(num_values-1)

    for i in range(0,num_values):
        theta= s_crank+ i*dtheta

        # volume paramters

        term1=0.5*(cr-1)
        term2=R + 1-math.cos(theta)
        term3= pow(pow(R,2)-pow(math.sin(theta),2),0.5)
        V.append((1 + term1*(term2 -term3))*v_c)

    return V

# inputes for cycle

p1=101325
t1=500
t3=2300
gamma= 1.4

# size/volume parameters

bore = 0.1
stroke= 0.1
con_rod= 0.15
cr= 12

# volume computation

v_s = (math.pi/4) * pow(bore,2) * stroke

v_c = v_s/(cr-1)

v1= v_s + v_c

# state point 2

v2= v_c

# p2v2^gamma = p1v1^gamma

p2= p1* pow(v1,gamma)/pow(v2,gamma)

# p1v1/t1 = p2v2/t2 | rhs = p1v1/t1 | rhs = p2v2/t2 | t2 = p2v2/rhs

rhs = p1*v1/t1

t2 = p2*v2/rhs

V_Compression= engine_kinemetics(bore, stroke, con_rod, cr, 180,0)


Constant= p1*pow(v1,gamma)

P_Compression=[]

for v in V_Compression:
    P_Compression.append(Constant/pow(v,gamma))


# state point 3

v3=v2

# p3v3/t3 = p2v2/t2 | rhs = p2v2/t2 | p3 = rhs*t3/v3

rhs = p2*v2/t2

p3 = rhs*t3/v3 

V_Expansion= engine_kinemetics(bore, stroke, con_rod, cr, 0,180)

Constant= p3*pow(v3,gamma)

P_Expansion=[]

for v in V_Expansion:
    P_Expansion.append(Constant/pow(v,gamma))

#state point 4

v4=v1

# p4v4^gamma = p3v3^gamma

p4 = p3* pow(v3,gamma)/pow(v4,gamma)

# p4v4/t4 = p3v3/t3 | rhs = p3v3/t3 | t4=p4v4/rhs

rhs = p3*v3/t3

t4 = p4*v4/rhs

thermal_efficiency=1-1/pow(cr,gamma-1)

thermal_efficiency=thermal_efficiency*100

print(f'Thermal Efficiency = {round(thermal_efficiency,2)} %')

plt.plot([v2,v3],[p2,p3])
plt.plot(V_Compression,P_Compression)
plt.plot(V_Expansion,P_Expansion)
plt.plot([v4,v1],[p4,p1])
plt.xlabel('Volume')
plt.ylabel('Pressure')
plt.show()