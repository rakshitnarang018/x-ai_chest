import { motion } from "framer-motion";

export default function BoundingBoxOverlay({ image, boxes, show }) {
  return (
    <div className="relative w-full">
      <img src={image} alt="dental" className="rounded-xl w-full" />

      {/* Bounding Boxes */}
      {show &&
        boxes.map((box, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.2 }}
            className="absolute border-2 border-green-400 shadow-lg shadow-green-400/30"
            style={{
              top: box.y,
              left: box.x,
              width: box.width,
              height: box.height,
            }}
          />
        ))}
    </div>
  );
}