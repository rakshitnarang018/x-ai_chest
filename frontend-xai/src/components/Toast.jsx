import { motion, AnimatePresence } from "framer-motion";

export default function Toast({ message }) {

return (
<AnimatePresence>
{message && (
<motion.div
initial={{
 opacity:0,
 y:30
}}
animate={{
 opacity:1,
 y:0
}}
exit={{
 opacity:0,
 y:30
}}
className="
fixed
bottom-6
right-6
bg-green-600
text-white
px-5
py-3
rounded-xl
shadow-xl
z-[9999]
"
>
{message}
</motion.div>
)}
</AnimatePresence>
);

}