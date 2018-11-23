import femm
import numpy as np
import matplotlib.pyplot as plt
EndTime = 2
dt = 0.01
circuitstep = 1000
class Projectile():
    a = 0
    v = 0
    s = 2.5
    m = 0.001
    def Intergrate(self,dt):
        self.s += self.v*dt
        self.v += self.a*dt
        self.a = 0
class Circuit():
    I = 0
    Capacitance = 100e-3
    CapVolts = 1000#Columb
    Resistance = 100
    VInductor = 0
    Inductance = 1
    Discharge = True
    def Intergrate(self,dt):
        VRes = self.I * self.Resistance
        if self.Discharge:
            self.VInductor = self.CapVolts - VRes
        else:
            self.VInductor =-VRes
        dI = (-self.VInductor/self.Inductance) * dt
        dQ = self.I * dt
        self.I -= dI
        self.CapVolts -= dQ / self.Capacitance
armeture = Projectile()
circ = Circuit()
# VCirc = []
# tdata = np.arange(0,10,dt)
# for t in tdata:
#     circ.Intergrate(dt)
#     VCirc.append(circ.I)
# plt.plot(tdata,VCirc)
# plt.show()
# quit()
femm.openfemm()
femm.opendocument("default.fem")
femm.mi_saveas("temp.fem")
femm.mi_seteditmode("group")
z=[]
f=[]
VData=[]
IData = []
steps = (5 - 2.5) / 16
timedata = np.arange(0,EndTime,dt)
for n in timedata:
    print(n,armeture.s,circ.I)
    if armeture.s >= 7:
        print("Out of bounds")
        break
    femm.mi_analyze()
    femm.mi_loadsolution()
    femm.mo_groupselectblock(1)
    fz=femm.mo_blockintegral(19)
    z.append(n*steps)
    f.append(fz)
    VData.append(armeture.v)
    armeture.a = fz/armeture.m
    armeture.Intergrate(dt)
    for i in range(circuitstep):
        circ.Intergrate(dt/circuitstep)
        IData.append(circ.I)
    femm.mi_selectgroup(1)
    femm.mi_movetranslate(0, armeture.v*dt)
    femm.mi_modifycircprop("coil",1,circ.I)
    if(armeture.s >= 5):
        circ.Discharge = False
        #femm.mi_modifycircprop("coil",1,0)
femm.closefemm()
timedata = timedata[:len(VData)]
plt.plot(z,f)
plt.ylabel('Force, N')
plt.xlabel('Offset, in')
plt.figure()
plt.plot(timedata,VData)
plt.title("Time and Velocity")
plt.figure()
plt.plot(IData)
plt.title("Time and Current")
plt.show()
