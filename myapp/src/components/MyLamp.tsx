"use client";
import React from "react";
import { motion } from "framer-motion";
import { LampContainer } from "./ui/lamp";
import { CardBody, CardContainer, CardItem } from "../components/ui/3d-card";
import { BackgroundGradient } from "@/components/ui/background-gradient";

export function LampDemo({ first, children }: any) {
  return (
    <>
      <LampContainer>
        {/* Changed from motion.h1 to motion.div to fix the hydration error */}
        <motion.div
          initial={{ opacity: 0.5, y: 100 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{
            delay: 0.3,
            duration: 0.8,
            ease: "easeInOut",
          }}
          className="mt-8 bg-gradient-to-br from-slate-300 to-slate-500 py-4 bg-clip-text text-center text-4xl font-medium tracking-tight text-transparent md:text-7xl"
        >
          <h1 className="text-lg md:text-7xl text-center font-sans font-bold mb-8 text-white">
            {first}
          </h1>
        </motion.div>
      </LampContainer>
      {children}
    </>
  );
}