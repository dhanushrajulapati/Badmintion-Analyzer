import FeautredCourses from "@/components/FeautredCourses";
import { ThreeDCardDemo } from "@/components/HeroImage";
import HeroSection from "@/components/HeroSection";
import MeetOurInstructors from "@/components/MeetOurInstructors";
import { TypewriterEffectSmoothDemo } from "@/components/Name";
import Testimonial from "@/components/Testimonial";
import { Spotlight } from "@/components/ui/Spotlight";
import Whychooseus from "@/components/Whychooseus";

// const {
//   GoogleGenerativeAI,
//   HarmCategory,
//   HarmBlockThreshold,
// } = require("@google/generative-ai");
// import  {Google}  from "@/google/generative-ai"
// import   {GoogleGenerativeAI,
// HarmCategory,
// HarmBlockThreshold,
// }  from "goog"
export default function Home() {
  return (
    <>
      <main className="bg-black/[0.96] bg-grid-white/[0.02]">
        <div className="flex justify-between py-12 px-12">
          <div className="mr-8">
            <TypewriterEffectSmoothDemo />
            <Spotlight />
            <HeroSection />
          </div>
          <div className="ml-8">
            
          </div>
        </div>
        <FeautredCourses />
       
       
      </main>
    </>
  );
}
