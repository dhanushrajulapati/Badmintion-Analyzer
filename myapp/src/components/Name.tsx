"use client";
import { TypewriterEffectSmooth } from "./ui/typewriter-effect";
export function TypewriterEffectSmoothDemo() {
  const words = [
    {
      text: "Welcome",
      className: "text-red-500 dark:text-red-500 bg-blue",
    },
  ];
  return <TypewriterEffectSmooth words={words} />;
}
