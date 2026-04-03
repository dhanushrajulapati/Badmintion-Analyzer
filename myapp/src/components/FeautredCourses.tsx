"use client";

import Link from "next/link";
import { BackgroundGradient } from "./ui/background-gradient";

import Problems from "../data/data.json";


interface Course {
  id: number;
  title: string;
  slug: string;
  description: string;
  isFeatured: boolean;
}
function FeautredCourses() {
  return (
    <div className="py-12 bg-gray-1000  ">
      <div className="flex items-center justify-center">
        <div className="text-center">
          {/* <h2 className=" text-base test-teal-600 font-semibold tracking-wide lowercase italic">
            ADOBE GENSOLVE
          </h2> */}

          <div className="item">
           
          </div>
        </div>
      </div>
      <div className="mt-10">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 justify-center">
          {Problems.features.map((problem) => (
            <div key={1} className="flex justify-center">
              <BackgroundGradient className="rounded-[22px]  p-4 sm:p-10 bg-white dark:bg-zinc-900 overflow-hidden h-full max-w-sm">
                <div className="p-4 sm:p-6 flex flex-col items-center text-center flex-grow ">
                  <p className="text-lg sm:text-xl text-black mt-4 mb-2 dark:text-neutral-200 ">
                    {problem.title}
                  </p>
                  <p className="text-sm text-neutral-600 dark:text-neutral-400 flex-grow">
                    {problem.description}
                  </p>
                  {/* <Link href={`/courses/${problme.slug}`}>Learn More</Link> */}
                </div>
              </BackgroundGradient>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default FeautredCourses;
