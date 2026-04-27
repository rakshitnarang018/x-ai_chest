import { motion } from "framer-motion";
import { Link, useLocation } from "react-router-dom";
import { useNavigate } from "react-router-dom";

export default function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();

  const navItems = [
    { name: "Home", path: "/" },
    { name: "Detection", path: "/detection" },
  ];

  return (
    <motion.nav
      initial={{ y: -80, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6 }}
      className="fixed top-0 left-0 w-full z-50 backdrop-blur-xl bg-black/60 border-b border-white/10 shadow-lg"
    >
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        
        {/* Logo */}
        <motion.h1
          whileHover={{ scale: 1.05 }}
          className="text-xl md:text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent cursor-pointer"
        >
          AI MedVision
        </motion.h1>

        {/* Nav Links */}
        <div className="flex gap-6 items-center">
          {navItems.map((item, index) => {
            const isActive = location.pathname === item.path;

            return (
              <Link key={index} to={item.path}>
                <motion.div
                  whileHover={{ y: -2 }}
                  className={`relative text-sm md:text-base transition-all duration-300 ${
                    isActive ? "text-blue-400" : "text-gray-400 hover:text-white"
                  }`}
                >
                  {item.name}

                  {/* Active Underline */}
                  {isActive && (
                    <motion.div
                      layoutId="underline"
                      className="absolute left-0 -bottom-1 w-full h-[2px] bg-gradient-to-r from-blue-500 to-purple-500 shadow-[0_0_10px_rgba(99,102,241,0.8)]"
                    />
                  )}
                </motion.div>
              </Link>
            );
          })}
        </div>

        {/* Right Side Button */}
        <motion.button
          whileHover={{ scale: 1.08 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => navigate("/detection")}
          className="hidden md:block px-5 py-2 rounded-lg bg-gradient-to-r from-blue-500 to-purple-600 text-sm font-medium shadow-lg shadow-blue-500/20"
        >
          Try Now
        </motion.button>
      </div>
    </motion.nav>
  );
}