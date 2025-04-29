import { Outlet } from "react-router";
import { AppLayout } from "./components/layout/AppLayout";
import { ErrorBoundary } from "./components/error/ErrorBoundry";
import { getGlobalLinks } from "./utils/linkUtils";
import "./app.css"

export const links = getGlobalLinks;

export { ErrorBoundary };

export function Layout({ children }: { children: React.ReactNode }) {
  return <AppLayout>{children}</AppLayout>;
}

export default function App() {
  return <Outlet />;
}