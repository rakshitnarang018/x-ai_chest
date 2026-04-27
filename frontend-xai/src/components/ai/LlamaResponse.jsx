import { motion } from "framer-motion";
import { useEffect, useRef, useState } from "react";

export default function LlamaResponse({ data, loading }) {

  const [displayText,setDisplayText]=useState("");
  const [isTyping,setIsTyping]=useState(false);

  const timerRef=useRef(null);


  useEffect(()=>{

    if(!data) return;

    // cleanup previous animation
    if(timerRef.current){
      clearTimeout(timerRef.current);
    }

    let i=0;

    setDisplayText("");
    setIsTyping(true);


    const typeNext=()=>{

      i++;

      // CRITICAL FIX:
      // render canonical substring
      // never append from stale state
      setDisplayText(
        data.slice(0,i)
      );


      if(i < data.length){
        timerRef.current=
          setTimeout(
            typeNext,
            18 // typing speed
          );
      }
      else{
        setIsTyping(false);
      }

    };


    // slight delay feels nicer
    timerRef.current=
      setTimeout(
        typeNext,
        120
      );


    return ()=>{
      if(timerRef.current){
        clearTimeout(
          timerRef.current
        );
      }
    };

  },[data]);


  return(
    <motion.div
      initial={{opacity:0,y:40}}
      animate={{opacity:1,y:0}}
      className="
      bg-white/5
      backdrop-blur-xl
      border border-white/10
      rounded-2xl
      p-6
      shadow-lg
      "
    >

      <h2 className="text-xl font-semibold mb-4 text-white">
        AI Explanation
      </h2>


      {/* Loading */}
      {loading && (

        <div className="flex items-center gap-3 text-gray-400">

          <div className="flex gap-1">

            <motion.div
             animate={{y:[0,-5,0]}}
             transition={{
               repeat:Infinity,
               duration:0.6
             }}
             className="w-2 h-2 bg-blue-400 rounded-full"
            />

            <motion.div
             animate={{y:[0,-5,0]}}
             transition={{
               repeat:Infinity,
               duration:0.6,
               delay:0.2
             }}
             className="w-2 h-2 bg-purple-400 rounded-full"
            />

            <motion.div
             animate={{y:[0,-5,0]}}
             transition={{
               repeat:Infinity,
               duration:0.6,
               delay:0.4
             }}
             className="w-2 h-2 bg-green-400 rounded-full"
            />

          </div>

          <span>
            Analyzing with AI...
          </span>

        </div>

      )}



      {/* Response */}
      {!loading && data && (

        <motion.p
          initial={{opacity:0}}
          animate={{opacity:1}}
          className="
          text-gray-300
          leading-relaxed
          whitespace-pre-line
          "
        >

          {displayText}

          {isTyping && (
            <span className="animate-pulse">
              |
            </span>
          )}

        </motion.p>

      )}



      {/* Empty */}
      {!loading && !data && (
        <p className="text-gray-400 text-sm">
          AI explanation will appear here.
        </p>
      )}

    </motion.div>
  );

}