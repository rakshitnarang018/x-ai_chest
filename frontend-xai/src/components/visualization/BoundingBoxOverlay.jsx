import {
 useRef,
 useState,
 forwardRef
} from "react";

import { motion } from "framer-motion";


const BoundingBoxOverlay=forwardRef(({
 image,
 boxes,
 show
},captureRef)=>{

const imgRef=useRef(null);

const [dims,setDims]=useState({
 width:1,
 height:1,
 offsetX:0,
 offsetY:0
});



const handleLoad=()=>{

 if(!imgRef.current) return;

 const img=
   imgRef.current;

 const renderedWidth=
   img.clientWidth;

 const renderedHeight=
   img.clientHeight;

 const containerWidth=
   img.parentElement.clientWidth;

 const containerHeight=
   img.parentElement.clientHeight;


 setDims({
  width:renderedWidth,
  height:renderedHeight,
  offsetX:
   (containerWidth-renderedWidth)/2,
  offsetY:
   (containerHeight-renderedHeight)/2
 });

};



return(

<div
 ref={captureRef}
 className="
 relative
 w-full
 h-[420px] md:h-[500px]
 rounded-2xl
 overflow-hidden
 bg-white/5
 border border-white/10
 flex items-center justify-center
"
>

<img
 ref={imgRef}
 src={image}
 alt="dental"
 onLoad={handleLoad}
 draggable={false}
 className="
 max-w-full
 max-h-full
 object-contain
 rounded-xl
 select-none
 "
/>


{
show &&
boxes?.map(
(box,index)=>{


const scaleX=
 dims.width/512;

const scaleY=
 dims.height/512;


/* normal support vs pathology */
const isNormalMode=
 boxes?.length &&
 boxes.every(
  b=>b.confidence>0.7
 );


const borderClass=
 isNormalMode
 ? "border-blue-400 shadow-blue-400/30"
 : "border-green-400 shadow-green-400/30";



/* base box */
let left=
 dims.offsetX+
 (box.x*scaleX);

let top=
 dims.offsetY+
 (box.y*scaleY);

let width=
 box.w*scaleX;

let height=
 box.h*scaleY;



/*
NORMAL SUPPORT
*/
if(isNormalMode){

 width=
  width*0.88;

 const originalHeight=
  height;

 height=
  height*0.58;

 left=
 left+
 (box.w*scaleX*0.06);


 top=
 top+
 (originalHeight*0.34);

}

/*
PATHOLOGY
*/
else{

 top=
 top-
 (height*0.08);

}



/* clamp inside image */
left=Math.max(
 dims.offsetX,
 Math.min(
   left,
   dims.offsetX+
   dims.width-
   width
 )
);

top=Math.max(
 dims.offsetY,
 Math.min(
   top,
   dims.offsetY+
   dims.height-
   height
 )
);



return(

<motion.div
 key={index}
 initial={{
  opacity:0,
  scale:.85
 }}
 animate={{
  opacity:1,
  scale:1
 }}
 transition={{
  delay:index*.15
 }}
 className={`
 absolute
 border-2
 rounded-sm
 shadow-lg
 ${borderClass}
 `}
 style={{
  left,
  top,
  width,
  height,
  pointerEvents:"none"
 }}
/>

)

}
)
}

</div>

)

});


export default BoundingBoxOverlay;