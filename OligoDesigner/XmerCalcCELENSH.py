class CalcCELENSH:
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
    def xmerCalcCELE(self,Calc_Seq1,Calc_Seq2):
        from Bio.Seq import Seq
        from Bio.Alphabet import IUPAC
        
        ########LCS#############
        Calc_Seq1=Seq(Calc_Seq1, IUPAC.unambiguous_dna).upper()
        Calc_Seq2=Seq(Calc_Seq2, IUPAC.unambiguous_dna).upper()
        
        x4merlcs_CE_LE=self.lcs(str(Calc_Seq1),str(Calc_Seq2))
###########Server as CE Probe Weighting Factor##########################
        WF_CEtoLE=6
############################################################################
        if len(x4merlcs_CE_LE) >=4:
            score_x4mer_CEtoLE=[]
            data_CEtoLE={}
            i=0
            while(i<len(x4merlcs_CE_LE)-3):
                score_x4mer_CEtoLE.append(self.x4merScore(x4merlcs_CE_LE[i:i+4]))
                i=i+1
            data_CEtoLE['score_x4mer_CEtoLE']=score_x4mer_CEtoLE
            NSH_Score_CEtoLE=sum(data_CEtoLE['score_x4mer_CEtoLE'])*WF_CEtoLE
        else:
            NSH_Score_CEtoLE=0
        return NSH_Score_CEtoLE
        
    def x4merScore(self,seq):
        SumAT=seq.count("A")+seq.count("T")
        SumGC=seq.count("G")+seq.count("C")
        Score=round((0.5*SumAT+1.0*SumGC)/4,3)
        return Score
