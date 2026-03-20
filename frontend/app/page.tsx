import Image from "next/image";
import DemoOne from "@/components/demo";
import { MatrixText } from "@/components/ui/matrix-text";

export default function Home() {
  return (
    <main className="relative flex min-h-screen flex-col bg-background">
      <header className="sticky top-0 z-50 w-full border-b bg-background/80 backdrop-blur-sm">
        <div className="container mx-auto flex h-16 items-center gap-4 px-4">
          <Image
            src="/pulse_logo.png"
            alt="Pulse Logo"
            width={48}
            height={48}
            className="object-contain"
            priority
          />
          <div className="w-px h-6 bg-white/10" />
          <MatrixText
            text="Today in AI"
            className="text-2xl font-bold tracking-tight text-foreground"
            initialDelay={300}
            letterAnimationDuration={500}
            letterInterval={80}
          />
        </div>
      </header>

      <section className="relative w-full h-[600px] border-b">
        <DemoOne />
      </section>
      
      {/* Rest of the page content would go here */}
      <section className="container mx-auto py-12 px-4">
        <h2 className="text-2xl font-semibold mb-4">Latest Antigravity News</h2>
        <p className="text-muted-foreground">The rest of your dashboard will be implemented here.</p>
      </section>
    </main>
  );
}
