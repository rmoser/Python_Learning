# Advent of Code
year = 2023
day = 25

import numpy as np
import aocd
import os
import pprint
import itertools as it
import functools as ft
import igraph as ig
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
plt.ioff()

text0 = """
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""

# text1 = aocd.get_data(day=day, year=year)
text1 = """
vgz: pjv
rfx: gqn
jnd: ldj tvn nxh kpn
rpx: jpm
spg: rfc mkf qsg pnh
zkm: fjq qdl lsb
sps: mzr
pvv: gmj drl
dck: kxc vph mhv rjr
lxt: fqx mbg hrj
vxj: ngg qcg khn
vhr: hgq rzg klr hcz
xfx: znq hjx mbz
tfj: rgz djk vlt
hvj: hnb mrm
pjg: cbm
bhc: mrg bzt xfk qlf
dmn: glj vqk czk mkx
frg: pmm tmv zkx
cvc: lnp
xrj: hnj fgv kjq tjh
lck: gqf zbn pcb jrp lpx
pth: xgt lbz
mcr: cpn ssz bjj krl
bzt: tnp
lxm: bqq
dpx: dds crd cdt qpr vns
fhv: zsp kxq lxx vzs
dgr: cqn kkh pqs vcv
qlr: ndx cjn
csb: jrh gdf sbr
qfd: bhc scm kmg vxx
dnv: fvs mbg jmj
hzv: nqm cfg dkq mll bzb znl
vtr: lhm rkl
pfb: hdg
pgq: jcg cxt lrk tkg
prv: kkc knb tvl
fkp: bdt
fqf: nkp vvv nps
fnj: bqx nqv lsc
nfn: hkb dvg
cxz: rpr cfb jmv lbz
vts: bkc
dqn: rvq kvz ztc
gdd: jpj fnd sxr gkt
zmp: fpg
xvz: bhj vxn rlx bnc
bqf: hqc gfr
rrj: rzh
gnk: jmc
vlp: jmj znt
hsp: vgz lhh xdp ptp vxn
krl: zkj
jmg: smh
xnk: frt srj rvb dvn
njs: qlr
pms: rkl dxk
hpr: cvn fsz dvx tvx jrj
dvb: bqv
gsf: fgk zlh xdm
qjx: zkt hcz kbj gvn
kmg: vpq tnn
zvt: mnf bbk tdp mjq xpm bnq
xnh: fgv mjq
qpz: mft pdz
qff: pvz
mjf: nst pjj
pfv: bqf smq dkd qbt rtq
tjr: bdg phm hxl
mpt: zkk
jps: mnm vkc qcd srh
stk: rrj
cpr: mtz qrb jlc rvj
ljl: kjq
kfc: szh
hmz: srq vph lmh pbb
sfp: lbd
shc: fvg jgj vpz
ggr: mhv nss vhd czb
zgx: fdr zqk jdl kxm
ljt: hxs nhc dxv
lsh: kkg
sjz: clx
lhh: xpr ptb tjl
qbj: ghp zlh nmp
jxp: gzv rbm hnj frq
jlk: mcg pzg nlj dzl
mzb: lqk
bsh: gtp cbz tzz fkp
pnm: gxt
qxl: bfb djk
dfx: lsc
hzl: qvl jsl sqr
vvv: rpq xbj
jmq: ztv zqh zgc
kck: vmz zpg
kbf: zjd lth xpk hgr mzb
jtf: pdr cbg
vpz: vfn
zns: jdj drx dlx
mxd: bmb njz zsr jfp
svk: jrb mgk tzg lfc
mzm: lfc cnz xfv ppm
hxx: zsx ckj pmm
sbp: qxl xlx ffj
qmg: jcc tdx mmv pdj
pjh: jsj qzs
mmv: zgh rsh
jcr: lsc tbj
rct: ltj tdr dzj
vfz: hpp
rqt: dlx dvn
ctk: dvg cbh ksp txp
bbh: lpm qrp nrq txx
rgr: zkj pjj
glp: qvl
jlc: pls dkq scm
tkn: xlx gtr
prl: kdh
jjt: vnd frg sfs vzx qxs
lbz: szm
mqd: ljz mgk
pnx: gzc krz gvl
mkq: xqc hxs
hkm: cqn xfk
dvg: vfp jvj
xrt: tnc
kfm: phm rjf dqh kvb
dcn: tdl
dtr: nhn ztv mbg
jrh: hhr
brv: qsb pzf dmq rxl
ckz: zpk qzc fnf
tgj: rkh llr
gkd: csj kgk fxl
ppl: lrx zjr fjf njv
nbh: frt chs
jsl: mmt
nrl: scm crt
cnh: ffx bqq cfg
lzv: qvt
rqk: flt rxg qmk flb
xnm: zvz sql
nmq: nbq tzm
nlp: gsd fgl hdc mpt
zjr: sbs pjv
bpq: pgz xsh bzk jrz
dbl: hrr qvt
kkn: xbj
npd: xmg hbt
brl: ztc
svb: ltz
qcz: lbm hmm sbs
nch: jvp mfs
gbd: vts fgs gtd czt xlx
mlc: gbh jxk kkl
lsn: jzj lbz rxp gbh
bng: flb qxs ktn fjf
lfj: kpc
jdf: ppv lgm
cdg: dkq
jqt: rkh
lmg: ccx sfk
kdq: mrm
gtp: gkp xvn knm vmt
pvx: gdn src rlb bhm rjm nmq
thv: zlh pgh
vqd: kbj rvk lfj
pnb: pdz nrq
xsg: jjr drz
gkt: ngq
prx: fgt brx
lhc: pvv fvg prs bdk
qqb: glg fxt
fnd: jrg dkq czt
sbj: ksp
lgk: cjn dxp mnh
klp: dtl hsz
hrk: ndq shh hbg
dqz: fcx zkx lmh zsx
fcc: fmh fpg rjf
jfs: mqd dgz
hxl: znt xlg rkh vqk thg
lnp: rxg mzb
rbm: lzh
bdg: vfn cnp zkk
dzn: mbg jvj xzj
mjc: pbl dxk ccs
ntt: dkr bxs bgf kdb
dqr: vmz srd dvb
zhx: kmc zrs
dxm: ltr lzc jkt cjj
mgl: nzn ltc
gqm: lgt
phj: jpm dtn
ndf: prz xnh dng jvk
jjb: nmh xsn
ndh: hdc xbj fgl pjg gnk clx mmj
kts: nhc smf
stc: hgm mtj rkv
vcv: jfp bqv
fts: vjp zgh mxt drz
jpm: fxt
svh: gtr rvj bbm
tdn: rzp rvk srj
jcg: rvj dsr
szn: cgn gfj dtr
vsd: gjs bdk
sqt: gxs fcn ppd xsg ggg
tdf: ccs
rlx: fnj
dqj: hqq pnm mrm hvq
frq: hdk zsp ghp
xgg: jkf djk jcr
nfz: jxk sch vph fpq mzr
fbf: mmt bqx
vmz: vlv
jgh: lzn
lhn: xcl csn bvh mqb vnx
bfb: xgj qbt trb hgl
fcx: pqr jdh
vnd: jtb dxk
cgt: hbg cnh tbj
zpg: zhc
shm: bln sbq pgk hxs
rtv: dkq jzq
hnt: brc snt hbc nzp
ppm: ppg cmx
dgp: jkf tdp
llr: nvg
zxp: pqr mtj cqn vnd nrl
zkk: rcq
brx: shq
bqv: flb
dms: fqx qsb thk
pbh: dbs zrs
vfc: tfx jgh qmb
qbz: crp
skv: dmb fvh tdl zmp
hmn: bdk ncd xzj
vdc: rth rnn bln
zsr: ltj hqg
kkh: tmg pbb fkp
njk: tmv qht hgq
vzm: vtr pdr rgl fnf ckm
sjp: nbh gtd srd ttz
vkm: npl qmm
klr: rvj gqm bdt
qdx: djk pgr mqf scm
czn: qkn cbm
hcf: vpv qkn nst xnm
rpj: prj
hcz: szb
nkf: bjz vvc nqv gpv
bmm: kft lvr dqp
ngk: pvz phm cpc
spk: lcp nfc
rtq: tdr hqk
cdp: xcl lbr
kgs: tjl kcx phj nzn
snh: gxt bdd dzl hsz
xmh: pnf xcl qhs vkc gzc
qqz: fsc
mbf: kpc dxr
kjd: xrt msv kbj
klc: lxt fsz lvn pqp
mvt: lzh
fxs: shz bhm vnx pvz vfz
tjv: plh hfd qsg tfj
jvb: bhz szx gqm kxd
fcl: nvg jmc
nzn: zpk
pnf: ppv
pmx: dzj vff kmg nbh
bhj: trb
rzt: qmm pmp qht
xkx: hsk mrm rzz
pvh: vpq njk fqr sjt
cnl: ngg mnh kns fkg fvm phc
hjr: dnd czg pjl
rkv: pbp
khn: lbr
rfd: mvt kkq ndd xrt
znj: nxh
cms: ktn mjm pzv
hlc: rzg lrx hjx xgj nvb kgj
zzk: jvk svb
zzp: grg zsr vkm
bcm: gxs txp sbr xnd
kds: nbx lpp mrg
fhz: hsz sdt nhn kxq
xfs: dbs
xts: rgc fbf
mxt: sjz crp fvg
qkk: pzv zhg fnf qcj
drt: gqm ljl
ddk: fsb zht xzk
xgj: kqm
rfm: ftz lvn qgj
hqk: gxq lqk
tzz: dgp spt bhj
zmq: kqm
bmb: mvn spt
pgz: zqh cmx
hks: njl qzp
ngp: nmh tpn
nbl: hzh nsv
pcv: xvn rxg cdg hdt
fzm: trb tqv zdj
jpl: rvz xcz bfn
xmc: thg zkj tqb sxv ppd lcp
nxf: ghp vrz dgv ljv
kzn: ppd tkf
bsm: fqb rtp vpn qzc
rgc: jpm
ljh: cbh zzd gdj szn jlm
fgl: rdl
ptv: khr fdr kxp smf
hht: grg
czb: zfj vpn cqt
ljv: ptt
dxp: rcq
fgc: pxb kgv ndk mmv spk qcd
mnz: bxs vpd pnh
kxq: crz
zld: jjb znt xpq
fpz: ndx gmx fgz zrs
hfx: dqp
jkf: ztc
hmm: fgs
hkc: ntv
ckr: jps vgd ntv bln
rvt: tkn xfx ngj npd qcz
qhq: sdd vcq mcg fkg
nst: fgz tqr jsj
mjv: drl sxb
jkm: ghc mgm kjq zpg
qfk: qmk jsn czg nsv jts knb
tpn: pnb
qct: lxx
gtr: tbj
jgn: sst
zzc: fft rjm cgm
kgj: glv trb npl
lns: lzv rzc fsz
njz: bxs zck
klf: scl zkh rpq
tvn: ccs bhz dtp
sgt: lth nzk xnh zjr fxt
frd: rfc qsg qlv vjl
ltz: hdx vnl
crg: nrv pjv
rfk: npl knb
kzj: mvn qsf
mph: lpr klp rkh sqj ncx
pcb: lxm
ktj: cng
cgm: nvg
pqp: qlr
znm: lxm fns kkc nzn rlx gtr
njp: ltj
qgg: zff ngq ldz
fcn: sfp xcl
qvq: jlr jdl tkf dds
rxp: znq cmj bxs cxt
mxk: dzj rgz thv sps
rgl: czp ffx
fkc: hqk rtv szb gkt
rtp: prc krp mqn rzp
pgk: nrm
kjk: cpm
mcv: prl jfp nxh hnd
nkm: bvg pnf
hvq: shq
lhv: bhl khn ppm tvx
sql: smf nzp
cnv: bzt bnq
fnr: jmj fqx hbc qkn
xpr: glz
hdd: fxj tbn qtp
vvz: jsj zpl
rqh: lbb mkx zvz jzl bvg cdp
bhr: xsd czt
tqt: hzh bqq
pxb: thk
znq: vnl gjg
gst: nbl zns ccx hkm
thg: fkg
fqb: gpg czp jxk
lpx: zck czg
mzd: ljl phj tkq npd tvn
tkg: qtg ntl
rpr: nsv
zfk: tlr qcg ndx dqb jqt vlp
fsg: jxj ftz jlr rdl
zzd: rzc fvg
dtn: njp nss dkd
shz: rfx zdr tct
rcj: tkq zpb xdz pzl
gzv: mxk bml gnq kgl xjp
gqx: tbn zgc
lrx: ltj
scp: gjg bjc jpf
ncx: gzc cbm
vbn: trr zpl hkc klk nps
mmj: prs prj mgk
hfb: tmv hbx
ldz: mdk rfk
kft: mjv ppz xcs
tkf: ppg brx
cls: bqx
njc: gxs pnf mjz
fpg: drz
hft: xsd bsm rpx bml ltc
sfs: vjl bjz
cdt: jlv nkm zfx scc
qdl: dvj nrq
kpq: pxv dkr mqz lnp
jjp: tcn krp pbl bhr
mhj: xmh ccz vgp
fqr: kbn hht
hpk: llr
ffz: bjz dvb djl
nmp: kjd lhh bzm
dxb: qpr dxv hvj zfg
nzs: mbf fnd zns
zdd: dds dqp
pch: jvp qzk xfs kdp
vjm: mzr gch xdm szb
xpz: qcd fxj
ccx: bkg
rgk: rvb cbg zbq vmt
pxv: fjf szb rzt
njl: hbx mmt
rvz: dqn jdj mll vpd mgl
gdj: qfq xpz rpq
mbj: rct mxk mkf rgz
bpg: szk trb nss kpc rjr
jrb: gkd zkd bjj hvq
sls: dsl gzn khn thh
rzc: dvx sjz
vbx: bbh lns tmm nrz
rnn: hrj
bqm: snq hjr mvt spr
gjc: dms hsz pjj vkg
znl: jzq
czc: tvl mlc dfx dpm
svj: fdr nfl cqs dnv
hzn: dmb prs qmb nmq
cbm: dgz ntv
fsb: ktj
hqg: mdh
ppp: dgd xql bhj prm glp ltc
lkt: mnm sxb
tlt: hkc
kpm: mdf pnx rpj tqb
mft: bdd vqt
zdj: grg
hnd: hcr
sdd: dvx hzf zkr
rvq: kkg
zjc: qfq tdh qzd
gzn: vvv hdg lxx
tpl: vgg hkc rnn hpc
jdn: jgn zfg stk rzh pql
qhs: hrn
kcn: nzp cdp dqm
ptq: bnj qlr
fmh: hhr
szh: dtl
dhc: zbh mct nxq ghc
mdk: cfh xrr
trp: cls shf
tnc: hgl
hcd: hgm gxq skg zjd cnr
qrm: pfb sxv
thh: ljz
ldr: dxk
xql: zck
gzt: bcs zrc tzv lbm bcz
tfx: tcr zkd
nfs: fcq gfr rct hnd
tql: snt vtx jvj
lsb: dqp
trc: rtk gpg dxk jcr
tdp: skg pbl
jqx: ljt hrr hrn bnj
jlm: hpc pvz
jrg: tkn
cxt: bnt xqt qqz
qcd: gmj
ffj: mnk xlx bqx
bhl: sst zkk
rdh: gbs dgj hks hxx rjr
bkk: fcc dnm dvx lnm
mct: glp flj ttz vvr
mjz: mmv lzv vtx bvh
zjd: bkc nvb
xff: lgt kkc
pls: zdj ljv
jkt: vqk jbr klc
pjf: ksp
mbz: nbx
jvp: rth mgk vdc
fjb: znj kpc nvh
vnx: rth drz
tct: vjp
mjn: vpn znl
vff: zff
btc: zkm sqk rjb hpk
gpv: bgf qqb rvk
qcm: hqg vpq lzh
lpr: brx
mdf: zrs xgb
pvc: qsc zpg xsd
jcm: zlh rvj vnl lfj
fnh: hrk fxt sbp cpl
lrk: sdp
hvz: vkc pjf qgj
qmb: xfs zvz vfp
pbg: fxt lcn kzj nrl
zvm: pjj hvj hbc hkb
vvn: thg tzm hfx vfh
vzv: sgf mbg xcb
hln: ngp svq fmh tlt
fxz: chs tsm
snt: xqc cpm
cqn: xpk hdk
crv: ckk shc hbc
gdf: ppg xsn
lcn: gbd gbg
czh: trp ngq fbf mqf
vsb: fmj
rjb: gxt
cpz: gjt fqx ztg kfc
cgl: vfc tqr mgc pvz mdf fvs csx
fcq: nln cqt tqt
fvz: kds mdh bgf njl
dkq: qvl gpg mhv
hzh: tqv
lfx: ckm bkc lrm mnk
fjc: gfj grf sxb jrh vzs
cbn: lzc gnk jlm qzk
lgm: clx pjf nlc
ngc: tmg
rjr: mbz lmg dxr hgl cqc
tmq: vns
qmd: tjk jgn kft vsb
bzm: pdr jvb
pgc: mrm smf ztg
xxx: nch gqx zfn
jxd: hvh nzm qbj hxx
rzz: ztx dvj
flt: dvn jhz
tvl: gtr
gsl: llr crz xlg tdl pkz
lfk: ltz qlf pzv bqx hnj xjg
jdx: lmz qml
kgv: szh vtx ncx
cgn: pjf xqc
xcq: hgm zpb kdb shn
bml: xrt
rzg: vpn
vjl: ffx kkt
qcg: jps qbz
sgc: nxq rct zpd djl
ghd: xfv czn vhz lbd tjr jbr
gjs: vfp
xvd: plc fgv rvk
ghc: fgk
bcz: bjz mhv lsc
ltc: skr nvm
gzr: xts drt rtq lmh
kcv: czt hcr bbv xdg
jxj: zgc qsb txp
tqv: kdh
jgm: jvz kzn tpn lpm
srd: lpx nrv
fns: lgt qzp cdg
xjp: rzg mjm pmx
mxs: npb tkf pvv rbx rpq
jxx: hfb cvc lsj tnc
nnc: cnr kdq jfs
hrr: qvt zkd pbh
xzs: qpr xxg zvz gqs
scm: snq tnc
pzg: vns
glv: csd shf srj
xrm: nxq ndq vtr kck
cxm: bbh hxs czn cjj
xpm: dfx
krp: vff
rng: smh cqc
tkq: cnv rpr
thk: tdh brc lnm
gsk: zdg nzp xjf
mrb: hdd bhm jkz jbr src
flf: mrj lgp qgv kts
gzz: bdt vpn hmm
zrq: klk clx qbz
cjn: mgg rdl
jjr: vcq ngg
tlr: jmj brc
dqh: hrj xnd zdd
dlh: ltj zdz dng pqs
prs: fpg
bzb: xmg kxd xqt
qtg: shn ztc
fxp: vgg xsv dcn xzk
nqv: rtv
xmb: jrg hql hzh jsn
csd: jkb tnn
zgc: gmj
jrj: bln trr jgh
pqk: mjn ngq ptt hdx spt zsp
ksn: cpn vlf jgm
dsf: mqz spt vxx xmg
tpr: rqt ljx fpq sch svb
zbh: plc mqz
qgv: qhs gdn
pmm: gbs pmp
ksb: cgm spk
rzp: fxz gxq tqf
qrp: vmg ksb
hcr: fss
tzm: cqs
vzb: kvb
gbg: qzp qqz
qmp: hbp bdd pnm cgq tql tdg
cbz: qsc
jrn: bhz hdk rlx tqf
fxd: czk jjb drl
kgk: srn vpv gjs
jxk: fnf rtk
fdx: srn hzf
ppk: gvn rbm vtr dsr
str: tqr kts klf rbx
fvm: fsb xpq
xbc: jtf
ttz: mqz hgq
qvs: nbq fxl xxx
lpf: rtp vjx lpn krp dgd
nrv: xcz
jtb: mzr fcj nrv
mtr: lgz sgn vlv sqn nbz
bfn: jrp plc
fgs: jpx tjh
tkt: kft jsj
jmv: npl lzh gbs
lzn: mrj crp kph jdx
khr: cnp
bnc: szm zbz ckj
sxl: ksb gfj kxm qpr txx
nrz: mpt kkn
ztg: gsd tvx
ccz: dxp hdg
gcr: njs pql pqp dcn
zml: ntv qff hpp fjq
mbx: mbz cms jrg mjq ckz lfs
nvh: njp tdf sqn
zbz: ldr hht zrc dmm
ctn: vvz vpz ksb
mnc: nvb
qlv: qvc vts zns
xhr: vkm nbx pth zsx ldr
hnq: fcj mzb
jzl: flh ztv qzd tct
xzk: fmh pgc
jgg: dbl lbd mjf fgz
dgj: szm cvc qvl
ptb: bkg shn
rlz: mvn lpp hbx ztc
fgk: tnn
kxd: dtp xvn
zpd: csd jhz
hml: qdl hdg qrp tzm
sdt: qkn mjz kxq fkd
bmh: rgr blf npb
ghr: vgd pjh pvs
jrp: bnt tqv
nvs: gnq rxp jkb hcr
gfq: sfp ppg pxb fqx
kqx: lsh vcv xts
qlf: jmg ngc pgh jzj qcs
nhc: gpj rjb
mcg: gvl
cjb: fcj
src: rfm mgc mkq
svp: cpm dvx flf dqp
glz: lqk jsn tjl
szk: dtp
cjg: jrh xnm ppv mhj
qqx: zdg
cxl: bqh dgd ngc jsd
pgh: qmm
qht: lgt
gzj: nzp thh xcs kvb
gkk: phm zcr vfz
xsh: lbd mgg
jjv: qlz bmb njv lvk kkl
bgm: dgx qsf sbs
jzj: xpm fjf
vhd: rgc fsc cls
nzk: flj dkr hgr
mkx: hdg
xcb: rrj
zfg: prx stk gnk
bnm: bzl xdz lrx nzs szx
tsm: prz
ghp: cdg crg czp
mgc: ssz qqx
chs: pqr
vjq: lfc mgk
czg: qvl
jhp: rqk mnk gkp
pzl: snq rvq sps pjl
gch: gpz hqc mjq rkv
zbq: lpx lhm fxz
nln: hdx jpx
gmj: rrj
gbh: fqh
skt: xrm hnq pms bkg fkp
hbc: mpt
tzh: njs glj xfs pnm
txp: zcb
vxn: kvz mjn mjm prv
nqm: kcx jhz hgq
kgl: rlx rgl dgx
mdr: qgv lzv bln svq
lhm: bnq
bqp: fqr jvj xfv bdd
bbd: cvn xjf pgk pjf
frf: bml trp zmq hhs
lbk: xgb jps qzs tbt cbh
htc: bvh mnh nch fpg
knm: dsq dlx zrc
kqv: hmq khr mkq thb
xdn: vhz lbj fhj vkn
lbb: pxb jmm vsd
pjv: lzh
hqc: qqz
mxp: fgv vvr bkg
fkj: xgg glz
jdh: grg vjx
srj: dvh mll
pqs: mtj gkt bfb cqc
kvq: dmq ztx jmc zld qct
vzs: zqh sbj
lmz: xgb
tbj: prz
jgj: nlj xzj hrn nnd
npb: fdx
tjl: jzq
ptn: mcg zcb vfp dbl tbt
tdg: lxx
dsq: djl tnn
hgr: qbt
frj: cjb brl rng cgt
dbs: tcr qvt drz
qml: fgl crp
tlb: nbq fgt zcr dbs
kdb: sfk mnf
zcr: xsn
pzn: ntm zzk rng
rfc: gnq pvc
chd: zpx jgh bmh sbq fft ngk
bgs: zjr dgh frt rkj
gml: pth zdz vqd cxt
cnd: glj mcr hdg sjz
cvh: tbn zcb srn vpv dqm hmq
lbj: qnz dnf nnc
pjs: ggg fqx cgm sgf
bkj: nmh lnm jtr vgd
bhz: cqn
mrj: fmj xsn
mgm: vjg kqm hql
pbb: dtx
pgr: dgd lth gfr
gfm: bhr dlx xpr sch
skr: nbx mdk
ckk: ngg tvx
zsp: lzh
qfq: tdh hkb
srt: bcs msv bbm pmp
jsd: nrv rvk
gfr: cbg lzm nvm
ndq: vgz kbf
hjc: kbn nrl kjg mjc
xdg: cnv hbt zpb
vhz: hvj lzv
rsh: gfj
fzs: zpg xjg
ljc: nfn gdf cnz bnj
gqd: pmx zpk rfc kck
pvl: hsk hbp jcc ppz
spr: fjb bbm bzm cfg hgr
szm: rgc zsx
fkg: gxs
xzj: cqs
zbj: vjq pgc qgj
mtz: jhz tsm bqq
pgp: hpc shq
hvh: mqf ccx sjt
ncs: mfs tjk
pkc: lrk zkx rvq qxs
ltr: mft gzc
vmk: zkx xrj sxq
xqk: ldz njz djk
qsc: qmm xfk
pjl: lxm bbk
jsn: cfh lpp
dkd: tdr hkm pbp
fhj: kxm fsb
hpp: mqd xcs
vrz: tkq rfk zdj flt pzn
zkx: tdf
lpn: qhg pmm hzl
psk: qpz tzg jfs pjg cbm
jfp: czp
ljx: ccx qxs
rbx: cnd pjh zpx
plr: bjz bjt qqb chs
ztx: nlc
ttf: zff tdp qtg
zdr: gsd ncd
zfj: jtd ghc tdr
vzx: znq kdb
lrm: njp xpr gpg
lvr: vgd cpm lmz
xvr: thb ksb kjk npb
vqk: nfc
ndk: fkd
lgq: tkt hvz tgj vgg
kbg: nss tvl skg sps kqx
rzd: xvd ndf svb kkc
bjt: qrb mnf dvn
tdh: vns
zkd: bsk
dgv: hhs jsn sps rlz
ptd: vzb qqx
qsf: mnc
fss: nrv
rjm: ljz lbr
ppz: gsd
cjj: kxm tlt
vvr: rgz pmp
mqb: hpk thh rcq
sxq: kkc trp
sbq: stk
cnp: qzs
ngj: qzc nbl tdf
lzb: fxj dzl vfz hkb
nxl: vkg tqb lbr
pkq: dng ptt
klk: pdj
vfh: zrs qfg cpm
gqn: qxd
gjt: jmc lpr xsn
vqt: xxg qxd bsk
psf: ktj sxv tlr csb gqn qvs
tbp: zpb znj ltz sxq
gqs: qxd jbr gvl
xgt: fsc tqf ngj
vgp: kkn ksp vpz
spt: vlv
hdv: ckj rng fpq sdp
qfg: fvg vsb xbj
jlv: pkz xnd
svt: mkf shf pjv mgm jpf
hhs: vgz cls
tgr: hfd smh vbg rlx
dpm: dgj sqn cqc
vcq: lzc
gvn: lgt
mqn: cvc fbf mll
lsj: brl vmk
qgj: nkm
pzq: xvd rxg tdn zkt
ksg: fzm ktc cjb pcb
sqk: klk dvj
fgt: mgg jqt
lcm: lmh kzj mrg
zkz: jjr dvj fhj
zkr: pdj vkc nlc
kmz: lmg snq fcq gfr
ngl: fft szs rnn ptd zjc cqs
pdz: qrm
cmx: pzg
xsv: xxg rgr
rsk: zbj kxp qdl lzc
hnb: rcq prj
zdh: nbq ppz lvr nlc
vlf: pjj gmx dxp hvq kcn
mpb: kdq zzc sls xsh lgq
rch: srq vmz lgz qvc
rvb: jdj
kjg: mjm nzz dxr
xdz: rvj dkq
cgq: fvm zdh svq
ntm: jdh kvz dkd
jtd: fgk tdr kbn
fqh: ngc sdp qsc
cfb: bkc rkl jhz
bcs: djl
szx: bdt rzt
zqh: ftz bvg
nxq: fvl
jtp: jqt nkp xjf zpx
zqk: csj sbj
qks: nqv jjv bjt
dks: mnm crd bsk
czk: zhx
xvn: smh
bcl: hdc cnz qff qqx
lgv: lgk kft blf
thb: nrq
vbg: gpg gtr jmg lxm
dqb: tmq snt
mqf: pbl
dgh: zzk qlv ntl
nbz: dvb
hfm: njl jkb hqg hdx sdg lvk
znt: tbn
tcx: jdf cpc sxb kzn ddk
rcl: rzh jjb tqb dqh
flh: mgg ncd tdx lmz
jll: mnc drt nzm gqf
scc: mgk zzd
vjp: cng ljz
fvl: fxt trb
gbs: qlz
tjp: xqt hmm prm lsh
qhg: rct dvb srd hfb
dqm: mqb
nvm: qqz knb
vlt: tmg jtd
vtd: xpm mmt rtk dgp tkg nbz
cdq: lfj hvv nzm mgl
ktc: rvb xrr jhp
fjq: mnm pql
tjk: pdz lzc
jts: mnc prl tqv
zpl: vfn pfb
mtb: dzj mjq jkb lcn
hdl: thb brx tct hmn xpz
bxn: dds bnj tdg
kxc: lsj qdx rtk
dnf: bqp rcl dcn
rjf: jdl vmg
csn: ptq ppv
khl: tkt prs zdr lcp
csx: vfn sxb
kph: zhx ztv qqx
hbg: xdm xfk
jvk: jpx kkc
jzn: vmg vzs sst gqn rzq dtl
gmp: ttf vlt lsh
qgz: hbx bnt mvn bqf
xdp: plc prc qvc
crp: jmc
sdg: fzs zbh kkg
kkq: bhr rkl hht
lxq: ljl nbz jhz bbm zhc
bzl: qxl jxk xrr nxh rdz
hkb: rzz
dnd: rvk pcb mtj
hql: hnd tmv dpq
qsv: rpj jdf fsb dzn
nbv: bdd lpr ppz
zgh: nps
jnz: vqt cnp
svq: kmt
sch: gsf
xnb: lxm zbn jsl mtr
zbn: gkp tnp
nps: ndk vcq gdn
szd: mtz kkg dvn rgl
lvk: dvh
mfs: fcl dgz
phm: tdl
zkh: lsb ppv
pxr: ngp bxn tql vzb
tqf: qgg
qng: ltj vzx mvt qlz
sjt: gjg
ktn: zlh snq
tbt: zdd srn
gxs: shq
dxv: gmx rsh
hjk: jts jsd cbg xql
ldj: glg xbc xcz
shn: kjq
shh: pkq xqt pmm vnl dfx
stb: gjs xfv ckk nfc
tsr: gxt rdl nrm ssz xcb
vhn: ztg jlr xlg zrq kmc
zdg: fgt dvx
cbx: bqv vts hdk rqt
qrs: jhz qrb dng czb
cgb: xql stc jkf zff
srq: dsr
tdx: zkz ndk xlg
jdg: xjg jsl qlz xqk cbg xgj
rvd: xjf rrj dnm dcn
cmj: fcj
qqk: pvc nsv kkq kqx
pzf: xzj lzc pdj
dbg: rfx sbq lgv lcp
hrn: pnl
cvn: crd
sgn: zbq tjp lvk zlh
fgz: tmq
qtp: krl
qcs: rzg zpb
pbp: flj
clk: hht sfs hks bcs
rgm: blf xsh cdp vgd
hqq: vkg jnz prj
prc: jfp lth
cpn: gvl ptq jtr
jpj: ffx ffz qbt
kbs: qks tnp mtz mnz
sgz: kbj hbx brl
jmm: fpg ltr
trr: tgj jmj pgp
nfl: fcl fgt lbr
rhb: jtr krl
bqh: nvm zmq dtx
fdr: zgh sst clx
cqt: trb flj
jdl: lgk kfc
grc: nkp xxg hnb ktj
hjl: zls jlv gsk hfx
pkz: qzs prx
tcj: ljx bqf tpr plh
dzl: zrs
bgq: xff tqv jkl cmj svh
cbh: zpl czk
rxl: dqm qcg nhn
vph: zhc
hsk: ksb zkd
hmq: jgh
vxx: ntl jkb
dsl: tqr sql szh ssz xcb
rth: pdz
fkd: lpm rzh
dmb: gkk qct
rlb: mnh dtl smf
zht: vqk gxt
tnp: lqk dtp
jct: mjv pjf cgn
bjj: ncx gqz
zls: hnb grc tlt
nqd: cmx krz nxl hfj
lnm: fft qtp
vmg: xzj
xnd: tpn
kcx: srq bzb
nhx: fss gxq vbg
sbs: kbn
pnl: brc nkp
mbt: nbx hnr bzt xgj
sqj: vxj jmm nlj
jkl: cbz vff mkf
cjl: vkg kmc zkr nfc
phc: klk vsb vdq
xpx: kdq gcd tdg thk
dng: szb glp ptb
gtd: kdh zhg
rbk: ldr prz pdr bzb
ggg: zmp hhr
kpn: fkp bfn ldz
zfn: vzv krz ncs rpj nmh
cnr: mcr gqz hfx
bjc: pbp gqf vmt sgz
vjg: jdj tmv cbz
hnr: zsx xlx dxr
kxp: kfc dds
dmq: bvh fxd
qrb: nzz qvc
msv: qrb ljv
fpq: vpn
txx: jnz pql
dsr: sdp
dmm: zhc
xfv: ngp hrn
pqn: gqf sfk gbg scp
pvs: jgh fkd
bhh: hmq jct vvd nps
qcj: lpp qvc
scl: tbn kmc bvg
zkt: zmq nzz hgq
qmk: qcj ntl
qzd: pjg ccz jgn
szs: vpv jkz vtx
lgz: jcr mbf lgt
rzq: rhb vzb nvg
jpf: tnp
kvz: dgx
grf: rzc fqf fcn
sqr: kkl szk thv
mfc: njc gqx vsd glj vlp
nnd: bsk lgp gqz
hfd: hqc xbc xcz
rrc: vpn zhg szk nhx bxs
qsg: pbb qsf
trb: ckj
vvd: tzg kfc qtp
tcn: gzz svh hfb
rdz: pms nrv
kkt: lgt czg
nlj: pqp
cnz: qsb
hkd: crz jtr tfx ndx
crd: mcg
pnh: hnj tsm
kns: zkh tlt csn sfp
pzv: gnq fsc
vkn: pgp csx tjr cnz zqk
xpq: xqc fvs
lzj: nfn jvz sfp qlr
zfx: pnb hhr rfx kxm
gcd: kjk dnm bmm dtl
hfj: nrm gjt cvn
qvg: bgm hvh kmz pnh
xfp: kqv csn tzg xgb
kvb: zpx vmg
jgx: ctn dzn fxl ghr dqb cng
hzf: nvg snt
ntv: drl bhm
gkp: tjh zck
kdp: qpz xzk fgp cpc
knb: mdh
smt: skr nbl ffz nqv
jtz: mnk cjb zpb
drx: bkc dsq
bbv: qcs
fmj: nrm zcb
csj: ftz vqk bxn
lzm: flb rkv spt
gpj: crp qrm
ccs: vpq
fvh: crv flf lvn xcs
kqz: vjq hpk gqz nbv fdx cnd
ncd: krz kkn xsg
pqr: kbn
nhn: tkf
vmt: xmg plh
kmt: tdg lkt mjf hpc xsg
qnz: dxp ztx qxd
bbk: ptt bkg
jrz: nrz lxt pvs zcr
gqz: lsb
vdq: mnm xcl tmq
ppd: gpj
hgm: gqm nln zzp zsp
gmx: jvz
dpq: jpx qzp prz
bnt: rpr
rtd: kft rjb khr dvj
rkj: fcx xnh zsx
cfg: ccx
smq: pvc mdh
sbr: qhs dzl zmp
sxv: zkj
ljz: blf
tqr: vgg
tjb: lfc srh ljz shz ncs
shf: xsd
lfs: bbv sgt cpl vlv hnq
sxr: lrk jpf gbh
qlz: hgl
bgf: mqz rpx znj
kpk: jmq vvz pgk dqm
vpd: tqt dmm
dvh: xrr jzq
gzb: fzs dqr pmp vxx
vjx: sjt sqn xpk
slh: lcm crg jpl qzc
qzk: bnj hqq zht zdh
hvv: skg jtf mnc
jkz: clx dnm
zmb: xfp kjk mkx sqk
fxj: fsb
dtx: cfh bnq
ftx: bqv jkb zmq dpq
vvc: gkt sfk xdm
frt: qht mnf rxp zpd
sgf: gdn nvg
zln: scc qml dks gpj
blm: kxd kjq jpf tqf
bdk: tdl pfb rkh
srh: sbj
kkl: hdk
hbp: qct jnz ksn qff bzk
bjz: fss
cpc: nch cng
tmm: ptd crz tmq hdc
lgp: pjh
ckm: lgt fjf
zpk: tnc nzz
mkp: pmm pkq brl ztc mrg dkr
hdt: rbm fkj jtz
nzm: lhh xbc
jcc: zmp ncd rhb
tbn: ckk
pdj: lgp
ptp: rkj gjg klr
kks: lkt bhl njs jdx
zhg: xfk nbx
zrf: fvs klc jvz pzg
ndd: pbl lhm grg pms jmg
tcr: srn krl pnl
lbm: sgc qvc
brg: srh gmx dgz xkx
xmx: hgr pgh rpx hcz
cpl: tnn crt
ckj: tjh
crt: rvb cfh xpk xjg
gpz: jcg dtp hgq
lmh: qcm jxk
lvn: qbz
zrc: pls cnv cmj
qgq: pdj klp pbh pkz
bzk: lpm fxl
tmg: gxq znl
glg: kdh ljv rgc
hbt: xff jcr
tpx: hcz rdz fvl dmm gmp
fsz: xbj
fgp: hxs khr rsh
zdz: smq hnq tkg
jlr: pgz xsv hrj
prm: tkg zck
qxs: njv
mvv: drx fkj mxp bbv
hjx: gvn nvb
tzv: lsh kkt nzz
njv: dgx
ndn: plh kqm ltj prl bsm
"""

def graph(maps):
    g = ig.Graph(len(maps))
    g.vs['name'] = list(maps.keys())
    for k, v in maps.items():
        i = g.vs.select(name_eq=k)[0].index
        for o in v:
            j = g.vs.select(name_eq=o)[0].index
            g.add_edge(i, j)
    return g.simplify()

def betweenness(maps):
    result = {x: 0. for x in maps}
    inc = 1 / len(maps)
    for a, b, c in it.combinations(maps, 3):
        if b in maps[a] and b in maps[c]:
            result[b] += inc
        if a in maps[b] and a in maps[c]:
            result[a] += inc
        if c in maps[a] and c in maps[b]:
            result[c] += inc
        pprint.pprint(result)
    return result


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    nodes = set()
    maps = dict()
    for line in text:
        a, b = line.split(': ')
        b = b.split()
        nodes.add(a)
        nodes.update(b)
        if a not in maps:
            maps[a] = set()
        maps[a].update(b)
        for n in b:
            if n not in maps:
                maps[n] = set()
            maps[n].add(a)
        # print(line)
        # pprint.pprint(maps)
        # input()

    g = graph(maps)
    geb = np.array(g.edge_betweenness())
    edges_to_remove = np.argsort(geb)[-3:]

    # for e in edges_to_remove:
    #     ei = g.es[e]
    #     print(g.vs[ei.source]['name'], g.vs[ei.target]['name'])
    g.delete_edges(edges_to_remove)
    g.vs["label"] = g.vs["name"]

    components = g.connected_components(mode='weak')
    pone = len(components[0]) * len(components[1])

    # fig, ax = plt.subplots()
    # ig.plot(g, bbox=(300, 300), margin=20, target=ax)
    # plt.show()

    # print(nodes)
    # pprint.pprint(maps)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
