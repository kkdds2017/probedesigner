 
function Calculate(form) {

newOligo = new Oligo(form.oligoBox.value)

form.oligoBox.value = newOligo.Sequence

form.tmBox.value = newOligo.Tm()

form.gcBox.value = newOligo.GC()

form.mwBox.value = newOligo.MW()

form.odBox.value = newOligo.OD()

form.lBox.value = newOligo.Sequence.length

form.AcountBox.value=newOligo.aCount

form.GcountBox.value=newOligo.gCount

form.CcountBox.value=newOligo.cCount

form.TcountBox.value=newOligo.tCount

form.JcountBox.value=newOligo.jCount

form.FcountBox.value=newOligo.fCount

}



function Oligo(theString)

{

this.Sequence = RemoveNonBase(theString)

this.aCount = CountChar(theString,"A")

this.cCount = CountChar(theString,"C")

this.gCount = CountChar(theString,"G")

this.tCount = CountChar(theString,"T")

this.jCount = CountChar(theString,"J")

this.fCount = CountChar(theString,"F")

this.Tm = Tm

this.GC = GC

this.MW = MW

this.OD = OD

}



function OD()

{

if (this.Sequence.length > 0) {

return Math.round((1000/(this.gCount * 8.1 + this.cCount * 6.1 + this.aCount * 13.3 + this.tCount * 7.9 + this.jCount*4.4 + this.fCount*5.7))*1000)/1000

}

else

{

return ""

}

}



function MW()

{

if (this.Sequence.length > 0) {

return Math.round(313.21 * this.aCount + 329.21 * this.gCount + 289.18 * this.cCount + 304.19 * this.tCount + 329.21*this.jCount + 303.21*this.fCount - 60.96)

}

else

{

return ""

}

}



function GC()

{

if (this.Sequence.length > 0) {

return Math.round(( 100 * ( this.gCount + this.cCount + this.jCount + this.fCount ) / this.Sequence.length )*10)/10

}

else

{

return ""

}

}



function Tm()

{

                if (this.Sequence.length > 0) {

                if (this.Sequence.length < 14) {

                        return  Math.round(2 * (this.aCount + this.tCount) + 4 * (this.gCount + this.cCount + this.jCount + this.fCount))

                        }

                else {

                return Math.round(64.9 + 41 * ((this.gCount + this.cCount + this.jCount + this.fCount - 16.4) / this.Sequence.length))

                        }

                        }

                else {

        return ""

}

}



function RemoveNonBase(theString) {

var returnString = ""

theString = theString.toUpperCase()

for ( var i = 0; i < theString.length; i++) {

if ((theString.charAt(i) == "A") || (theString.charAt(i) == "G") || (theString.charAt(i) == "C") || (theString.charAt(i) == "T")) {

returnString += theString.charAt(i)

}

}

return returnString

}



function CountChar(theString,theChar) {

var returnValue = 0

theString = theString.toUpperCase()

for ( var i = 0; i < theString.length; i++) {

if (theString.charAt(i) == theChar) {

returnValue ++

}

}

return returnValue

}



function Disallow(form) {

form.oligoBox.focus()

}
