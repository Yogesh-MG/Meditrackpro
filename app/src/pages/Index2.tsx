import React, {useState} from "react";
import { useNavigate } from "react-router-dom";
import { Hospital, ArrowRight, ShieldCheck, BarChart3, Package, Stethoscope } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";
import EmployeeLogin from "@/components/hospital/EmployeeLogin";
import { motion} from "framer-motion"

const Index2 = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);// Add loading state

  // Simulate login with a 2-second delay
  const handleLogin = () => {
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      // Navigate after loading (replace with actual login logic if needed)
      navigate("/dashboard"); // Adjust the route as needed
    }, 2000); // 2-second delay
  };
  
  return (
    <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
    <div className="min-h-screen bg-background flex flex-col">
      

      <main className="flex-1">
        <section className="py-20 px-6">
              <Tabs defaultValue="login">
               <TabsList className="grid w-full grid-cols-2 mb-6">
                  <TabsTrigger value="login">Login</TabsTrigger>
                  <button 
                    onClick={() => navigate("/hospital-registration")} 
                    className="text-sm font-medium text-gray-600 hover:text-gray-900"
                  >
                    Register
                  </button>
                </TabsList>
                <TabsContent value="login" className="space-y-4">
                  <EmployeeLogin /> {/* Now handles actual login */}
                </TabsContent>
                <TabsContent value="info" className="space-y-4">
                </TabsContent>
              </Tabs>
        </section>
        {/* Rest of the file remains unchanged */}
      </main>
    </div>
    </motion.div>
  );
};

export default Index2;