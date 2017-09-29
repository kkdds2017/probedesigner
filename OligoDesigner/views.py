#coding:utf-8
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,response
from django.views.decorators.csrf import csrf_protect,csrf_exempt
import time
from datetime import datetime
from models import *
import sys,urllib
import base64
import Cookie
from xmerCalcNSH import *
from arithMetic import *
from searchProbe import *
from XmerCalcCELENSH import *
from django.core.context_processors import request

local='probedesigner.cn'
#local='127.0.0.1:8000'
thisyear=time.strftime('%Y',time.localtime(time.time()))

#######################实现最长公共字符查找##################################

def index(request):
    global local
    return render_to_response('bootstrap.html',{'local':local,'thisyear':thisyear},context_instance=RequestContext(request))
def eindex(request):
    global local
    return render_to_response('englishindex.html',{'local':local,'thisyear':thisyear},context_instance=RequestContext(request))
#english version######
def probedesign(request):
    global local
    return render_to_response('probedesign.html',{'local':local,'thisyear':thisyear},context_instance=RequestContext(request))
def entrez(request):
    global local
    return render_to_response('entrez.html',{'local':local,'thisyear':thisyear},context_instance=RequestContext(request))
def fromfile(request):
    global local
    return render_to_response('fromfile.html',{'local':local,'thisyear':thisyear},context_instance=RequestContext(request))
def test(request):
    global local
    return render_to_response('test.html',{'local':local,'thisyear':thisyear},context_instance=RequestContext(request))
def intro(request):
    global local
    return render_to_response('quantimat.html',{'local':local,'thisyear':thisyear},context_instance=RequestContext(request))
def startdesign(request):
    global local
    return render_to_response('startdesign.html',{
                                                  'local':local,
                                                  'thisyear':thisyear,
                                                  'sequence':request.COOKIES.get('seq',''),
                                                  'description':request.COOKIES.get('des',''),
                                                  },context_instance=RequestContext(request))

def GetMiddleStr(content,startStr,endStr):
    startIndex = content.index(startStr)
    if startIndex>=0:
        startIndex += len(startStr)
        endIndex = content.index(endStr)
    return content[startIndex:endIndex]
def tfdeal(request):
    return render_to_response('tfdealdata.html',{'local':local,
                                                 'thisyear':thisyear,
                                                 },context_instance=RequestContext(request))
@csrf_protect
def tfdealdata(request):
    if request.method=="POST":
        fdata=request.POST['fdata']
        farr=fdata.split('\r\n')
        cdata=[]
        data=[]
        f1=[]
        f2=[]
        for x in farr:
            c=x.replace(';','\t')
            d=c.split('\t')
#########################################################
            f1=d[0].split('|')
            f2=d[1].split('[')
            g=f1+f2
            data.append(g[1]+";"+g[2]+"\n")
        sdata=set(data)
        cdata=[i for i in sdata]
        return render_to_response('showtfdata.html',{'local':local,'thisyear':thisyear,'cdata':cdata,},context_instance=RequestContext(request))             
            
def oligoGC(s):
    if len(s)!= 0:
        s=s.upper()
        acount=s.count('A')
        ccount=s.count('C')
        gcount=s.count('G')
        tcount=s.count('T')
    return round(100*(gcount+ccount)/(gcount+ccount+acount+tcount))
def oligoMW(s):
    if len(s)!=0:
        s=s.upper()
        acount=s.count('A')
        ccount=s.count('C')
        gcount=s.count('G')
        tcount=s.count('T')
    return round(313.21 * acount + 329.21 * gcount + 289.18 * ccount + 304.19 * tcount  - 60.96)
def oligoTm(s):
    if len(s)!= 0:
        s=s.upper()
        acount=s.count('A')
        ccount=s.count('C')
        gcount=s.count('G')
        tcount=s.count('T') 
        if len(s)<14:
            TmValue=round(2*(acount+tcount)+4*(gcount+ccount))
        else:
            TmValue=round(64.9+41*((gcount+ccount-16.4)/len(s)))
    else:
        TmValue=0
    return TmValue
def oligoTd(s):
    if len(s)!= 0:
        s=s.upper()
        acount=s.count('A')
        ccount=s.count('C')
        gcount=s.count('G')
        tcount=s.count('T') 
        TdValue=round(2*(acount+tcount)+4(gcount+ccount))
    return TdValue

def oligoOD(s):
    if len(s)!= 0:
        s=s.upper()
        acount=s.count('A')
        ccount=s.count('C')
        gcount=s.count('G')
        tcount=s.count('T')        
        ODValue=round((1000/(gcount*8.1+ccount*6.1+acount*13.3+tcount*7.9))*1000)/1000
    else:
        ODValue=0
    return ODValue
#################################碱基互补配对函数######################################################################   
re_seq=''
def reverseOligo(ss):
    if len(ss)!= 0:
        strss=str(ss)
        for s in strss:
            global re_seq
            if s=='A':
                re_s='T'
                re_seq=re_seq+re_s
            elif s=='T':
                re_s='A'
                re_seq=re_seq+re_s
            elif s=='G':
                re_s='C'
                re_seq=re_seq+re_s
            elif s=='C':
                re_s='G'
                re_seq=re_seq+re_s
    return re_seq[::-1]
##############################################################功能实现代码区############################################
@csrf_protect
def subseq(request):
    if request.method=='POST':
        oligoseq=request.POST['oligoBox']
        seqlen=len(oligoseq)
        if seqlen !=0:
            acount=oligoseq.count('A')
            ccount=oligoseq.count('C')
            gcount=oligoseq.count('G')
            tcount=oligoseq.count('T')
            GC=oligoGC(oligoseq)
            MW=oligoMW(oligoseq)
            Tm=oligoTm(oligoseq)
            OD=oligoOD(oligoseq)
            reverse=reverseOligo(oligoseq)
            pl=probeList(reverse)
        else:
            acount=0
            ccount=0
            gcount=0
            tcount=0
            GC=0
            MW=0
            Tm=0
            OD=0
            reverse=''
            pl=''
    return render_to_response('showprobe.html',{'local':local,'thisyear':thisyear,'oligoseq':oligoseq,'seqlen':seqlen,'acount':acount,'ccount':ccount,'gcount':gcount,'tcount':tcount,'GC':GC,'MW':MW,'Tm':Tm,'OD':OD,'reverse':reverse,'pl':pl,},context_instance=RequestContext(request))             
def probeList(s):
    probedict={}
    count=1
    while(count<=len(s)/25):
        begin=25*count-25
        end=25*count
        probedict.setdefault('probe'+str(count),s[begin:end])
        count=count+1
        if count>=len(s)/25:
            probedict.setdefault('probe'+str(count+1),s[25*count:len(s)])
            break        
    return probedict
 ###############################################################################################################
def downloadentrez(request):
    if request.method=='POST':
        gid=request.POST['filename']
        from Bio import Entrez
        Entrez.email="kkds@slyyc.asia"
        handle=Entrez.efetch(db="nucleotide",id=str(gid),rettype="gb",retmode="xml")
        record=Entrez.read(handle, validate=False)
        request.session['sequence']=record[0]['GBSeq_sequence']
        aversion="N/A"
        udate="N/A" 
        protein_seq="N/A"
        return render_to_response('showentrez.html',{
                                                     'local':local,
                                                     'thisyear':thisyear,
                                                     'oligoseq':record[0]['GBSeq_sequence'],
                                                     'seqlen':record[0]['GBSeq_length'],
                                                     'cdate':record[0]['GBSeq_create-date'],
                                                     'taxonomy':record[0]['GBSeq_taxonomy'],
                                                     'organism':record[0]['GBSeq_organism'],
                                                     'locus':record[0]['GBSeq_locus'],
                                                     'source':record[0]['GBSeq_source'],
                                                     'topology':record[0]['GBSeq_topology'],
                                                     'division':record[0]['GBSeq_division'],
                                                     'accession_version': aversion,
                                                     'update_date':udate ,
                                                     'strandedness':record[0]['GBSeq_strandedness'],
                                                     'definition':record[0]['GBSeq_definition'],
                                                     'protein_seq':protein_seq,
                                                     },context_instance=RequestContext(request))
    else:
        return HttpResponse("<script>alert(‘非法参数的进入！’)</script>")
def entreztoxml(request):
    if request.method=='POST':
        content = request.FILES['file']
        name=content.name
        from os import environ  
        online = environ.get("APP_NAME", "")   
   
    if online:  
        import sae.const  
        access_key = sae.const.ACCESS_KEY  
        secret_key = sae.const.SECRET_KEY  
        appname = sae.const.APP_NAME  
        domain_name = "seq"  #刚申请的domain         
           
        import sae.storage
        s = sae.storage.Client()  
        ob = sae.storage.Object(content.read())
        cname=content.name
        cname_rb=base64.encodestring(datetime.now().strftime("%Y%m%d%H%M%S%f")+'_'+str(len(cname)))[:-3]+'.'+cname.split('.')[-1]
        fileurl = s.put(domain_name, cname_rb, ob)
        from Bio import Entrez,SeqIO
        import urllib
        from urllib import urlopen
        import re
        filetype=re.findall(r'\.[^.\\/:*?"<>|\r\n]+$',fileurl)
        global record
        if filetype[0]==".gb" :
            record=SeqIO.parse(urlopen(fileurl),"genbank")
        elif filetype[0]==".fasta":
            record=SeqIO.parse(urlopen(fileurl),"fasta")
        nr=record.next()
################模板开始渲染######################################        
        if len(nr.annotations)!=0:
            source=nr.annotations['source']
            organism=nr.annotations['organism']
            taxonomy=nr.annotations['taxonomy']
            topology=nr.annotations['topology']
        else:
            source="N/A"
            organism="N/A"
            taxonomy="N/A"
            topology="N/A"
            
        cookie=Cookie.SimpleCookie()
        #cookie['sequence']=nr.seq
        #cookie['descri']=nr.description
        #request.session['description']=nr.description
        #request.session['sequence']=nr.seq
    response=render_to_response('parselocalfile.html',{
                                                       'local':local,
                                                       'thisyear':thisyear,
                                                       'filetype':filetype[0],
                                                       'local':local,
                                                       'accessid':nr.id,
                                                       'sequence':str(nr.seq),
                                                       'description':nr.description,
                                                       'name':nr.name,
                                                     #'dbxrefs':nr.dbxrefs[0],
                                                       'source':source,
                                                       'organism':organism,
                                                       'taxonomy':taxonomy,
                                                       'topology':topology,
                                                     },context_instance=RequestContext(request))
    response.set_cookie("seq",nr.seq)
    response.set_cookie("des",nr.description)
    return response

def convertdata(request):
    if request.method=='POST':
        content = request.FILES['file']
        name=content.name
        from os import environ  
        online = environ.get("APP_NAME", "")   
   
    if online:  
        import sae.const  
        access_key = sae.const.ACCESS_KEY  
        secret_key = sae.const.SECRET_KEY  
        appname = sae.const.APP_NAME  
        domain_name = "seq"  #刚申请的domain         
           
        import sae.storage
        s = sae.storage.Client()  
        ob = sae.storage.Object(content.read())
        cname=content.name
        cname_rb=base64.encodestring(datetime.now().strftime("%Y%m%d%H%M%S%f")+'_'+str(len(cname)))[:-3]+'.'+cname.split('.')[-1]
        fileurl = s.put(domain_name, cname_rb, ob)
        from Bio import Entrez,SeqIO
        import urllib
        from urllib import urlopen
        import re
        filetype=re.findall(r'\.[^.\\/:*?"<>|\r\n]+$',fileurl)
        global record
        if filetype[0]==".gb" :
            record=SeqIO.parse(urlopen(fileurl),"genbank")
        elif filetype[0]==".fasta":
            record=SeqIO.parse(urlopen(fileurl),"fasta")
        nr=record.next()
################模板开始渲染######################################        
        if len(nr.annotations)!=0:
            source=nr.annotations['source']
            organism=nr.annotations['organism']
            taxonomy=nr.annotations['taxonomy']
            topology=nr.annotations['topology']
        else:
            source="N/A"
            organism="N/A"
            taxonomy="N/A"
            topology="N/A"
            
        cookie=Cookie.SimpleCookie()
        #cookie['sequence']=nr.seq
        #cookie['descri']=nr.description
        #request.session['description']=nr.description
        #request.session['sequence']=nr.seq
    response=render_to_response('parserresults.html',{
                                                       'local':local,
                                                       'thisyear':thisyear,
                                                     'filetype':filetype[0],
                                                     'local':local,
                                                     'accessid':nr.id,
                                                     'sequence':str(nr.seq),
                                                     'description':nr.description,
                                                     'name':nr.name,
                                                     #'dbxrefs':nr.dbxrefs[0],
                                                     'source':source,
                                                     'organism':organism,
                                                     'taxonomy':taxonomy,
                                                     'topology':topology,
                                                     },context_instance=RequestContext(request))
    response.set_cookie("seq",nr.seq)
    response.set_cookie("des",nr.description)
    return response
##############X-mer数值计算函数################

@csrf_protect                                                             
def x4merCalc(request):
    if request.method=="POST":
        from Bio.Seq import Seq
        from Bio.Alphabet import IUPAC
        
        uni_Aleader_seq=Seq("AAAACGGTAACTTCTTTATGCTTTGACTCAG", IUPAC.unambiguous_dna)
        uni_Aarms_seq=Seq("ATCTCAGTCTCGTTAATGGATTCCT", IUPAC.unambiguous_dna)
        uni_AP_seq=Seq("GATGTGGTTGTCGTACTT", IUPAC.unambiguous_dna)
        uni_PSCP_seq=Seq("CTCTTGGAAAGAAAGT", IUPAC.unambiguous_dna)
###########Server as CE Probe Weighting Factor##########################
        WF_CEtoLeaders=3
        WF_CEtoAMParms=20
        WF_CEtoAP=20
        WF_LEtoPSCP=0
###########Server as LE Probe Weighting Factor##########################
        WF_LEtoLeaders=0
        WF_LEtoAMParms=0
        WF_LEtoAP=0
        WF_CEtoPSCP=12
        
        calc_seq=Seq(request.POST['pseq'], IUPAC.unambiguous_dna).upper()
        arith = arithmetic()
        x4merlcs_Aleader=arith.lcs(str(uni_Aleader_seq),str(calc_seq))
        x4merlcslen_Aleader=arith.levenshtein(str(uni_Aleader_seq),str(calc_seq))
        x4merlcs_Aarms=arith.lcs(str(uni_Aarms_seq),str(calc_seq))
        x4merlcs_AP=arith.lcs(str(uni_AP_seq),str(calc_seq))
        x4merlcs_PSCP=arith.lcs(str(uni_PSCP_seq),str(calc_seq))
########与Aleader计算X-mer值############
        if len(x4merlcs_Aleader) >=4:
            x4mer_Aleaders=x4merlcs_Aleader+"-"+Seq(x4merlcs_Aleader,IUPAC.unambiguous_dna).reverse_complement().tostring()
            i=0
            x4mer_Aleader=[]
            score_x4mer_Aleader=[]
            data_Aleader={}
            while(i<len(x4merlcs_Aleader)-3):
                x4mer_Aleader.append(x4merlcs_Aleader[i:i+4]+"-"+Seq(x4merlcs_Aleader[i:i+4],IUPAC.unambiguous_dna).reverse_complement().tostring())
                score_x4mer_Aleader.append(x4merScore(x4merlcs_Aleader[i:i+4]))
                i=i+1
            data_Aleader['x4mer_Aleader']=x4mer_Aleader
            data_Aleader['score_x4mer_Aleader']=score_x4mer_Aleader
            NSH_Score_Aleader_SACE=sum(data_Aleader['score_x4mer_Aleader'])*WF_CEtoLeaders
            NSH_Score_Aleader_SALE=sum(data_Aleader['score_x4mer_Aleader'])*WF_LEtoLeaders
        else:
            x4mer_Aleaders=""
            data_Aleader={'x4mer_Aleader':'-','score_x4mer_Aleader':'-'}
            NSH_Score_Aleader_SACE=0
            NSH_Score_Aleader_SALE=0
########与Aarms计算X-mer值############
        if len(x4merlcs_Aarms) >=4:
            x4mer_Aarmss=x4merlcs_Aarms+"-"+Seq(x4merlcs_Aarms,IUPAC.unambiguous_dna).reverse_complement().tostring()
            i=0
            x4mer_Aarms=[]
            score_x4mer_Aarms=[]
            data_Aarms={}
            while(i<len(x4merlcs_Aarms)-3):
                x4mer_Aarms.append(x4merlcs_Aarms[i:i+4]+"-"+Seq(x4merlcs_Aarms[i:i+4],IUPAC.unambiguous_dna).reverse_complement().tostring())
                score_x4mer_Aarms.append(x4merScore(x4merlcs_Aarms[i:i+4]))
                i=i+1
            data_Aarms['x4mer_Aarms']=x4mer_Aarms
            data_Aarms['score_x4mer_Aarms']=score_x4mer_Aarms
            NSH_Score_Aarms_SACE=sum(data_Aarms['score_x4mer_Aarms'])*WF_CEtoAMParms
            NSH_Score_Aarms_SALE=sum(data_Aarms['score_x4mer_Aarms'])*WF_LEtoAMParms
        else:
            x4mer_Aarmss=""
            data_Aarms={'x4mer_Aarms':'-','score_x4mer_Aarms':'-'}
            NSH_Score_Aarms_SACE=0
            NSH_Score_Aarms_SALE=0
#####################与AP探针计算x-mer的值########
        if len(x4merlcs_AP) >=4:
            x4mer_APs=x4merlcs_AP+"-"+Seq(x4merlcs_AP,IUPAC.unambiguous_dna).reverse_complement().tostring()
            i=0
            x4mer_AP=[]
            score_x4mer_AP=[]
            data_AP={}
            while(i<len(x4merlcs_AP)-3):
                x4mer_AP.append(x4merlcs_AP[i:i+4]+"-"+Seq(x4merlcs_AP[i:i+4],IUPAC.unambiguous_dna).reverse_complement().tostring())
                score_x4mer_AP.append(x4merScore(x4merlcs_AP[i:i+4]))
                i=i+1
            data_AP['x4mer_AP']=x4mer_AP
            data_AP['score_x4mer_AP']=score_x4mer_AP
            NSH_Score_AP_SACE=sum(data_AP['score_x4mer_AP'])*WF_CEtoAP
            NSH_Score_AP_SALE=sum(data_AP['score_x4mer_AP'])*WF_LEtoAP
        else:
            x4mer_APs=""
            data_AP={'x4mer_AP':'-','score_x4mer_AP':'-'}
            NSH_Score_AP_SACE=0
            NSH_Score_AP_SALE=0
##############与PSCP探针计算x-mer的值###############################
        if len(x4merlcs_PSCP) >=4:
            x4mer_PSCPs=x4merlcs_PSCP+"-"+Seq(x4merlcs_PSCP,IUPAC.unambiguous_dna).reverse_complement().tostring()
            i=0
            x4mer_PSCP=[]
            score_x4mer_PSCP=[]
            data_PSCP={}
            while(i<len(x4merlcs_PSCP)-3):
                x4mer_PSCP.append(x4merlcs_PSCP[i:i+4]+"-"+Seq(x4merlcs_PSCP[i:i+4],IUPAC.unambiguous_dna).reverse_complement().tostring())
                score_x4mer_PSCP.append(x4merScore(x4merlcs_PSCP[i:i+4]))
                i=i+1
            data_PSCP['x4mer_PSCP']=x4mer_PSCP
            data_PSCP['score_x4mer_PSCP']=score_x4mer_PSCP
            NSH_Score_PSCP_SACE=sum(data_PSCP['score_x4mer_PSCP'])*WF_LEtoPSCP
            NSH_Score_PSCP_SALE=sum(data_PSCP['score_x4mer_PSCP'])*WF_CEtoPSCP
        else:
            x4mer_PSCPs=""
            data_PSCP={'x4mer_PSCP':'-','score_x4mer_PSCP':'-'}
            NSH_Score_PSCP_SACE=0
            NSH_Score_PSCP_SALE=0
#######END############
        Total_NSH_SACE= NSH_Score_Aleader_SACE+NSH_Score_Aarms_SACE+NSH_Score_AP_SACE+NSH_Score_PSCP_SACE
        Total_NSH_SALE= NSH_Score_Aleader_SALE+NSH_Score_Aarms_SALE+NSH_Score_AP_SALE+NSH_Score_PSCP_SALE
        
#############模板渲染开始##########################
        return render_to_response('showcalcresult.html',{
                                                     'local':local,
                                                     'thisyear':thisyear,
                                                     'x4merlcs_Aleader':x4merlcs_Aleader,
                                                     'x4merlcslen_Aleader':x4merlcslen_Aleader,
                                                     'uni_Aleader_seq':uni_Aleader_seq,
                                                     'uni_Aarms_seq':uni_Aarms_seq,
                                                     'uni_AP_seq':uni_AP_seq,
                                                     'uni_PSCP_seq':uni_PSCP_seq,
                                                     'calc_seq':calc_seq,
                                                     'x4mer_Aleaders':x4mer_Aleaders,
                                                     'x4mer_Aarmss':x4mer_Aarmss,
                                                     'x4mer_APs':x4mer_APs,
                                                     'x4mer_PSCPs':x4mer_PSCPs,
                                                     'x4mer_Aleader':data_Aleader['x4mer_Aleader'],
                                                     'score_x4mer_Aleader':data_Aleader['score_x4mer_Aleader'],
                                                     'NSH_Score_Aleader_SACE':NSH_Score_Aleader_SACE,
                                                     'NSH_Score_Aleader_SALE':NSH_Score_Aleader_SALE,
                                                     'x4mer_Aarmss':x4mer_Aarmss,
                                                     'x4mer_Aarms':data_Aarms['x4mer_Aarms'],
                                                     'score_x4mer_Aarms':data_Aarms['score_x4mer_Aarms'],
                                                     'NSH_Score_Aarms_SACE':NSH_Score_Aarms_SACE,
                                                     'NSH_Score_Aarms_SALE':NSH_Score_Aarms_SALE,
                                                     'x4mer_APs':x4mer_APs,
                                                     'x4mer_AP':data_AP['x4mer_AP'],
                                                     'score_x4mer_AP':data_AP['score_x4mer_AP'],
                                                     'NSH_Score_AP_SACE':NSH_Score_AP_SACE,
                                                     'NSH_Score_AP_SALE':NSH_Score_AP_SALE,
                                                     'x4mer_PSCPs':x4mer_PSCPs,
                                                     'x4mer_PSCP':data_PSCP['x4mer_PSCP'],
                                                     'score_x4mer_PSCP':data_PSCP['score_x4mer_PSCP'],
                                                     'NSH_Score_PSCP_SACE':NSH_Score_PSCP_SACE,
                                                     'NSH_Score_PSCP_SALE':NSH_Score_PSCP_SALE,
                                                     'Total_NSH_SACE':Total_NSH_SACE,
                                                     'Total_NSH_SALE':Total_NSH_SALE,
                                                     },context_instance=RequestContext(request))
def x4merScore(seq):
    SumAT=seq.count("A")+seq.count("T")
    SumGC=seq.count("G")+seq.count("C")
    Score=round((0.5*SumAT+1.0*SumGC)/4,3)
    return Score  

##################################################################
@csrf_protect    
def NonNshFilter(req):
    if req.method=='POST':
        nonnshfilter=NonNSHFilter()
        probedict={}
        probelist=nonnshfilter.filterSequence(req.POST['seqtxt'])
        s=req.POST['seqtxt'].upper()
        probelist.append(len(s))
        for i in range(len(probelist)):
            if probelist[i]<len(s)-20:
#计算GC含量以及计算CE&LE 公式：
                probedict.setdefault('p'+str(probelist[i]),[s[probelist[i]:probelist[i+1]],probelist[i]])
        return render_to_response('showfilterprobe.html',{
                                                     'local':local,
                                                     'thisyear':thisyear,
                                                     'probedict':probedict,
                                                     },context_instance=RequestContext(req))  
##################################################################
@csrf_protect    
def Probelist(req):
    if req.method=='POST':
        nonnshfilter=NonNSHFilter()
        probedict={}
        probelist=nonnshfilter.filterSequence(req.POST['seqtxt'])
        s=req.POST['seqtxt'].upper()
        probelist.append(len(s))
        for i in range(len(probelist)):
            if probelist[i]<len(s)-20:
#计算GC含量以及计算CE&LE 公式：
                probedict.setdefault('p'+str(probelist[i]),[s[probelist[i]:probelist[i+1]],probelist[i]])
        return render_to_response('probelist.html',{
                                                     'local':local,
                                                     'thisyear':thisyear,
                                                     'probedict':probedict,
                                                     },context_instance=RequestContext(req))   
def PostCalcXmer(req):
    if req.method=='POST':
        dict_xmervalue=[]
        probe_xmer_list=[]
        probe_xmer_dict={}
        dict_value=req.POST.getlist('probedictvalue','')
        dict_key=req.POST.getlist('probedictkey','')
        dict_length=req.POST.getlist('probelength','')
        xmerclac=CalcNSH()
        for i in range(len(dict_value)):
            dict_xmervalue.append(xmerclac.xmerCalc(dict_value[i]))
        for v in range(len(dict_xmervalue)):
            probe_xmer_dict.setdefault(dict_key[v],[dict_xmervalue[v],int(dict_length[v]),dict_value[v],oligoGC(dict_value[v])])
        probe_xmer_list=sorted(probe_xmer_dict.items(),key=lambda x:x[1][1])
        return render_to_response('showxmerscore.html',{
                                                                              'local':local,
                                                                              'thisyear':thisyear,
                                                                              'probe_xmer_list':probe_xmer_list,
                                                                              },context_instance=RequestContext(req))
#########################CE&LE cross#################################
###################################################
def Universalvalue(req):
    if req.method=='POST':
        dict_xmervalue=[]
        probe_xmer_list=[]
        probe_xmer_dict={}
        dict_value=req.POST.getlist('probedictvalue','')
        dict_key=req.POST.getlist('probedictkey','')
        dict_length=req.POST.getlist('probelength','')
        xmerclac=CalcNSH()
        for i in range(len(dict_value)):
            dict_xmervalue.append(xmerclac.xmerCalc(dict_value[i]))
        for v in range(len(dict_xmervalue)):
            probe_xmer_dict.setdefault(dict_key[v],[dict_xmervalue[v],int(dict_length[v]),dict_value[v],oligoGC(dict_value[v])])
        probe_xmer_list=sorted(probe_xmer_dict.items(),key=lambda x:x[1][1])
        return render_to_response('universalvalue.html',{
                                                                              'local':local,
                                                                              'thisyear':thisyear,
                                                                              'probe_xmer_list':probe_xmer_list,
                                                                              },context_instance=RequestContext(req))
#########################CE&LE cross#################################
####################################################
def ProbeSetsXmer(req):
    if req.method=="POST":
        CE_plist=[]
        LE_plist=[]
        BL_plist=[]
        list_pkey=req.POST.getlist("pkey")
        list_pseq=req.POST.getlist("pseq")
        list_CE=req.POST.getlist("CEcheck")
        list_LE=req.POST.getlist("LEcheck")
        list_BL=req.POST.getlist("BLcheck")
        probesets_list=[]
        for i in range(len(list_pkey)):
            probesets_list.append((list_pkey[i],list_pseq[i],list_CE[i],list_LE[i],list_BL[i]))
        for j in range(len(probesets_list)):
            if probesets_list[j][2]=="CE":
                CE_plist.append((probesets_list[j][0],probesets_list[j][1]))
            if probesets_list[j][3]=="LE":
                LE_plist.append((probesets_list[j][0],probesets_list[j][1]))
            if probesets_list[j][4]=="BL":
                BL_plist.append((probesets_list[j][0],probesets_list[j][1]))
        xmerclaccele=CalcCELENSH()
        CEtoLE_score_list=[]
        CEtoLE_score=[]
        LE_plist1=[]
        LE_plist2=[]  
        LE_plist3=[]
        LE_plist4=[]
        LE_plist5=[]
        LE_plist6=[]
        LE_plist7=[]
        len_lep=len(LE_plist)
        if len_lep<=15:
            LE_plist1=LE_plist[0:len(LE_plist)]
        elif 16<len_lep<=30:
            LE_plist1=LE_plist[0:15]
            LE_plist2=LE_plist[15:len(LE_plist)]
        elif 31<len_lep<=45:
            LE_plist1=LE_plist[0:15]
            LE_plist2=LE_plist[15:30]  
            LE_plist3=LE_plist[30:len(LE_plist)]
        elif 46<len_lep<=60:
            LE_plist1=LE_plist[0:15]
            LE_plist2=LE_plist[15:30]  
            LE_plist3=LE_plist[30:45]
            LE_plist4=LE_plist[45:len(LE_plist)]
        elif 61<len_lep<=75:
            LE_plist1=LE_plist[0:15]
            LE_plist2=LE_plist[15:30]  
            LE_plist3=LE_plist[30:45]
            LE_plist4=LE_plist[45:60]
            LE_plist5=LE_plist[60:len(LE_plist)]
        elif 76<len_lep<=90:
            LE_plist1=LE_plist[0:15]
            LE_plist2=LE_plist[15:30]  
            LE_plist3=LE_plist[30:45]
            LE_plist4=LE_plist[45:60]
            LE_plist5=LE_plist[60:75]
            LE_plist6=LE_plist[75:len(LE_plist)]
        elif 91<len_lep<=105:
            LE_plist1=LE_plist[0:15]
            LE_plist2=LE_plist[15:30]  
            LE_plist3=LE_plist[30:45]
            LE_plist4=LE_plist[45:60]
            LE_plist5=LE_plist[60:75]
            LE_plist6=LE_plist[75:90]
            LE_plist7=LE_plist[90:len(LE_plist)]
        for c in range(len(CE_plist)):
            for l in range(len(LE_plist)):
                CEtoLE_score.append(xmerclaccele.xmerCalcCELE(CE_plist[c][1], LE_plist[l][1]))
            CEtoLE_score_list.append((CE_plist[c][0],CEtoLE_score[len_lep*c:(c+1)*len_lep]))
            
        CEtoLE_score_list1=[]
        CEtoLE_score_list2=[]
        CEtoLE_score_list3=[]
        CEtoLE_score_list4=[]
        CEtoLE_score_list5=[]
        CEtoLE_score_list6=[]
        CEtoLE_score_list7=[]
        
        if len_lep<=15:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:len_lep]))
        elif 15<len_lep<=30:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:15]))
                CEtoLE_score_list2.append((clsl[0],clsl[1][15:len_lep]))
        elif 30<len_lep<=45:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:15]))
                CEtoLE_score_list2.append((clsl[0],clsl[1][15:30]))
                CEtoLE_score_list3.append((clsl[0],clsl[1][30:len_lep]))
        elif 45<len_lep<=60:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:15]))
                CEtoLE_score_list2.append((clsl[0],clsl[1][15:30]))
                CEtoLE_score_list3.append((clsl[0],clsl[1][30:45]))
                CEtoLE_score_list4.append((clsl[0],clsl[1][45:len_lep]))
        elif 60<len_lep<=75:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:15]))
                CEtoLE_score_list2.append((clsl[0],clsl[1][15:30]))
                CEtoLE_score_list3.append((clsl[0],clsl[1][30:45]))
                CEtoLE_score_list4.append((clsl[0],clsl[1][45:60]))
                CEtoLE_score_list5.append((clsl[0],clsl[1][60:len_lep]))
        elif 75<len_lep<=90:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:15]))
                CEtoLE_score_list2.append((clsl[0],clsl[1][15:30]))
                CEtoLE_score_list3.append((clsl[0],clsl[1][30:45]))
                CEtoLE_score_list4.append((clsl[0],clsl[1][45:60]))
                CEtoLE_score_list5.append((clsl[0],clsl[1][60:75])) 
                CEtoLE_score_list6.append((clsl[0],clsl[1][75:len_lep]))
        elif 90<len_lep<=105:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:15]))
                CEtoLE_score_list2.append((clsl[0],clsl[1][15:30]))
                CEtoLE_score_list3.append((clsl[0],clsl[1][30:45]))
                CEtoLE_score_list4.append((clsl[0],clsl[1][45:60]))
                CEtoLE_score_list5.append((clsl[0],clsl[1][60:75])) 
                CEtoLE_score_list6.append((clsl[0],clsl[1][75:90]))
                CEtoLE_score_list6.append((clsl[0],clsl[1][90:len_lep]))       
                
        return render_to_response('showceleNSH.html',{
                                                        'local':local,
                                                        'thisyear':thisyear,
                                                        'len_lep':len_lep,
                                                        'LE_plist':LE_plist,
                                                        'LE_plist1':LE_plist1,
                                                        'LE_plist2':LE_plist2,
                                                        'LE_plist3':LE_plist3,
                                                        'LE_plist4':LE_plist4,
                                                        'LE_plist5':LE_plist5,
                                                        'LE_plist6':LE_plist6,
                                                        'LE_plist7':LE_plist7,
                                                        'CE_plist':CE_plist,
                                                        'BL_plist':BL_plist,
                                                        'CEtoLE_score_list':CEtoLE_score_list,
                                                        'CEtoLE_score_list1':CEtoLE_score_list1,
                                                        'CEtoLE_score_list2':CEtoLE_score_list2,
                                                        'CEtoLE_score_list3':CEtoLE_score_list3,
                                                        'CEtoLE_score_list4':CEtoLE_score_list4,
                                                        'CEtoLE_score_list5':CEtoLE_score_list5,
                                                        'CEtoLE_score_list6':CEtoLE_score_list6,
                                                        'CEtoLE_score_list7':CEtoLE_score_list7,
                                                        },context_instance=RequestContext(req))   
##################################Generate probe sets#####################################################
def Probegroupsvalues(req):
    if req.method=="POST":
        CE_plist=[]
        LE_plist=[]
        BL_plist=[]
        list_pkey=req.POST.getlist("pkey")
        list_pseq=req.POST.getlist("pseq")
        list_CE=req.POST.getlist("CEcheck")
        list_LE=req.POST.getlist("LEcheck")
        list_BL=req.POST.getlist("BLcheck")
        probesets_list=[]
        for i in range(len(list_pkey)):
            probesets_list.append((list_pkey[i],list_pseq[i],list_CE[i],list_LE[i],list_BL[i]))
        for j in range(len(probesets_list)):
            if probesets_list[j][2]=="CE":
                CE_plist.append((probesets_list[j][0],probesets_list[j][1]))
            if probesets_list[j][3]=="LE":
                LE_plist.append((probesets_list[j][0],probesets_list[j][1]))
            if probesets_list[j][4]=="BL":
                BL_plist.append((probesets_list[j][0],probesets_list[j][1]))
        xmerclaccele=CalcCELENSH()
        CEtoLE_score_list=[]
        CEtoLE_score=[]
        LE_plist1=[]
        LE_plist2=[]  
        LE_plist3=[]
        LE_plist4=[]
        LE_plist5=[]
        LE_plist6=[]
        LE_plist7=[]
        len_lep=len(LE_plist)
        if len_lep<=15:
            LE_plist1=LE_plist[0:len(LE_plist)]
        elif 16<len_lep<=30:
            LE_plist1=LE_plist[0:15]
            LE_plist2=LE_plist[15:len(LE_plist)]
        elif 31<len_lep<=45:
            LE_plist1=LE_plist[0:15]
            LE_plist2=LE_plist[15:30]  
            LE_plist3=LE_plist[30:len(LE_plist)]
        elif 46<len_lep<=60:
            LE_plist1=LE_plist[0:15]
            LE_plist2=LE_plist[15:30]  
            LE_plist3=LE_plist[30:45]
            LE_plist4=LE_plist[45:len(LE_plist)]
        elif 61<len_lep<=75:
            LE_plist1=LE_plist[0:15]
            LE_plist2=LE_plist[15:30]  
            LE_plist3=LE_plist[30:45]
            LE_plist4=LE_plist[45:60]
            LE_plist5=LE_plist[60:len(LE_plist)]
        elif 76<len_lep<=90:
            LE_plist1=LE_plist[0:15]
            LE_plist2=LE_plist[15:30]  
            LE_plist3=LE_plist[30:45]
            LE_plist4=LE_plist[45:60]
            LE_plist5=LE_plist[60:75]
            LE_plist6=LE_plist[75:len(LE_plist)]
        elif 91<len_lep<=105:
            LE_plist1=LE_plist[0:15]
            LE_plist2=LE_plist[15:30]  
            LE_plist3=LE_plist[30:45]
            LE_plist4=LE_plist[45:60]
            LE_plist5=LE_plist[60:75]
            LE_plist6=LE_plist[75:90]
            LE_plist7=LE_plist[90:len(LE_plist)]
        for c in range(len(CE_plist)):
            for l in range(len(LE_plist)):
                CEtoLE_score.append(xmerclaccele.xmerCalcCELE(CE_plist[c][1], LE_plist[l][1]))
            CEtoLE_score_list.append((CE_plist[c][0],CEtoLE_score[len_lep*c:(c+1)*len_lep]))
            
        CEtoLE_score_list1=[]
        CEtoLE_score_list2=[]
        CEtoLE_score_list3=[]
        CEtoLE_score_list4=[]
        CEtoLE_score_list5=[]
        CEtoLE_score_list6=[]
        CEtoLE_score_list7=[]
        
        if len_lep<=15:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:len_lep]))
        elif 15<len_lep<=30:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:15]))
                CEtoLE_score_list2.append((clsl[0],clsl[1][15:len_lep]))
        elif 30<len_lep<=45:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:15]))
                CEtoLE_score_list2.append((clsl[0],clsl[1][15:30]))
                CEtoLE_score_list3.append((clsl[0],clsl[1][30:len_lep]))
        elif 45<len_lep<=60:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:15]))
                CEtoLE_score_list2.append((clsl[0],clsl[1][15:30]))
                CEtoLE_score_list3.append((clsl[0],clsl[1][30:45]))
                CEtoLE_score_list4.append((clsl[0],clsl[1][45:len_lep]))
        elif 60<len_lep<=75:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:15]))
                CEtoLE_score_list2.append((clsl[0],clsl[1][15:30]))
                CEtoLE_score_list3.append((clsl[0],clsl[1][30:45]))
                CEtoLE_score_list4.append((clsl[0],clsl[1][45:60]))
                CEtoLE_score_list5.append((clsl[0],clsl[1][60:len_lep]))
        elif 75<len_lep<=90:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:15]))
                CEtoLE_score_list2.append((clsl[0],clsl[1][15:30]))
                CEtoLE_score_list3.append((clsl[0],clsl[1][30:45]))
                CEtoLE_score_list4.append((clsl[0],clsl[1][45:60]))
                CEtoLE_score_list5.append((clsl[0],clsl[1][60:75])) 
                CEtoLE_score_list6.append((clsl[0],clsl[1][75:len_lep]))
        elif 90<len_lep<=105:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:15]))
                CEtoLE_score_list2.append((clsl[0],clsl[1][15:30]))
                CEtoLE_score_list3.append((clsl[0],clsl[1][30:45]))
                CEtoLE_score_list4.append((clsl[0],clsl[1][45:60]))
                CEtoLE_score_list5.append((clsl[0],clsl[1][60:75])) 
                CEtoLE_score_list6.append((clsl[0],clsl[1][75:90]))
                CEtoLE_score_list6.append((clsl[0],clsl[1][90:len_lep]))       
                
        return render_to_response('probegroupsvalues.html',{
                                                        'local':local,
                                                        'thisyear':thisyear,
                                                        'len_lep':len_lep,
                                                        'LE_plist':LE_plist,
                                                        'LE_plist1':LE_plist1,
                                                        'LE_plist2':LE_plist2,
                                                        'LE_plist3':LE_plist3,
                                                        'LE_plist4':LE_plist4,
                                                        'LE_plist5':LE_plist5,
                                                        'LE_plist6':LE_plist6,
                                                        'LE_plist7':LE_plist7,
                                                        'CE_plist':CE_plist,
                                                        'BL_plist':BL_plist,
                                                        'CEtoLE_score_list':CEtoLE_score_list,
                                                        'CEtoLE_score_list1':CEtoLE_score_list1,
                                                        'CEtoLE_score_list2':CEtoLE_score_list2,
                                                        'CEtoLE_score_list3':CEtoLE_score_list3,
                                                        'CEtoLE_score_list4':CEtoLE_score_list4,
                                                        'CEtoLE_score_list5':CEtoLE_score_list5,
                                                        'CEtoLE_score_list6':CEtoLE_score_list6,
                                                        'CEtoLE_score_list7':CEtoLE_score_list7,
                                                        },context_instance=RequestContext(req))   
##################################Generate probe sets#####################################################
def GenerateProbesets(req):
    if req.method=="POST":
        probesname=req.POST.getlist("probename")
        probesseq=req.POST.getlist("probeseq")
        probesfunc=req.POST.getlist("probefunc")
        probesets_list=[]
        for i in range(len(probesname)):
            probesets_list.append((probesname[i],probesseq[i],probesfunc[i]))
        CE_final_list=[]
        LE_final_list=[]
        BL_final_list=[]
        for j in range(len(probesets_list)):
            if probesets_list[j][2]=="CE":
                CE_final_list.append((probesets_list[j][0],probesets_list[j][1]+'tttttCTCTTGGAAAGAAAGT'))
            if probesets_list[j][2]=="BL":
                BL_final_list.append((probesets_list[j][0],probesets_list[j][1]))
            if probesets_list[j][2]=="LE":
                LE_final_list.append((probesets_list[j][0],probesets_list[j][1]))
        LE_final_final_list=[]
        for k in range(len(LE_final_list)):
            if LE_final_list.index(LE_final_list[k])%2==0:
                LE_final_final_list.append((LE_final_list[k][0],LE_final_list[k][1]+'TTTTTgaagttaccgtttt'))
            else:
                LE_final_final_list.append((LE_final_list[k][0],LE_final_list[k][1]+'TTTTTctgagtcaaagcat'))
        return render_to_response('generateprobes.html',{
                                      'local':local,
                                      'thisyear':thisyear,
                                      'CE_final_list':CE_final_list,
                                      'BL_final_list':BL_final_list,
                                      'LE_final_final_list':LE_final_final_list,
                                      },context_instance=RequestContext(req))
def Probesetsgenerate(req):
    if req.method=="POST":
        probesname=req.POST.getlist("probename")
        probesseq=req.POST.getlist("probeseq")
        probesfunc=req.POST.getlist("probefunc")
        probesets_list=[]
        for i in range(len(probesname)):
            probesets_list.append((probesname[i],probesseq[i],probesfunc[i]))
        CE_final_list=[]
        LE_final_list=[]
        BL_final_list=[]
        for j in range(len(probesets_list)):
            if probesets_list[j][2]=="CE":
                CE_final_list.append((probesets_list[j][0],probesets_list[j][1]+'tttttCTCTTGGAAAGAAAGT'))
            if probesets_list[j][2]=="BL":
                BL_final_list.append((probesets_list[j][0],probesets_list[j][1]))
            if probesets_list[j][2]=="LE":
                LE_final_list.append((probesets_list[j][0],probesets_list[j][1]))
        LE_final_final_list=[]
        for k in range(len(LE_final_list)):
            if LE_final_list.index(LE_final_list[k])%2==0:
                LE_final_final_list.append((LE_final_list[k][0],LE_final_list[k][1]+'TTTTTgaagttaccgtttt'))
            else:
                LE_final_final_list.append((LE_final_list[k][0],LE_final_list[k][1]+'TTTTTctgagtcaaagcat'))
        return render_to_response('probelistgenerate.html',{
                                      'local':local,
                                      'thisyear':thisyear,
                                      'CE_final_list':CE_final_list,
                                      'BL_final_list':BL_final_list,
                                      'LE_final_final_list':LE_final_final_list,
                                      },context_instance=RequestContext(req))

############################ 软件英文版入口##################################################
def english(request):
    global local
    return render_to_response('english.html',{'local':local,'thisyear':thisyear},context_instance=RequestContext(request))
def bingodesign(request):
    global local
    return render_to_response('bingodesign.html',{
                                                  'local':local,
                                                  'thisyear':thisyear,
                                                  'sequence':request.COOKIES.get('seq',''),
                                                  'description':request.COOKIES.get('des',''),
                                                  },context_instance=RequestContext(request))
def BigData(request):
    global local
    from Bio import Entrez
    Entrez.email = "A.N.Other@example.com" 
    handle = Entrez.egquery(term="bDNA")
    handle1= Entrez.egquery(term="pcr")
    record = Entrez.read(handle)
    record1= Entrez.read(handle1)
    bDNA=[]
    pcr=[]
    for row0 in record["eGQueryResult"]: 
        bDNA.append([row0["Count"],row0["DbName"]])
    for row1 in record1["eGQueryResult"]: 
        pcr.append([row1["Count"],row1["DbName"]])
    return render_to_response('bigdata.html',{
                                                  'local':local,
                                                  'thisyear':thisyear,
                                                  'bDNA':bDNA,
                                                  'pcr':pcr,
                                                  },context_instance=RequestContext(request))
    
    
