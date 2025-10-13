import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <div className="container mx-auto px-4">
      <section className="mt-24">
        <div className="w-fit mx-auto">
          <h1 className="text-7xl font-bold tracking-tight leading-tight">
            Coming Soon...
          </h1>
          <div className="flex mt-4 justify-center gap-4">
            <Button>Get started</Button>
            <Button variant="outline">Login</Button>
          </div>
        </div>
      </section>
    </div>
  );
}
