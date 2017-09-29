class CalcNSH:
    def __init__(self):
        pass
    '''This a Class that can calculate the NSH and LCS'''
    def lcs(self,first,second):  
        first_length = len(first)  
        second_length = len(second)  
        size = 0  
        x = 0  
        y = 0  
        matrix = [range(second_length) for x in range(first_length)]  
        #print matrix  
        for i in range(first_length):  
            for j in range(second_length):  
                #print i,j  
                if first[i] == second[j]:  
                    if i - 1 >= 0 and j - 1 >=0:  
                        matrix[i][j] = matrix[i-1][j-1] + 1  
                    else:  
                        matrix[i][j] = 1  
                    if matrix[i][j] > size:  
                        size = matrix[i][j]  
                        x = j  
                        y = i  
                else:  
                    matrix[i][j] = 0  
        #print matrix  
        #print size,x,y   
  
        return second[x-size+1:x+1] 
    ############################################
    def xmerCalc(self,Calc_Seq):
        from Bio.Seq import Seq
        from Bio.Alphabet import IUPAC
#########################QuantiMAT2.0 universal file#####################################################        
        uni_Aleader_seq=Seq("AAAACGGTAACTTCTTTATGCTTTGACTCAG", IUPAC.unambiguous_dna)
        uni_Aarms_seq=Seq("ATCTCAGTCTCGTTAATGGATTCCT", IUPAC.unambiguous_dna)
        uni_AP_seq=Seq("GATGTGGTTGTCGTACTT", IUPAC.unambiguous_dna)
        uni_PSCP_seq=Seq("CTCTTGGAAAGAAAGT", IUPAC.unambiguous_dna)
        
        ########LCS#############
        Calc_Seq=Seq(Calc_Seq, IUPAC.unambiguous_dna).upper()
        x4merlcs_Aleader=self.lcs(str(uni_Aleader_seq),str(Calc_Seq))
        x4merlcs_Aarms=self.lcs(str(uni_Aarms_seq),str(Calc_Seq))
        x4merlcs_AP=self.lcs(str(uni_AP_seq),str(Calc_Seq))
        x4merlcs_PSCP=self.lcs(str(uni_PSCP_seq),str(Calc_Seq))
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
############################################################################
        if len(x4merlcs_Aleader) >=4:
            score_x4mer_Aleader=[]
            data_Aleader={}
            i=0
            while(i<len(x4merlcs_Aleader)-3):
                score_x4mer_Aleader.append(self.x4merScore(x4merlcs_Aleader[i:i+4]))
                i=i+1
            data_Aleader['score_x4mer_Aleader']=score_x4mer_Aleader
            NSH_Score_Aleader_SACE=sum(data_Aleader['score_x4mer_Aleader'])*WF_CEtoLeaders
            NSH_Score_Aleader_SALE=sum(data_Aleader['score_x4mer_Aleader'])*WF_LEtoLeaders
        else:
            NSH_Score_Aleader_SACE=0
            NSH_Score_Aleader_SALE=0
###############Aarms xmer Score############################################
        if len(x4merlcs_Aarms) >=4:
            i=0
            score_x4mer_Aarms=[]
            data_Aarms={}
            while(i<len(x4merlcs_Aarms)-3):
                score_x4mer_Aarms.append(self.x4merScore(x4merlcs_Aarms[i:i+4]))
                i=i+1
            data_Aarms['score_x4mer_Aarms']=score_x4mer_Aarms
            NSH_Score_Aarms_SACE=sum(data_Aarms['score_x4mer_Aarms'])*WF_CEtoAMParms
            NSH_Score_Aarms_SALE=sum(data_Aarms['score_x4mer_Aarms'])*WF_LEtoAMParms
        else:
            NSH_Score_Aarms_SACE=0
            NSH_Score_Aarms_SALE=0
###############APs xmer Score##############################################
        if len(x4merlcs_AP) >=4:
            i=0
            score_x4mer_AP=[]
            data_AP={}
            while(i<len(x4merlcs_AP)-3):
                score_x4mer_AP.append(self.x4merScore(x4merlcs_AP[i:i+4]))
                i=i+1
            data_AP['score_x4mer_AP']=score_x4mer_AP
            NSH_Score_AP_SACE=sum(data_AP['score_x4mer_AP'])*WF_CEtoAP
            NSH_Score_AP_SALE=sum(data_AP['score_x4mer_AP'])*WF_LEtoAP
        else:
            NSH_Score_AP_SACE=0
            NSH_Score_AP_SALE=0
##############PSCP x-mer Score###############################
        if len(x4merlcs_PSCP) >=4:
            i=0
            score_x4mer_PSCP=[]
            data_PSCP={}
            while(i<len(x4merlcs_PSCP)-3):
                score_x4mer_PSCP.append(self.x4merScore(x4merlcs_PSCP[i:i+4]))
                i=i+1
            data_PSCP['score_x4mer_PSCP']=score_x4mer_PSCP
            NSH_Score_PSCP_SACE=sum(data_PSCP['score_x4mer_PSCP'])*WF_LEtoPSCP
            NSH_Score_PSCP_SALE=sum(data_PSCP['score_x4mer_PSCP'])*WF_CEtoPSCP
        else:
            NSH_Score_PSCP_SACE=0
            NSH_Score_PSCP_SALE=0
#######END############
        Total_NSH_SACE= NSH_Score_Aleader_SACE+NSH_Score_Aarms_SACE+NSH_Score_AP_SACE+NSH_Score_PSCP_SACE
        Total_NSH_SALE= NSH_Score_Aleader_SALE+NSH_Score_Aarms_SALE+NSH_Score_AP_SALE+NSH_Score_PSCP_SALE
        return [Total_NSH_SACE,Total_NSH_SALE]
        
    def x4merScore(self,seq):
        SumAT=seq.count("A")+seq.count("T")
        SumGC=seq.count("G")+seq.count("C")
        Score=round((0.5*SumAT+1.0*SumGC)/4,3)
        return Score