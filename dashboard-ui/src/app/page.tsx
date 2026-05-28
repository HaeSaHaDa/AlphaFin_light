import { DashboardClient } from "@/components/dashboard-client";
import { RuntimeQueryProvider } from "@/runtime-state/runtime-query-context";

export default function HomePage() {
  return (
    <RuntimeQueryProvider>
      <DashboardClient />
    </RuntimeQueryProvider>
  );
}
