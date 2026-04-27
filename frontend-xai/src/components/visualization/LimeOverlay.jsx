import { motion } from "framer-motion";

export default function LimeOverlay({ image }) {

return(
<motion.div
 initial={{
  opacity:0,
  scale:.96
 }}
 animate={{
  opacity:1,
  scale:1
 }}
 className="
bg-white/5
backdrop-blur-xl
border border-white/10
rounded-2xl
p-4
shadow-lg
"
>

<h2 className="text-lg font-semibold mb-3 text-white">
Image Explanation
</h2>


<div
 className="
relative
min-h-[320px]
h-[55vh]
max-h-[650px]
rounded-xl
overflow-hidden
bg-black/20
flex items-center justify-center
"
>

{/* subtle explanation glow */}
<div
 className="
absolute inset-0
bg-green-500/20
blur-xl
opacity-60
z-0
"
/>


<img
 src={image}
 alt="LIME"
 className="
relative z-10
w-full
h-full
object-contain
scale-105
"
/>

</div>


<p className="text-sm text-gray-400 mt-3">
Highlighted regions show areas that influenced the model’s decision.
</p>

</motion.div>
)

}