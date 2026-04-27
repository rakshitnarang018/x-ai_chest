import jsPDF from "jspdf";

export default function DownloadReportButton({
 prediction,
 scanType,
 reportText,
 gradcamImage,
 limeImage,
 isDental=false
}){


const parseSections=()=>{
 if(!reportText){
  return{
   findings:"Not available",
   impression:"Not available",
   limitations:"Not available"
  };
 }

 return{
 findings:
 reportText.match(
 /Findings:\s*([\s\S]*?)Impression:/i
 )?.[1]?.trim() || reportText,

 impression:
 reportText.match(
 /Impression:\s*([\s\S]*?)Limitations:/i
 )?.[1]?.trim() || "",

 limitations:
 reportText.match(
 /Limitations:\s*([\s\S]*)/i
 )?.[1]?.trim() || ""
 };
};



const writeWrapped=(
 pdf,
 text,
 x,
 y,
 width,
 lineHeight=4.5,
 maxLines=5
)=>{
 const lines=
 pdf
 .splitTextToSize(
  text||"",
  width
 )
 .slice(0,maxLines);

 lines.forEach(
  (line,i)=>{
   pdf.text(
    line,
    x,
    y+(i*lineHeight)
   );
  }
 );
};



const sectionCard=(
 pdf,
 title,
 body,
 y,
 h=27
)=>{

pdf.setFillColor(
255,
252,
242
);

pdf.setDrawColor(
188,
204,
224
);

pdf.roundedRect(
12,y,186,h,2,2,"FD"
);


pdf.setFillColor(
50,74,104
);

pdf.rect(
12,y,186,6,"F"
);


pdf.setTextColor(
255,255,255
);

pdf.setFont(
"helvetica",
"bold"
);

pdf.setFontSize(10);

pdf.text(
title,
18,
y+4.2
);


pdf.setTextColor(
40,40,40
);

pdf.setFont(
"helvetica",
"normal"
);

pdf.setFontSize(9);

writeWrapped(
 pdf,
 body,
 18,
 y+12,
 172
);

return y+h+4;

};



const imageCard=(
pdf,
title,
img,
x,
y
)=>{
 if(!img) return;

 pdf.setFillColor(
 248,
 250,
 255
 );

 pdf.setDrawColor(
 190,
 205,
 225
 );

 pdf.roundedRect(
  x,
  y,
 78,
 60,
 2,
 2,
  "FD"
 );

 pdf.setFont(
  "helvetica",
  "bold"
 );

 pdf.setFontSize(8);

 pdf.setTextColor(
 55,
 55,
 55
 );

 pdf.text(
  title,
  x+4,
  y+5
 );

 pdf.addImage(
  img,
  "PNG",
  x+4,
  y+8,
  70,
  46
 );
};



const generatePdf=()=>{

const pdf=
new jsPDF(
 "p",
 "mm",
 "a4"
);

const {
 findings,
 impression,
 limitations
}=parseSections();



/* Background */
pdf.setFillColor(
255,
252,
240
);

pdf.rect(
0,
0,
210,
297,
"F"
);



/* Header */
pdf.setFillColor(
52,
74,
104
);

pdf.rect(
0,
0,
210,
24,
"F"
);


pdf.setFillColor(
255,
255,
255
);

pdf.circle(
15,
12,
5,
"F"
);

pdf.setTextColor(
52,
74,
104
);

pdf.setFontSize(8);

pdf.text(
"AI",
13.5,
13
);


pdf.setTextColor(
255,
255,
255
);

pdf.setFont(
"helvetica",
"bold"
);

pdf.setFontSize(18);

pdf.text(
"Explainable Radiology Assistant",
24,
10.5
);

pdf.setFontSize(8.5);

pdf.text(
"Clinical Decision Support Diagnostic Report",
24,
17
);


/* timestamp only here */
pdf.setFillColor(
245,
247,
250
);

pdf.roundedRect(
152,
5,
43,
10,
2,
2,
"F"
);

pdf.setTextColor(
45,
45,
45
);

pdf.setFontSize(7);

pdf.text(
new Date().toLocaleString(),
156,
11
);



let y=31;


/* Study summary */
pdf.setFillColor(
249,
246,
233
);

pdf.setDrawColor(
205,
195,
150
);

pdf.roundedRect(
12,
y,
186,
24,
2,
2,
"FD"
);

pdf.setFont(
"helvetica",
"bold"
);

pdf.setTextColor(
50,
50,
50
);

pdf.setFontSize(11);

pdf.text(
"Study Summary",
18,
y+7
);

pdf.setFont(
"helvetica",
"normal"
);

pdf.setFontSize(9);

pdf.text(
`Modality: ${scanType}`,
18,
y+15
);

pdf.text(
`Diagnosis: ${prediction?.label}`,
18,
y+20
);

pdf.text(
`Confidence: ${Math.round(
 prediction?.confidence*100
)}%`,
95,
y+15
);

pdf.text(
`Severity: ${prediction?.severity}`,
95,
y+20
);

y+=32;



/* Sections */
y=sectionCard(
pdf,
"Findings",
findings,
y
);

y=sectionCard(
pdf,
"Impression",
impression,
y
);

y=sectionCard(
pdf,
"Limitations",
limitations,
y,
24
);

y=sectionCard(
pdf,
"Explainability Summary",
isDental
? "Prediction supported through Grad-CAM attention and ROI localization evidence."
: "Prediction supported through Grad-CAM and attribution evidence.",
y,
22
);



/* Visual evidence */
/* only TWO panels — no overlap ever */
if(
gradcamImage || limeImage
){

y+=6;

pdf.setFont(
"helvetica",
"bold"
);

pdf.setFontSize(11);

pdf.setTextColor(
35,
35,
35
);

pdf.text(
"Diagnostic Visual Evidence",
15,
y
);

y+=8;


imageCard(
 pdf,
 "Grad-CAM",
 gradcamImage,
 25,
 y
);


if(limeImage){

imageCard(
 pdf,
 isDental
 ? "Uploaded Image"
 : "Image Explanation",
 limeImage,
 107,
 y
);

}

}



/* Professional Digital Signature Footer */

pdf.setFillColor(
243,
247,
252
);

pdf.setDrawColor(
186,
203,
225
);

pdf.roundedRect(
18,
278,
174,
12,
2,
2,
"FD"
);


pdf.setFont(
"helvetica",
"bold"
);

pdf.setTextColor(
45,
45,
45
);

pdf.setFontSize(8);

pdf.text(
"Digitally Signed by Explainable Radiology Assistant v1.0",
26,
283
);

pdf.setFont(
"helvetica",
"italic"
);

pdf.text(
"Authenticated Explainability Report",
26,
287
);



pdf.save(
"Clinical_XAI_Report.pdf"
);

};



return(
<button
onClick={generatePdf}
disabled={!prediction}
className="
w-full mt-4 py-3 rounded-xl
font-semibold
bg-gradient-to-r
from-blue-600
via-indigo-600
to-teal-600
hover:opacity-95
shadow-xl
"
>
Download Professional PDF Report
</button>
)

}