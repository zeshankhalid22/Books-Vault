import { Outlet} from "react-router";
import { Header } from "~/components/layout/Header";
import { Footer } from "~/components/layout/Footer";

export default function RootLayout() {
  return (
    <div>
      <Header />
      <main className="pt-16">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}