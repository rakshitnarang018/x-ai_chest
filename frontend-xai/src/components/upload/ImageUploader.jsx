import { useState } from "react";
import { motion } from "framer-motion";

export default function ImageUploader({ onUpload }) {

const [preview,setPreview]=useState(null);
const [dragActive,setDragActive]=useState(false);

const handleFile=(file)=>{
 if(!file) return;

 const imageUrl=URL.createObjectURL(file);
 setPreview(imageUrl);
 onUpload(file);
};

const handleDrop=(e)=>{
 e.preventDefault();
 setDragActive(false);
 handleFile(e.dataTransfer.files[0]);
};

return(
<div className="flex flex-col items-center">

<motion.div
 onDragOver={(e)=>{
  e.preventDefault();
  setDragActive(true);
 }}
 onDragLeave={()=>setDragActive(false)}
 onDrop={handleDrop}
 whileHover={{scale:1.02}}
 className={`
 w-full max-w-2xl p-8 rounded-2xl border-2 border-dashed
 cursor-pointer transition-all duration-300
 ${
 dragActive
 ? "border-blue-500 bg-blue-500/10 shadow-lg shadow-blue-500/20"
 : "border-white/20 bg-white/5 hover:border-purple-500 hover:bg-purple-500/10"
 }
 `}
>

<label className="
flex flex-col items-center justify-center
text-center cursor-pointer
">

<input
 type="file"
 accept="image/*"
 className="hidden"
 onChange={(e)=>handleFile(e.target.files[0])}
/>

<motion.div
 animate={{y:dragActive?-5:0}}
 className="text-4xl mb-4"
>
📤
</motion.div>

<p className="text-lg font-medium">
Drag & Drop your image here
</p>

<p className="text-sm text-gray-400 mt-2">
or click to browse
</p>

</label>
</motion.div>


{preview && (
<motion.div
 initial={{opacity:0,scale:.95}}
 animate={{opacity:1,scale:1}}
 className="mt-6 w-full max-w-2xl"
>
<div className="
bg-white/5
border border-white/10
rounded-2xl
p-4
">
<p className="text-gray-400 mb-2">
Preview
</p>

<div className="
w-full
min-h-[320px]
h-[55vh]
max-h-[650px]
rounded-xl
overflow-hidden
bg-black/20
flex items-center justify-center
">
<img
 src={preview}
 alt="preview"
 className="
w-full
h-full
object-contain
"
/>
</div>

</div>
</motion.div>
)}

</div>
)

}